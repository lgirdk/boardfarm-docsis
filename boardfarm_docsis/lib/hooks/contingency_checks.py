"""Provide Hook implementations for contingency checks for BF-docsis plugin."""

import json
import logging

from boardfarm.exceptions import ContingencyCheckError
from boardfarm.lib.DeviceManager import device_type
from boardfarm.lib.hooks import contingency_impl, hookimpl
from boardfarm.plugins import BFPluginManager
from termcolor import colored

from boardfarm_docsis.lib.docsis import check_board, check_interface, check_provisioning
from boardfarm_docsis.lib.voice import check_peer_registration

logger = logging.getLogger("tests_logger")


class ContingencyCheck:
    """Contingency check implementation."""

    impl_type = "base"

    # NOTE: not using tryfirst here, as we want boardfarm contingency check
    # to be executed first
    @hookimpl
    def contingency_check(self, env_req, dev_mgr, env_helper):
        """Register service check plugins based on env_req.

        Reading the key value pairs from env_req, BFPluginManager scans
        for relative hook specs and implementations and loads them into a
        feature PluginManager (use generate_feature_manager).

        Once all plugins are registered, this functions will call the hook
        initiating respective service checks.

        :param env_req: ENV request provided by a test
        :type env_req: dict
        """

        if "CMTS" not in env_helper.env["environment_def"]:
            logger.info("Not Executing contingency service checks under BF Docsis")
            return []

        logger.info("Executing all contingency service checks under BF Docsis")

        pm = BFPluginManager("contingency")
        pm.load_hook_specs("feature")
        all_impls = pm.fetch_impl_classes("feature")

        plugins_to_register = [all_impls["boardfarm_docsis.DefaultChecks"]]

        if "voice" in env_req.get("environment_def", {}):
            plugins_to_register.append(all_impls["boardfarm_docsis.Voice"])

        for i in reversed(plugins_to_register):
            pm.register(i)
        result = pm.hook.service_check(
            env_req=env_req, dev_mgr=dev_mgr, env_helper=env_helper
        )

        # this needs to be orchestrated by hook wrapper maybe
        BFPluginManager.remove_plugin_manager("contingency")
        return result


class DefaultChecks:
    """Perform these checks even if ENV req is empty."""

    impl_type = "feature"

    @contingency_impl
    def service_check(self, env_req, dev_mgr, env_helper):
        """Implement Default Contingency Hook."""

        logger.info(
            "Executing Default service checks[check_board,check_provisioning] for BF Docsis"
        )

        if not dev_mgr.board.is_erouter_honouring_config():
            msg = colored(
                "esafeErouterInitModeControl not set to 5 (honoreRouterInitMode)!!!!!",
                color="red",
                attrs=["bold"],
            )
            logger.critical(msg)
            logger.critical("Possible hint: a previous test did not cleanup?")
            raise ContingencyCheckError(msg)

        cm_mac = dev_mgr.board.config["cm_mac"]
        voice = "voice" in env_req.get("environment_def", {})
        board = dev_mgr.by_type(device_type.DUT)
        cmts = dev_mgr.by_type(device_type.cmts)

        check_board(board, cmts, cm_mac)
        check_provisioning(dev_mgr.board, mta=voice)

        logger.info(
            "Default service checks[check_board,check_provisioning] for BF Docsis executed"
        )


class CheckInterface:
    """Perform these checks even if ENV req is empty."""

    impl_type = "feature"

    @contingency_impl(trylast=True)
    def service_check(self, env_req, dev_mgr, env_helper):
        """Implement Default Contingency Hook."""

        logger.info("Executing CheckInterface service check for BF Docsis")

        ip = {}
        board = dev_mgr.by_type(device_type.DUT)

        if env_helper.has_prov_mode():
            prov_mode = env_helper.get_prov_mode()
        else:
            prov_mode = "dual"  # default prov mode is dual

        ip_ifaces = [
            board.mta_iface,
            board.wan_iface,
            board.erouter_iface,
        ]

        if prov_mode.lower() in ["dslite", "ipv6"]:
            ip_ifaces.append(board.aftr_iface)
        elif prov_mode.lower() in ["disabled", "bridge"]:
            ip_ifaces.append(board.lan0_iface)
        else:
            ip_ifaces.append(board.lan_iface)

        ip["board"] = board.get_ifaces_ip_dict(ip_ifaces)

        try:
            # validate if all collected ip addresses are as per provisioning mode.
            if prov_mode != "none":
                check_interface(board, ip, prov_mode, [])
        except Exception as e:
            print(f"Interface check failed.\nReason: {e}")
            print(json.dumps(ip, indent=4))
            raise e
        logger.info("CheckInterface service checks for BF Docsis executed")

        return ip


class Voice:

    impl_type = "feature"

    @contingency_impl
    def service_check(self, env_req, dev_mgr, env_helper):
        """Implement contingency check for voice."""

        logger.info("Executing Voice service check for BF Docsis")

        sipserver = dev_mgr.by_type(device_type.sipcenter)
        board = dev_mgr.by_type(device_type.DUT)
        fxs_devices = [dev_mgr.fxs1, dev_mgr.fxs2]
        num_list = [fxs.own_number for fxs in fxs_devices]

        assert board.mta_prov_check(), "MTA is not provisioned!"
        assert (
            board.check_sip_endpoints_registration()
        ), "SIP endpoints are not registered"
        assert board.is_sip_endpoint_idle(), "MTA endpoints on board are not idle"

        check_peer_registration(board, num_list, sipserver)

        logger.info("Voice service checks for BF Docsis executed")
