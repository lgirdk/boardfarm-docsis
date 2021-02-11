"""Provide Hook implementations for contingency checks for BF-docsis plugin."""

from boardfarm.lib.hooks import contingency_impl, hookimpl
from boardfarm.plugins import BFPluginManager


class ContingencyCheck:
    """Contingency check implementation."""

    impl_type = "base"

    # NOTE: not using tryfirst here, as we want boardfarm contingency check
    # to be executed first
    @hookimpl
    def contingency_check(self, env_req, dev_mgr):
        """Register service check plugins based on env_req.

        Reading the key value pairs from env_req, BFPluginManager scans
        for relative hook specs and implementations and loads them into a
        feature PluginManager (use generate_feature_manager).

        Once all plugins are registered, this functions will call the hook
        initiating respective service checks.

        :param env_req: ENV request provided by a test
        :type env_req: dict
        """
        # Print statement can be removed later. Kept for understand exec flow
        print("This is BF docsis contingency check")

        pm = BFPluginManager("contingency")
        pm.load_hook_specs("feature")
        all_impls = pm.fetch_impl_classes("feature")

        # same theory here, based on env_req decide which plugin to register
        # TODO: Add right set of rules here.
        if "voice" in env_req.get("environment_def", {}):
            pm.register(all_impls["boardfarm_docsis.Voice"])
        pm.hook.service_check(env_req=env_req, dev_mgr=dev_mgr)

        # this needs to be orchestrated by hook wrapper maybe
        BFPluginManager.remove_plugin_manager("contingency")


class Voice:
    """Dummy implementation for Demo.

    Consider this to be an implementation for PacketCable 1.5
    """

    impl_type = "feature"

    @contingency_impl
    def service_check(self, env_req, dev_mgr):
        """Implement contingency check for voice."""
        print("Voice service checks executed", end=("\n" + "-" * 80 + "\n"))
