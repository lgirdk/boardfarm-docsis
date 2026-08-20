"""Boardfarm DOCSIS API plugin: router registration for templates and use cases."""

from __future__ import annotations

from pluggy import HookimplMarker

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boardfarm3.api.routers import RouterBundle

hookimpl_api = HookimplMarker("boardfarm_api")


@hookimpl_api
def boardfarm_add_api_routers() -> list[RouterBundle]:  # pylint: disable=too-many-locals
    """Return the DOCSIS boardfarm API routers, generated from template ABCs.

    :return: one RouterBundle for the ``docsis`` namespace
    :rtype: list[RouterBundle]
    """
    from boardfarm3.api.routers import (  # pylint: disable=import-outside-toplevel
        RouterBundle,
    )
    from boardfarm3.api.routers._generator import (  # pylint: disable=import-outside-toplevel
        TemplateMount,
        generate_template_routers,
    )
    from boardfarm3.api.routers._usecase_generator import (  # pylint: disable=import-outside-toplevel
        generate_usecase_routers,
    )
    from boardfarm3_docsis.templates.cable_modem.cable_modem import (  # pylint: disable=import-outside-toplevel
        CableModem,
    )
    from boardfarm3_docsis.templates.cable_modem.cable_modem_hw import (  # pylint: disable=import-outside-toplevel
        CableModemHW,
    )
    from boardfarm3_docsis.templates.cable_modem.cable_modem_sw import (  # pylint: disable=import-outside-toplevel
        CableModemSW,
    )
    from boardfarm3_docsis.templates.cmts import (  # pylint: disable=import-outside-toplevel
        CMTS,
    )
    from boardfarm3_docsis.templates.ntu.docsis_ntu import (  # pylint: disable=import-outside-toplevel
        DocsisNTU,
    )
    from boardfarm3_docsis.templates.provisioner import (  # pylint: disable=import-outside-toplevel
        Provisioner,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        connectivity as uc_connectivity,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        docsis as uc_docsis,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        erouter as uc_erouter,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        net_tools as uc_net_tools,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        networking as uc_networking,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        snmp as uc_snmp,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        software_update as uc_software_update,
    )
    from boardfarm3_docsis.use_cases import (  # pylint: disable=import-outside-toplevel
        tr069 as uc_tr069,
    )

    templates: list[type | TemplateMount] = [
        CMTS,
        Provisioner,
        DocsisNTU,
        TemplateMount("cable_modem", CableModem, CableModemSW, "sw"),
        TemplateMount("cable_modem", CableModem, CableModemHW, "hw"),
    ]
    routers, skipped = generate_template_routers(templates)
    uc_routers, uc_skipped = generate_usecase_routers(
        [
            uc_connectivity,
            uc_docsis,
            uc_erouter,
            uc_net_tools,
            uc_networking,
            uc_snmp,
            uc_software_update,
            uc_tr069,
        ]
    )
    return [
        RouterBundle(
            namespace="docsis",
            routers=[*routers, *uc_routers],
            skipped=[*skipped, *uc_skipped],
        )
    ]
