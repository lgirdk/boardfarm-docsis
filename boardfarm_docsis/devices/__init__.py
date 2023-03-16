# Copyright (c) 2019
#
# All rights reserved.
import importlib
import inspect
import pkgutil

device_sw_mappings = {}
device_mappings = {}


def probe_devices():
    """Dynamically find all devices classes across all boardfarm projects."""

    import boardfarm

    all_boardfarm_modules = dict(boardfarm.plugins)
    all_boardfarm_modules["boardfarm"] = importlib.import_module("boardfarm")

    all_mods = []

    # Loop over all modules to import their devices
    for modname in all_boardfarm_modules:
        bf_module = all_boardfarm_modules[modname]
        device_module = pkgutil.get_loader(".".join([bf_module.__name__, "devices"]))
        if device_module:
            all_mods += boardfarm.walk_library(
                device_module.load_module(),
                filter_pkgs=["base_devices", "connections", "platform"],
            )

    for module in all_mods:
        device_mappings[module] = []
        for thing_name in dir(module):
            thing = getattr(module, thing_name)
            if inspect.isclass(thing):
                if hasattr(thing, "model"):
                    # thing.__module__ prints the module name where it is defined
                    # this name needs to match the current module we're scanning.
                    # else we skip
                    if thing.__module__ == module.__name__:
                        device_mappings[module].append(thing)

                if hasattr(thing, "regex_fw"):
                    if thing.__module__ == module.__name__:
                        device_sw_mappings[thing] = thing.regex_fw
