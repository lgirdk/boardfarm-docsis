"""Provide Hook implementations for contingency checks for BF-docsis plugin."""

import json
import logging

from boardfarm.exceptions import BftSysExit
from boardfarm.lib.DeviceManager import device_type
from boardfarm.lib.hooks import contingency_impl, hookimpl
from boardfarm.plugins import BFPluginManager
from termcolor import colored

from boardfarm_docsis.lib.docsis import (
    check_board,
    check_cm_firmware_version,
    check_interface,
    check_provisioning,
)
from boardfarm_docsis.lib.voice import check_peer_registration

logger = logging.getLogger("bft")


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
        print(
            "Executing BF Docsis contingency service check",
            end=("\n" + "-" * 80 + "\n"),
        )

        pm = BFPluginManager("contingency")
        pm.load_hook_specs("feature")
        all_impls = pm.fetch_impl_classes("feature")

        plugins_to_register = [all_impls["boardfarm_docsis.DefaultChecks"]]

        if "voice" in env_req.get("environment_def", {}):
            plugins_to_register.append(all_impls["boardfarm_docsis.Voice"])

        plugins_to_register.append(all_impls["boardfarm_docsis.CheckInterface"])

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
        print(
            "Executing Default service check for BF Docsis",
            end=("\n" + "-" * 80 + "\n"),
        )

        if not dev_mgr.board.is_erouter_honouring_config():
            msg = colored(
                "esafeErouterInitModeControl not set to 5 (honoreRouterInitMode)!!!!!",
                color="red",
                attrs=["bold"],
            )
            logger.critical(msg)
            logger.critical("Possible hint: a previous test did not cleanup?")
            raise BftSysExit(msg)

        cm_mac = dev_mgr.board.config["cm_mac"]
        voice = "voice" in env_req.get("environment_def", {})
        board = dev_mgr.by_type(device_type.DUT)
        wan = dev_mgr.by_type(device_type.wan)
        cmts = dev_mgr.by_type(device_type.cmts)

        check_board(board, cmts, cm_mac)
        check_provisioning(dev_mgr.board, mta=voice)
        check_cm_firmware_version(board, wan, env_helper)

        print(
            "Default service checks for BF DOCSIS executed",
            end=("\n" + "-" * 80 + "\n"),
        )


class CheckInterface:
    """Perform these checks even if ENV req is empty."""

    impl_type = "feature"

    @contingency_impl(trylast=True)
    def service_check(self, env_req, dev_mgr, env_helper):
        """Implement Default Contingency Hook."""
        print(
            "Executing service check for BF DOCSIS CheckInterface",
            end=("\n" + "-" * 80 + "\n"),
        )

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

        ip["board"] = board.get_ifaces_ip_dict(ip_ifaces)

        try:
            # validate if all collected ip addresses are as per provisioning mode.
            check_interface(board, ip, prov_mode, [])
        except Exception as e:
            print("Interface check failed.\nReason: %s" % e)
            print(json.dumps(ip, indent=4))
            raise (e)

        print(
            "Service checks for BF DOCSIS CheckInterface executed",
            end=("\n" + "-" * 80 + "\n"),
        )

        return ip


class Voice:

    impl_type = "feature"

    @contingency_impl
    def service_check(self, env_req, dev_mgr, env_helper):
        """Implement contingency check for voice."""
        print("Executing service check for Voice", end=("\n" + "-" * 80 + "\n"))

        sipserver = dev_mgr.by_type(device_type.sipcenter)
        board = dev_mgr.by_type(device_type.DUT)
        lan_devices = [dev_mgr.lan, dev_mgr.lan2]
        num_list = [lan.own_number for lan in lan_devices]

        check_peer_registration(board, num_list, sipserver)

        print("Voice service checks executed", end=("\n" + "-" * 80 + "\n"))