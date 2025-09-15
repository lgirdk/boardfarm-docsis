<div id="top_nav">

[|||](# "Toggle sidebar")

# [Boardfarm Docsis documentation](# "Go to homepage")

[](search.html "Search")

<div class="searchbox_wrapper">

</div>

</div>

<div class="sphinxsidebar" role="navigation" aria-label="main navigation">

<div class="sphinxsidebarwrapper">

<span class="caption-text">Use Cases</span>

  - [Connectivity Use Cases](#document-connectivity)
  - [Docsis Use Cases](#document-docsis)
  - [Erouter Use Cases](#document-erouter)
  - [Net\_tools Use Cases](#document-net_tools)
  - [SNMP Use Cases](#document-snmp)
  - [TR069 Use Cases](#document-tr069)

</div>

</div>

<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" role="main">

<div id="boardfarm3-docsis-suite-use-cases-documentation" class="section">

# Boardfarm3\_docsis suite Use Cases documentation[¶](#boardfarm3-docsis-suite-use-cases-documentation "Link to this heading")

<div class="toctree-wrapper compound">

<span id="document-connectivity"></span>

<div id="connectivity-use-cases" class="section">

## Connectivity Use Cases[¶](#connectivity-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.connectivity" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.connectivity "Link to this heading")

Use Cases to handle getting the CPE online.

  - <span class="sig-name descname"><span class="pre">enable\_tunnel\_iface</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">aftr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">AFTR</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.enable_tunnel_iface "Link to this definition")
    Enable tunnel iface by configuring AFTR post mode switch.

    <div class="admonition hint">

    Hint

    This use case to be used:

      - When modem reprovisioning is done with ipv6 mode.

    Note: not to be used if board is booted with ipv6 mode.

    </div>

      - Parameters<span class="colon">:</span>

          - **aftr** (*AFTR*) – AFTR device instance

          - **board** (*CPE,* *optional*) – cpe device instance, defaults to None

          - **wan** (*WAN,* *optional*) – WAN client, defaults to None

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_interface\_mtu\_size</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">WLAN</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.get_interface_mtu_size "Link to this definition")
    Return the MTU size of the interface in bytes.

      - Parameters<span class="colon">:</span>

          - **device** (*CPE* *|* *LAN* *|* *WAN* *|* *WLAN*) – device instance

          - **interface** (*str*) – name of the interface

      - Returns<span class="colon">:</span>
        MTU size of the interface in bytes

      - Return type<span class="colon">:</span>
        int

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_interface\_status</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPEInterfaces</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">HostInterfaces</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.get_interface_status "Link to this definition")
    Return the status of the Linux interface.

    If the interface link is up or down on the device.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Check that the \[\] interface is up

    </div>

      - Parameters<span class="colon">:</span>

          - **device** (*LAN* *|* *WAN* *|* *CPE*) – device class object

          - **interface** (*CPEInterfaces* *|* *HostInterfaces* *|* *PONCPEInterface*) – enum for possible values for interfaces definition

      - Raises<span class="colon">:</span>
        **UseCaseFailure** – when device doesn’t have attribute mapped in enum

      - Returns<span class="colon">:</span>
        True if interface is up else False

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_subnet\_mask</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">WLAN</span></span>*, *<span class="n"><span class="pre">interface</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.get_subnet_mask "Link to this definition")
    Get the subnet mask of the interface.

      - Parameters<span class="colon">:</span>

          - **device** (*LAN* *|* *WAN* *|* *WLAN*) – device instance

          - **interface** (*str*) – name of the inerface

      - Returns<span class="colon">:</span>
        subnet mask of the interface

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">has\_ipv6\_tunnel\_interface\_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.has_ipv6_tunnel_interface_address "Link to this definition")
    Check for the tunnel interface on DUT console.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Check for the tunnel interface on DUT console.

    </div>

      - Parameters<span class="colon">:</span>
        **board** (*CPE* *|* *None,* *optional*) – the board object, defaults to None

      - Returns<span class="colon">:</span>
        True if tunnel interface is present else False

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">is\_board\_online\_after\_reset</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.is_board_online_after_reset "Link to this definition")
    Check board online after reset.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify CPE comes online after the factory reset

      - Verify DUT comes back online

    </div>

      - Returns<span class="colon">:</span>
        True if board is online else false

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">is\_wan\_accessible\_on\_client</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">who\_access</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">LAN</span></span>*, *<span class="n"><span class="pre">port</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">is\_ipv6</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.is_wan_accessible_on_client "Link to this definition")
    Ping the WAN IP address max with 2 retries from the lan/wifi client.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Check that the connected LAN client is able to access the internet

      - Verify LAN Client is able to reach the internet

    </div>

      - Parameters<span class="colon">:</span>

          - **who\_access** (*LAN*) – name of the client who wants to ping wan side

          - **port** (*int*) – port to which to perform the curl on wan client

          - **is\_ipv6** (*bool*) – whether to ping ipv4 or ipv6 address for wan

          - **wan** (*WAN* *|* *None*) – WAN client to be pinged

      - Returns<span class="colon">:</span>
        True if ping returns a success

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">power\_cycle</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.power_cycle "Link to this definition")
    Power cycle the board.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform a reboot on the CPE

      - Reboot the DUT

      - Do power cycle of DUT

    </div>

    Turn OFF and turn ON the board and wait for the boot to start This method is preferred to wait\_for\_board\_boot\_start as the power cycle and wait for the board boot is handled in this use case

      - Parameters<span class="colon">:</span>
        **board** (*CPE* *|* *None,* *optional*) – the board object, defaults to None

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">reset\_board\_via\_cmts</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.reset_board_via_cmts "Link to this definition")
    Reset the board via CMTS.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Reset the board via CMTS.

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – cpe device instance

          - **cmts** (*CMTS*) – cmts device instance

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">wait\_for\_board\_boot\_start</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.connectivity.wait_for_board_boot_start "Link to this definition")
    Wait for the board boot to start.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify that DUT comes online.

    </div>

    The usage if this directly in the test would be depecrated in favour of power\_cycle() as it would handle both board turn OFF and ON and wait for board boot to start

      - Parameters<span class="colon">:</span>
        **board** (*CPE* *|* *None,* *optional*) – the board object, defaults to None

</div>

</div>

<span id="document-docsis"></span>

<div id="docsis-use-cases" class="section">

## Docsis Use Cases[¶](#docsis-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.docsis" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.docsis "Link to this heading")

Use Cases to interact with DOCSIS devices such as CMTS and CM.

  - <span class="sig-name descname"><span class="pre">add\_tlvs\_to\_bootfile</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">multiline\_tlv</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">config\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.add_tlvs_to_bootfile "Link to this definition")
    Add TLVs to the boot file in the env\_hepler.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Add TLVs to the boot file in the env\_hepler.

    </div>

      - Adds/appends TLVs (as multiline string) at the end of the boot file, just before
        the CmMic comment line

    <!-- end list -->

      - Parameters<span class="colon">:</span>

          - **multiline\_tlv** (*str*) – a string with embedded newlines with the TLVs to be added

          - **config\_file** (*str* *|* *None*) – updated config file

          - **board** (*CableModem*) – Cable Modem device instance

      - Raises<span class="colon">:</span>
        **ValueError** – if the string hook was not found in the bootfile

      - Returns<span class="colon">:</span>
        a copy of the env\_helper bootfile with the TLVs added

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">are\_boot\_logs\_successful</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.are_boot_logs_successful "Link to this definition")
    Collect the boot logs and validate the boot stages and provisioning.

      - Parameters<span class="colon">:</span>

          - **timeout** (*int*) – time value to collect the logs for

          - **board** (*CableModem*) – Cable Modem device instance

      - Returns<span class="colon">:</span>
        True if boot stages are verified and provisioning is successful else False

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_cable\_modem\_channels</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.get_cable_modem_channels "Link to this definition")
    Get the CM channel values from the CMTS.

    <div class="highlight-python notranslate">

    <div class="highlight">

        # example output
        {
            "US": "1(2,3,4,5,6,7,8)",
            "DS": "9(1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)",
        }

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – Cable Modem device instance

          - **cmts** (*CMTS*) – CMTS device instance

      - Returns<span class="colon">:</span>
        Cable Modem channel values

      - Return type<span class="colon">:</span>
        dict\[str, str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_downstream\_bonded\_channel</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.get_downstream_bonded_channel "Link to this definition")
    Get the Downstream bonded channel value from the CMTS.

    <div class="highlight-python notranslate">

    <div class="highlight">

        # example output
        "9"

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – Cable Modem device instance

          - **cmts** (*CMTS*) – CMTS device instance

      - Returns<span class="colon">:</span>
        Downstream bonded channel value

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_ds\_frequecy\_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.get_ds_frequecy_list "Link to this definition")
    Return the frequency list of CableModem.

    Get the Downstream frequency list from the CableModem device.

    <div class="highlight-python notranslate">

    <div class="highlight">

        # example output:
        [
            "137000000",
            "242000000",
            "274000000",
            "300000000",
            "305000000",
            "306750000",
            "330250000",
            "330750000",
            "331000000",
            "370750000",
            "338000000",
            "338750000",
            "339000000",
            "402000000",
            "402750000",
            "410000000",
            "418000000",
            "426000000",
            "434000000",
            "442000000",
            "450000000",
            "458000000",
            "466000000",
            "474000000",
            "482000000",
            "490000000",
            "498000000",
            "578000000",
            "586750000",
            "594000000",
            "618000000",
            "634000000",
            "666000000",
            "730000000",
            "754000000",
            "778000000",
            "786000000",
            "810000000",
            "826000000",
            "842000000",
        ]

    </div>

    </div>

      - Parameters<span class="colon">:</span>
        **board** (*CableModem*) – CableModem device instance

      - Returns<span class="colon">:</span>
        frequency list of CPE

      - Return type<span class="colon">:</span>
        list\[str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_upstream\_bonded\_channel</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.get_upstream_bonded_channel "Link to this definition")
    Get the upstream bonded channel value from the CMTS.

    <div class="highlight-python notranslate">

    <div class="highlight">

        # example output
        "8"

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – Cable Modem device instance

          - **cmts** (*CMTS*) – CMTS device instance

      - Returns<span class="colon">:</span>
        Upstream bonded channel value

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_vendor\_id\_from\_cm\_bootfile</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.get_vendor_id_from_cm_bootfile "Link to this definition")
    Fetch the vendor identifier hexadecimal value from CM bootfile.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Fetch the vendor identifier hexadecimal value from CM bootfile.

    </div>

      - Parameters<span class="colon">:</span>
        **board** (*CableModem*) – Cable Modem device instance

      - Returns<span class="colon">:</span>
        hexadecimal value of vendor identifier

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">is\_bpi\_privacy\_disabled</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.is_bpi_privacy_disabled "Link to this definition")
    Fetch the GlobalPrivacy TLV value in CM config file.

    Return True if GlobalPrivacyEnable inside config file is set to Integer 0. By default, BPI privacy is enabled in CM config file.

    This use case will be used for scenarios where BPI+ encyption is not used. i.e. Multicast

      - Parameters<span class="colon">:</span>
        **board** (*CableModem*) – CableModem device instance, defaults to None

      - Raises<span class="colon">:</span>

          - **ValueError** – when the board object is None

          - **ValueError** – when the bootfile is an empty string

      - Returns<span class="colon">:</span>
        True if BPI is disabled.

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">is\_route\_present\_on\_cmts</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">route</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">IPv4Network</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">IPv6Network</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.is_route_present_on_cmts "Link to this definition")
    Check if routing table of CMTS router contains a route.

    Perfrom `ip route` command on a router, collect the routes and check if route is present in table output.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify that the CMTS learns route

      - Make sure that the packets can be captured between CPE and CMTS

    </div>

    <div class="highlight-python notranslate">

    <div class="highlight">

        # example usage
        status = is_route_present_on_cmts(
            route=ipaddress.ip_network("192.168.101.0/24"),
        )

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **route** (*IPv4Network* *|* *IPv6Network*) – route to be looked up on CMTS

          - **cmts** (*CMTS*) – CMTS to be used

      - Returns<span class="colon">:</span>
        True if route is present on CMTS

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">override\_boot\_files</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">cm\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">mta\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.override_boot_files "Link to this definition")
    Configure the boot file.

    This method implements what in Boardfarm v2 was configure\_boot\_file(), but does not update the objects’ configuration anymore. In Boardfarm v2, the CPE object needed update before a call to the provisioning Use Cases was made. As such, it is deprecated in favour of passing the files explicitly to the appropriate Use Case.

    In Boardfarm v3 the user should choose between provision\_docsis\_board() and provision\_docsis\_board\_and\_reboot\_it()

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – the Cable Modem to be provisioned

          - **cm\_boot\_file** (*str* *|* *None,* *optional*) – Cable Modem config, defaults to None

          - **mta\_boot\_file** (*str* *|* *None,* *optional*) – eMTA config, defaults to None

      - Returns<span class="colon">:</span>
        the two configuration files in string format

      - Return type<span class="colon">:</span>
        tuple\[str, str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">provision\_board\_w\_boot\_files</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">tftp</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">mta\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.provision_board_w_boot_files "Link to this definition")
    Provision Cable Modem with given boot files.

    This Use Case is deprecated in favour of provision\_docsis\_board\_and\_reboot\_it(). Said Use Case forces us to be more explicit.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Initialize DUT using boot file with below parameters

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – the Cable Modem to be provisioned

          - **provisioner** (*Provisioner*) – the Provisioner

          - **tftp** (*WAN*) – the TFTP device

          - **cm\_boot\_file** – Cable Modem boot file, defaults to None

          - **cm\_boot\_file** – str | None

          - **mta\_boot\_file** – MTA boot file, defaults to None

          - **mta\_boot\_file** – str | None

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">provision\_cable\_modem</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">emta\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.provision_cable_modem "Link to this definition")
    Provision the Cable Modem.

    With this function, the CM and eMTA boot files can be None. This function is deprecated; prefer to use provision\_docsis\_board() instead. That ensures that we are explicit, rather than implicit.

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – the CM to be provisioned

          - **provisioner** (*Provisioner*) – the Provisioner

          - **wan** (*WAN*) – the TFTP device

          - **cm\_boot\_file** (*str* *|* *None*) – content of the CM boot file, defaults to None

          - **emta\_boot\_file** (*str* *|* *None*) – content of the eMTA boot file, defaults to None

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">provision\_docsis\_board</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">emta\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.provision_docsis_board "Link to this definition")
    Provision the Cable Modem with the given CM and eMTA boot files.

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – the Cable Modem to be provisioned

          - **provisioner** (*Provisioner*) – DOCSIS provisioner

          - **wan** (*WAN*) – TFTP server

          - **cm\_boot\_file** (*str*) – Cable Modem config

          - **emta\_boot\_file** (*str*) – eMTA config

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">provision\_docsis\_board\_and\_reboot\_it</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">provisioner</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Provisioner</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cm\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">emta\_boot\_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.provision_docsis_board_and_reboot_it "Link to this definition")
    Provision the Cable Modem with the given bootfiles and reboot it.

    This Use Case performs a CPE-triggered software reboot.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Initialize DUT using boot file with below parameters

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CableModem*) – the Cable Modem to be provisioned

          - **provisioner** (*Provisioner*) – DOCSIS provisioner

          - **wan** (*WAN*) – TFTP server

          - **cm\_boot\_file** (*str*) – Cable Modem config

          - **emta\_boot\_file** (*str*) – eMTA config

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">update\_erouter\_mode</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CableModem</span></span>*, *<span class="n"><span class="pre">bootfile</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.docsis.update_erouter_mode "Link to this definition")
    Switch the bootfile eRouter config in the env\_helper to given mode.

    If the mode has to be switched multiple times then the bootfile param to be used. bootfile param should be the current eRouter config and not the one in env\_helper.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Switch to modem mode using config file

      - Switch the provisioning mode via config file

      - Switch back to IPv4 provisioning mode using config file

    </div>

      - Parameters<span class="colon">:</span>

          - **mode** (*str*) – one of “none”, “disabled”, “ipv4”, “ipv6”, “dual”

          - **board** (*CableModem*) – Cable Modem device instance

          - **bootfile** (*str*) – config file to be used before updating mode

      - Raises<span class="colon">:</span>
        **ValueError** – if mode is not valid

      - Returns<span class="colon">:</span>
        a copy of the env\_helper bootfile with the new mode

      - Return type<span class="colon">:</span>
        str

</div>

</div>

<span id="document-erouter"></span>

<div id="erouter-use-cases" class="section">

## Erouter Use Cases[¶](#erouter-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.erouter" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.erouter "Link to this heading")

eRouter use cases.

  - <span class="sig-name descname"><span class="pre">get\_board\_guest\_ip\_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry\_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_board_guest_ip_address "Link to this definition")
    Get the board’s Guest IP addresses.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify that the guest interface acquires an IPv4/IPv6 address.

    </div>

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – instance of CPE

          - **retry\_count** (*int*) – number of retries

      - Returns<span class="colon">:</span>
        IPAddress of guest interface

      - Return type<span class="colon">:</span>
        IPAddresses

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_board\_lan\_ip\_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry\_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_board_lan_ip_address "Link to this definition")
    Get the board’s LAN IP addresses.

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – instance of CPE

          - **retry\_count** (*int*) – number of retries

      - Returns<span class="colon">:</span>
        IPAddress of LAN interface

      - Return type<span class="colon">:</span>
        IPAddresses

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_erouter\_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">retry\_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_erouter_addresses "Link to this definition")
    Get erouter IPv4, IPv6 addresses.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Check if eRouter gets an IP address.

      - Check if the eRouter WAN Interface acquires IPv4 and IPv6 address

    </div>

      - Parameters<span class="colon">:</span>

          - **retry\_count** (*int*) – number of retries to get IPs

          - **board** (*CPE*) – CPE device instance

      - Returns<span class="colon">:</span>
        erouter IP addresses data class

      - Return type<span class="colon">:</span>
        IPAddresses

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_erouter\_iface\_ipv6\_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPv6Address</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_erouter_iface_ipv6_address "Link to this definition")
    Get eRouter interface IPv6 address.

      - Parameters<span class="colon">:</span>
        **board** (*CPE*) – CPE device instance

      - Returns<span class="colon">:</span>
        IPv6 address of eRouter interface

      - Return type<span class="colon">:</span>
        IPv6Address

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_mta\_iface\_ip\_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry\_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_mta_iface_ip_addresses "Link to this definition")
    Get the voice interface IP addresses.

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – CPE device instance

          - **retry\_count** (*int*) – number of retries

      - Returns<span class="colon">:</span>
        IP addresses of voice interface

      - Return type<span class="colon">:</span>
        IPAddresses

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_wan\_iface\_ip\_addresses</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry\_count</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">IPAddresses</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.get_wan_iface_ip_addresses "Link to this definition")
    Get the management interface IP addresses.

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – CPE device instance

          - **retry\_count** (*int*) – number of retries

      - Returns<span class="colon">:</span>
        IP addresses of management interface

      - Return type<span class="colon">:</span>
        IPAddresses

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">verify\_erouter\_ip\_address</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">retry</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.erouter.verify_erouter_ip_address "Link to this definition")
    Verify the eRouter interface has the correct IP addresses for the specified mode.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify eRouter gets an IP address.

      - Check if the eRouter WAN Interface acquires IPv4 and/or IPv6 address

    </div>

      - Parameters<span class="colon">:</span>

          - **mode** (*str*) – mode could be IPv4, IPv6/DSLite, Dual, disabled/bridge/modem

          - **board** (*CPE*) – CPE device instance

          - **retry** (*int*) – number of retries in order to fetch the erouter IP, defaults to 1

      - Returns<span class="colon">:</span>
        True if the eRouter has correct IPv4/IPv6 address based on the mode passed

      - Return type<span class="colon">:</span>
        bool

</div>

</div>

<span id="document-net_tools"></span>

<div id="net-tools-use-cases" class="section">

## Net\_tools Use Cases[¶](#net-tools-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.net_tools" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.net_tools "Link to this heading")

Network utility helper use cases.

  - *<span class="pre">class</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">DNS</span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.DNS "Link to this definition")
    DNS use cases.

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">get\_dns\_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.DNS.get_dns_record "Link to this definition")
        Perform nslookup and return the parsed results.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **domain\_name** (*str*) – domain name to perform nslookup on

          - Returns<span class="colon">:</span>
            parsed nslookup results as dictionary

          - Return type<span class="colon">:</span>
            dict\[str, Any\]

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">nslookup\_AAAA\_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-q=AAAA'</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.DNS.nslookup_AAAA_record "Link to this definition")
        Perform nslookup for AAAA records and return the parsed results.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **domain\_name** (*str*) – domain name to perform nslookup on

              - **opts** (*str*) – nslookup command line options

              - **extra\_opts** (*str*) – nslookup additional command line options

          - Returns<span class="colon">:</span>
            parsed nslookup results as dictionary

          - Return type<span class="colon">:</span>
            dict\[str, Any\]

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">nslookup\_A\_record</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">domain\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-q=A'</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.DNS.nslookup_A_record "Link to this definition")
        Perform nslookup for A records and return the parsed results.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **domain\_name** (*str*) – domain name to perform nslookup on

              - **opts** (*str*) – nslookup command line options

              - **extra\_opts** (*str*) – nslookup additional command line options

          - Returns<span class="colon">:</span>
            parsed nslookup results as dictionary

          - Return type<span class="colon">:</span>
            dict\[str, Any\]

<!-- end list -->

  - *<span class="pre">class</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">Firewall</span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall "Link to this definition")
    Linux iptables network firewall.

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">add\_drop\_rule\_ip6tables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid\_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.add_drop_rule_ip6tables "Link to this definition")
        Add drop rule to ip6tables.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **option** (*str*) – ip6tables command line options

              - **valid\_ip** (*str*) – ip to be blocked from device

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">add\_drop\_rule\_iptables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid\_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.add_drop_rule_iptables "Link to this definition")
        Add drop rule to iptables.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **option** (*str*) – iptables command line options, set -s for source and -d for destination

              - **valid\_ip** (*str*) – ip to be blocked from device

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">del\_drop\_rule\_ip6tables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid\_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.del_drop_rule_ip6tables "Link to this definition")
        Delete drop rule from ip6tables.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **option** (*str*) – ip6tables command line options

              - **valid\_ip** (*str*) – ip to be unblocked

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">del\_drop\_rule\_iptables</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">option</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">valid\_ip</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.del_drop_rule_iptables "Link to this definition")
        Delete drop rule from iptables.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **option** (*str*) – iptables command line options, set -s for source and -d for destination

              - **valid\_ip** (*str*) – ip to be unblocked

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">ip6tables\_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.ip6tables_list "Link to this definition")
        Return ip6tables rules as dictionary.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line arguments for ip6tables command

              - **extra\_opts** (*str*) – extra command line arguments for ip6tables command

          - Returns<span class="colon">:</span>
            ip6tables rules dictionary

          - Return type<span class="colon">:</span>
            dict\[str, list\[dict\]\]

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">iptables\_list</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.iptables_list "Link to this definition")
        Return iptables rules as dictionary.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line arguments for iptables command

              - **extra\_opts** (*str*) – extra command line arguments for iptables command

          - Returns<span class="colon">:</span>
            iptables rules dictionary

          - Return type<span class="colon">:</span>
            dict\[str, list\[dict\]\]

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">is\_6table\_empty</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.is_6table_empty "Link to this definition")
        Return True if ip6tables is empty.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line arguments for ip6tables command

              - **extra\_opts** (*str*) – extra command line arguments for ip6tables command

          - Returns<span class="colon">:</span>
            True if ip6tables is empty, False otherwise

          - Return type<span class="colon">:</span>
            bool

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">is\_table\_empty</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nvL</span> <span class="pre">--line-number'</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.Firewall.is_table_empty "Link to this definition")
        Return True if iptables is empty.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line arguments for iptables command

              - **extra\_opts** (*str*) – extra command line arguments for iptables command

          - Returns<span class="colon">:</span>
            True if iptables is empty, False otherwise

          - Return type<span class="colon">:</span>
            bool

<!-- end list -->

  - *<span class="pre">class</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">NwUtility</span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.NwUtility "Link to this definition")
    OneFW network utility.

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">netstat\_all\_tcp</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_all_tcp "Link to this definition")
        Get all UDP ports.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line options

              - **extra\_opts** (*str*) – extra command line options

          - Returns<span class="colon">:</span>
            parsed netstat output

          - Return type<span class="colon">:</span>
            DataFrame

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">netstat\_all\_udp</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_all_udp "Link to this definition")
        Get all udp ports.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line options

              - **extra\_opts** (*str*) – extra command line options

          - Returns<span class="colon">:</span>
            parsed netstat output

          - Return type<span class="colon">:</span>
            DataFrame

    <!-- end list -->

      - *<span class="pre">static</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">netstat\_listening\_ports</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">device\_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">type</span><span class="p"><span class="pre">\[</span></span><span class="pre">CableModem</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'-nlp'</span></span>*, *<span class="n"><span class="pre">extra\_opts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">DataFrame</span></span></span>[¶](#boardfarm3_docsis.use_cases.net_tools.NwUtility.netstat_listening_ports "Link to this definition")
        Get all listening ports.

          - Parameters<span class="colon">:</span>

              - **device\_type** (*Type\[CableModem\]*) – type of the device

              - **opts** (*str*) – command line options

              - **extra\_opts** (*str*) – extra command line options

          - Returns<span class="colon">:</span>
            parsed netstat output

          - Return type<span class="colon">:</span>
            DataFrame

</div>

</div>

<span id="document-snmp"></span>

<div id="snmp-use-cases" class="section">

## SNMP Use Cases[¶](#snmp-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.snmp" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.snmp "Link to this heading")

SNMP Use Cases.

  - <span class="sig-name descname"><span class="pre">get\_mib\_oid</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">device</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span>[¶](#boardfarm3_docsis.use_cases.snmp.get_mib_oid "Link to this definition")
    Return the Object Identifier (OID) for a given MIB.

      - Parameters<span class="colon">:</span>

          - **mib\_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

          - **device** (*CPE*) – CPE device instance

      - Returns<span class="colon">:</span>
        OID of the MIB

      - Return type<span class="colon">:</span>
        str

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">snmp\_bulk\_get</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">mib\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">non\_repeaters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">max\_repetitions</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">100</span></span>*, *<span class="n"><span class="pre">extra\_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">cmd\_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.snmp.snmp_bulk_get "Link to this definition")
    Perform SNMP BulkGet on the device with given arguments.

      - Parameters<span class="colon">:</span>

          - **board** (*CPE*) – CPE device instance

          - **wan** (*WAN*) – WAN device instance

          - **cmts** (*CMTS*) – CMTS device instance

          - **mib\_name** (*str*) – MIB name used to perform SNMP query

          - **index** (*int* *|* *None*) – index used along with mib\_name, defaults to None

          - **community** (*str*) – SNMP Community string, defaults to “private”

          - **non\_repeaters** (*int*) – value treated as get request, defaults to 0

          - **max\_repetitions** (*int*) – value treated as get next operation, defaults to 10

          - **retries** (*int*) – number of time commands are executed on exception, defaults to 3

          - **timeout** (*int*) – timeout in seconds, defaults to 100

          - **extra\_args** (*str*) – extra arguments to be passed in the command, defaults to “”

          - **cmd\_timeout** (*int*) – timeout to wait for command to give otuput

      - Returns<span class="colon">:</span>
        output of snmpbulkget command

      - Return type<span class="colon">:</span>
        list\[tuple\[str, str, str\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">snmp\_get</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra\_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd\_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.snmp.snmp_get "Link to this definition")
    SNMP Get board MIB from WAN device via SNMPv2.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify Nm Access IP value via SNMP Get

      - Verify the LLC filter rules removed for IPv4 via SNMP

      - Get the values of \[mib\_name\] via SNMP

    </div>

      - Parameters<span class="colon">:</span>

          - **mib\_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

          - **wan** (*WAN*) – WAN device instance

          - **board** (*CPE*) – CPE device instance

          - **cmts** (*CMTS*) – CMTS device instance

          - **index** (*int*) – MIB index, defaults to 0

          - **community** (*str*) – public/private, defaults to “private”

          - **extra\_args** (*str*) – see `man snmpget` for extra args, defaults to “”

          - **timeout** (*int*) – seconds, defaults to 10

          - **retries** (*int*) – number of retries, defaults to 3

          - **cmd\_timeout** (*int*) – timeout to wait for command to give otuput

      - Returns<span class="colon">:</span>
        value, type, full SNMP output

      - Return type<span class="colon">:</span>
        tuple\[str, str, str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">snmp\_set</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">stype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra\_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd\_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.snmp.snmp_set "Link to this definition")
    SNMP Set board MIB from WAN device via SNMPv2.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform SNMP Set operation on \[mib\_name\]

      - Reset the DUT using SNMP command

      - Set the values of \[mib\_name\] via SNMP

    </div>

      - Parameters<span class="colon">:</span>

          - **mib\_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

          - **value** (*str*) – value to be set.

          - **stype** (*str*) –

            defines the datatype of value to be set for mib\_name. One of the following values:

              - i: INTEGER,

              - u: unsigned INTEGER,

              - t: TIMETICKS,

              - a: IPADDRESS,

              - o: OBJID,

              - s: STRING,

              - x: HEX STRING,

              - d: DECIMAL STRING,

              - b: BITS

              - U: unsigned int64,

              - I: signed int64,

              - F: float,

              - D: double

          - **wan** (*WAN*) – WAN device instance

          - **board** (*CPE*) – CPE device instance

          - **cmts** (*CMTS*) – CMTS device instance

          - **index** (*int*) – MIB index, defaults to 0

          - **community** (*str*) – public/private, defaults to “private”

          - **extra\_args** (*str*) – see `man snmpset` for extra args, defaults to “”

          - **timeout** (*int*) – seconds, defaults to 10

          - **retries** (*int*) – number of retries, defaults to 3

          - **cmd\_timeout** (*int*) – timeout to wait for command to give otuput

      - Returns<span class="colon">:</span>
        value, type, full SNMP output

      - Return type<span class="colon">:</span>
        tuple\[str, str, str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">snmp\_walk</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">mib\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">wan</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">WAN</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*, *<span class="n"><span class="pre">cmts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CMTS</span></span>*, *<span class="n"><span class="pre">index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span>*, *<span class="n"><span class="pre">community</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'private'</span></span>*, *<span class="n"><span class="pre">extra\_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span>*, *<span class="n"><span class="pre">retries</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">3</span></span>*, *<span class="n"><span class="pre">cmd\_timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">30</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">tuple</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.snmp.snmp_walk "Link to this definition")
    SNMP Walk board MIB from WAN device via SNMPv2.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Do SNMP Walk on \[mib\_name\] MIB object on DUT

      - Perform SNMP Walk on DUT

    </div>

      - Parameters<span class="colon">:</span>

          - **mib\_name** (*str*) – MIB name. Will be searched in loaded MIB libraries.

          - **wan** (*WAN*) – WAN device instance

          - **board** (*CPE*) – CPE instance

          - **cmts** (*CMTS*) – CMTS device instance

          - **index** (*int*) – MIB index, defaults to 0

          - **community** (*str*) – public/private, defaults to “private”

          - **extra\_args** (*str*) – see `man snmpwalk` for extra args, defaults to “”

          - **timeout** (*int*) – seconds, defaults to 10

          - **retries** (*int*) – number of retries, defaults to 3

          - **cmd\_timeout** (*int*) – timeout to wait for command to give otuput

      - Returns<span class="colon">:</span>
        (dictionary of mib\_oid as key and tuple(mib value, mib type) as value, complete output)

      - Return type<span class="colon">:</span>
        tuple\[dict\[str, List\[str\]\], str\]

</div>

</div>

<span id="document-tr069"></span>

<div id="tr069-use-cases" class="section">

## TR069 Use Cases[¶](#tr069-use-cases "Link to this heading")

<div id="module-boardfarm3_docsis.use_cases.tr069" class="section">

<span id="from-boardfarm3-docsis"></span>

### from boardfarm3\_docsis[¶](#module-boardfarm3_docsis.use_cases.tr069 "Link to this heading")

TR-069 Use cases.

  - *<span class="pre">class</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">AddObjectResponse</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">response</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">object\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*<span class="sig-paren">)</span>[¶](#boardfarm3_docsis.use_cases.tr069.AddObjectResponse "Link to this definition")
    Store output of TR-069 AddObject RPC.

      - Raises<span class="colon">:</span>
        **UseCaseFailure** – in case of parsing errors

    <!-- end list -->

      - *<span class="pre">property</span><span class="w"> </span>*<span class="sig-name descname"><span class="pre">instance\_number</span></span>*<span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">int</span>*[¶](#boardfarm3_docsis.use_cases.tr069.AddObjectResponse.instance_number "Link to this definition")
        Store the Instance Number of the newly created Object.

        Once created, a Parameter or sub-object within this Object can be later referenced by using this Instance Number Identifier (defined in Section A.2.2.1) in the Path Name. The Instance Number assigned by the CPE is arbitrary.

        Note the fact that Instance Numbers are arbitrary means that they do not define a useful Object ordering, e.g. the ACS cannot assume that a newly created Object will have a higher Instance Number than its existing sibling Objects.

          - Returns<span class="colon">:</span>
            instance number

          - Return type<span class="colon">:</span>
            int

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">Download</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filetype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">targetfilename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filesize</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">username</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">password</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">commandkey</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">delayseconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">successurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">failureurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.Download "Link to this definition")
    Perform TR-069 RPC call Download.

    This method is used by the ACS to cause the CPE to download a specified file from the designated location.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute Download RPC via ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **url** (*str*) – specifies the source file location. HTTP and HTTPS transports MUST be supported

          - **filetype** (*str*) – An integer followed by a space followed by the file type description. Only the following values are currently defined for the FileType argument: 1. Firmware Upgrade Image 2. Web Content 3. Vendor Configuration File 4. Tone File 5. Ringer File 6. Stored Firmware Image

          - **targetfilename** (*str*) – The name of the file to be used on the target file system.

          - **filesize** (*int*) – The size of the file to be downloaded in bytes

          - **username** (*str*) – Username to be used by the CPE to authenticate with the file server

          - **password** (*str*) – Password to be used by the CPE to authenticate with the file server

          - **commandkey** (*str*) – The string the CPE uses to refer to a particular download

          - **delayseconds** (*int*) – This argument has different meanings for Unicast and Multicast downloads

          - **successurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes successfully

          - **failureurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes unsuccessfully

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        Return the list of Dictionary containing the keys Status,StartTime and CompleteTime

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">GPA</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.GPA "Link to this definition")
    Perform TR-069 RPC call GetParameterAttributes.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute GetParameterAttributes RPC

      - Execute GPA RPC

      - Execute GPA on param

    </div>

      - Parameters<span class="colon">:</span>

          - **param** (*str*) – name of the parameter

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        list of dictionary with keys Name, AccessList, Notification indicating the attributes of the parameter

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">GPN</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param\_path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">next\_level</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">120</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.GPN "Link to this definition")
    Perform TR-069 RPC call GetParametersName.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - GPN of \[\]

      - GetParameterNames RPC

    </div>

      - Parameters<span class="colon">:</span>

          - **param\_path** (*str*) – name of the parameter

          - **next\_level** (*bool*) – If false, the response MUST contain the Parameter or Object whose name exactly matches the ParameterPath argument

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

          - **timeout** (*int*) – Timeout for the GPN RPC call, defaults to 120

      - Returns<span class="colon">:</span>
        list of dictionary with key, type and value

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">GPV</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.GPV "Link to this definition")
    Perform TR-069 RPC call GetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute GetParameterValues RPC by providing param name

      - Perform GPV on parameter

      - using GPV via ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        GPV(params=["param1", "param2"])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **params** (*str* *|* *list\[str\]*) – List of parameters

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        List of dict of Param,Value pairs

      - Return type<span class="colon">:</span>
        List\[RPCOutput\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">GetRPCMethods</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.GetRPCMethods "Link to this definition")
    Perform TR-069 RPC call GetRPCMethods.

      - Parameters<span class="colon">:</span>

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        list of all the RPC methods

      - Return type<span class="colon">:</span>
        List\[str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">Reboot</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">command\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.Reboot "Link to this definition")
    Perform TR-069 RPC call Reboot.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform reboot on DUT

      - Reboot the DUT

      - Execute Reboot RPC from ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **command\_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE reboots and calls the Inform method.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Raises<span class="colon">:</span>
        **UseCaseFailure** – in case of board not online after reset

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">SPA</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">notification\_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access\_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access\_list</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.SPA "Link to this definition")
    Perform TR-069 RPC call SetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute SetParameterAttributes RPC

      - Execute SPA RPC by providing ParameterName

      - Perform SPA on

    </div>

    Example usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        SPA([{"Device.WiFi.SSID.1.SSID": "1"}], True, False, [])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **param** (*list\[dict\[str,* *str\]\]* *|* *dict\[str,* *str\]*) – parameter as key of dictionary and notification as its value

          - **notification\_change** (*bool*) – If true, the value of Notification replaces the current notification setting for this Parameter or group of Parameters. If false, no change is made to the notification setting

          - **access\_change** (*bool*) – If true, the value of AccessList replaces the current access list for this Parameter or group of Parameters. If false, no change is made to the access list.

          - **access\_list** (*list*) – Array of zero or more entities for which write access to the specified Parameter(s) is granted

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">SPV</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.SPV "Link to this definition")
    Perform TR-069 RPC call SetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform SetParameterValues RPC by providing parameter

      - Execute SPV RPC by providing parameter name

      - Execute SPV from ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        SPV(params=[{"param1": "value1"}, {"param2": 123}])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **params** (*list\[dict\[str,* *Any\]\]*) – Dict or list of Dict\[parameters, values\]

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        List of dict of Param,Value pairs

      - Return type<span class="colon">:</span>
        int

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">ScheduleInform</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">delay\_seconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">command\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.ScheduleInform "Link to this definition")
    Perform TR-069 RPC call ScheduleInform.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute ScheduleInform RPC from ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **delay\_seconds** (*int*) – The number of seconds from the time this method is called to the time the CPE is requested to initiate a one-time Inform method call

          - **command\_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE calls the Inform method.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">add\_object</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">object\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">parameter\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint">[<span class="pre">AddObjectResponse</span>](index.html#boardfarm3_docsis.use_cases.tr069.AddObjectResponse "boardfarm3_docsis.use_cases.tr069.AddObjectResponse")</span></span>[¶](#boardfarm3_docsis.use_cases.tr069.add_object "Link to this definition")
    Perform TR-069 RPC call AddObject.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute AddObject RPC by providing parameter name

      - Add the \[\] entry by Add object from ACS

      - Add new instance to \[\] by Add object from ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        out = add_object(object_name)
        instance_number = out.instance_number
        response = out.response

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **object\_name** (*str*) – Name of the object to be added

          - **parameter\_key** (*str* *|* *None*) – The optional string value to set the ParameterKey.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        AddObjectResponse with values response & instance\_number

      - Return type<span class="colon">:</span>
        [AddObjectResponse](index.html#boardfarm3_docsis.use_cases.tr069.AddObjectResponse "boardfarm3_docsis.use_cases.tr069.AddObjectResponse")

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">del\_object</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">object\_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">parameter\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.del_object "Link to this definition")
    Perform TR-069 RPC call DeleteObject.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Delete the \[\] entry using Delete Object RPC from ACS

      - Login to ACS and delete

      - Execute DeleteObject RPC from ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        del_object(object_name)

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **object\_name** (*str*) – Name of the object to be added

          - **parameter\_key** (*str* *|* *None*) – The optional string value to set the ParameterKey.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        delete object response value

      - Return type<span class="colon">:</span>
        int

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">download</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filetype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">targetfilename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">filesize</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">username</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">password</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">commandkey</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">delayseconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">successurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">failureurl</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.download "Link to this definition")
    Perform TR-069 RPC call Download.

    This method is used by the ACS to cause the CPE to download a specified file from the designated location.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute Download RPC via ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **url** (*str*) – specifies the source file location. HTTP and HTTPS transports MUST be supported

          - **filetype** (*str*) – An integer followed by a space followed by the file type description. Only the following values are currently defined for the FileType argument: 1. Firmware Upgrade Image 2. Web Content 3. Vendor Configuration File 4. Tone File 5. Ringer File 6. Stored Firmware Image

          - **targetfilename** (*str*) – The name of the file to be used on the target file system.

          - **filesize** (*int*) – The size of the file to be downloaded in bytes

          - **username** (*str*) – Username to be used by the CPE to authenticate with the file server

          - **password** (*str*) – Password to be used by the CPE to authenticate with the file server

          - **commandkey** (*str*) – The string the CPE uses to refer to a particular download

          - **delayseconds** (*int*) – This argument has different meanings for Unicast and Multicast downloads

          - **successurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes successfully

          - **failureurl** (*str*) – this argument contains the URL, the CPE should redirect the user’s browser to if the download completes unsuccessfully

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        Return the list of Dictionary containing the keys Status,StartTime and CompleteTime

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">factory\_reset</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.factory_reset "Link to this definition")
    Perform TR-069 FactoryReset RPC call and guarantee the board is back online.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Factory Reset the DUT

      - Perform factory reset on the CPE

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        factory_reset()

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Raises<span class="colon">:</span>
        **UseCaseFailure** – in case of board not online after reset

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_ccsptr069\_pid</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.get_ccsptr069_pid "Link to this definition")
    Return the CcspTr069PaSsp process id.

      - Parameters<span class="colon">:</span>
        **board** (*CPE*) – The CPE device instance

      - Returns<span class="colon">:</span>
        The pid of CcspTr069PaSsp process

      - Return type<span class="colon">:</span>
        int | None

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_parameter\_attributes</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.get_parameter_attributes "Link to this definition")
    Perform TR-069 RPC call GetParameterAttributes.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute GetParameterAttributes RPC

      - Execute GPA RPC

      - Execute GPA on param

    </div>

      - Parameters<span class="colon">:</span>

          - **param** (*str*) – name of the parameter

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        list of dictionary with keys Name, AccessList, Notification indicating the attributes of the parameter

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_parameter\_names</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param\_path</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">next\_level</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">timeout</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">120</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.get_parameter_names "Link to this definition")
    Perform TR-069 RPC call GetParametersName.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - GPN of \[\]

      - GetParameterNames RPC

    </div>

      - Parameters<span class="colon">:</span>

          - **param\_path** (*str*) – name of the parameter

          - **next\_level** (*bool*) – If false, the response MUST contain the Parameter or Object whose name exactly matches the ParameterPath argument

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

          - **timeout** (*int*) – Timeout for the GPN RPC call, defaults to 120

      - Returns<span class="colon">:</span>
        list of dictionary with key, type and value

      - Return type<span class="colon">:</span>
        list\[dict\[str, Any\]\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_parameter\_values</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.get_parameter_values "Link to this definition")
    Perform TR-069 RPC call GetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute GetParameterValues RPC by providing param name

      - Perform GPV on parameter

      - using GPV via ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        GPV(params=["param1", "param2"])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **params** (*str* *|* *list\[str\]*) – List of parameters

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        List of dict of Param,Value pairs

      - Return type<span class="colon">:</span>
        List\[RPCOutput\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">get\_rpc\_methods</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.get_rpc_methods "Link to this definition")
    Perform TR-069 RPC call GetRPCMethods.

      - Parameters<span class="colon">:</span>

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        list of all the RPC methods

      - Return type<span class="colon">:</span>
        List\[str\]

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">is\_dut\_online\_on\_acs</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.is_dut_online_on_acs "Link to this definition")
    Check if the DUT is online on ACS.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Verify the DUT registration status on the ACS

      - Make sure that DUT is registered on the ACS.

    </div>

      - Parameters<span class="colon">:</span>

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        True if devices is registered with ACS and GPV is successful for Device.DeviceInfo.SoftwareVersion, else False

      - Return type<span class="colon">:</span>
        bool

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">reboot</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">command\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.reboot "Link to this definition")
    Perform TR-069 RPC call Reboot.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform reboot on DUT

      - Reboot the DUT

      - Execute Reboot RPC from ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **command\_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE reboots and calls the Inform method.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Raises<span class="colon">:</span>
        **UseCaseFailure** – in case of board not online after reset

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">restart\_tr069\_agent</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.restart_tr069_agent "Link to this definition")
    Restart the TR-069 agent by killing the process based on the PID.

      - Parameters<span class="colon">:</span>
        **board** (*CPE*) – CPE device instance

      - Raises<span class="colon">:</span>
        **ValueError** – when the CcspTr069PaSsp is not alive

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">schedule\_inform</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">delay\_seconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span>*, *<span class="n"><span class="pre">command\_key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.schedule_inform "Link to this definition")
    Perform TR-069 RPC call ScheduleInform.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute ScheduleInform RPC from ACS

    </div>

      - Parameters<span class="colon">:</span>

          - **delay\_seconds** (*int*) – The number of seconds from the time this method is called to the time the CPE is requested to initiate a one-time Inform method call

          - **command\_key** (*str*) – The string to return in the CommandKey element of the InformStruct when the CPE calls the Inform method.

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">set\_parameter\_attributes</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">param</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">notification\_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access\_change</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span>*, *<span class="n"><span class="pre">access\_list</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.set_parameter_attributes "Link to this definition")
    Perform TR-069 RPC call SetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Execute SetParameterAttributes RPC

      - Execute SPA RPC by providing ParameterName

      - Perform SPA on

    </div>

    Example usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        SPA([{"Device.WiFi.SSID.1.SSID": "1"}], True, False, [])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **param** (*list\[dict\[str,* *str\]\]* *|* *dict\[str,* *str\]*) – parameter as key of dictionary and notification as its value

          - **notification\_change** (*bool*) – If true, the value of Notification replaces the current notification setting for this Parameter or group of Parameters. If false, no change is made to the notification setting

          - **access\_change** (*bool*) – If true, the value of AccessList replaces the current access list for this Parameter or group of Parameters. If false, no change is made to the access list.

          - **access\_list** (*list*) – Array of zero or more entities for which write access to the specified Parameter(s) is granted

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

<!-- end list -->

  - <span class="sig-name descname"><span class="pre">set\_parameter\_values</span></span><span class="sig-paren">(</span>*<span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">\[</span></span><span class="pre">dict</span><span class="p"><span class="pre">\[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">\]</span></span><span class="p"><span class="pre">\]</span></span></span>*, *<span class="n"><span class="pre">acs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ACS</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*, *<span class="n"><span class="pre">board</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">CPE</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span>*<span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span>[¶](#boardfarm3_docsis.use_cases.tr069.set_parameter_values "Link to this definition")
    Perform TR-069 RPC call SetParameterValues.

    <div class="admonition hint">

    Hint

    This Use Case implements statements from the test suite such as:

      - Perform SetParameterValues RPC by providing parameter

      - Execute SPV RPC by providing parameter name

      - Execute SPV from ACS

    </div>

    Usage:

    <div class="highlight-python notranslate">

    <div class="highlight">

        SPV(params=[{"param1": "value1"}, {"param2": 123}])

    </div>

    </div>

      - Parameters<span class="colon">:</span>

          - **params** (*list\[dict\[str,* *Any\]\]*) – Dict or list of Dict\[parameters, values\]

          - **acs** (*ACS* *|* *None*) – ACS server that will perform GPV

          - **board** (*CPE* *|* *None*) – CPE on which to perform TR-069 method

      - Returns<span class="colon">:</span>
        List of dict of Param,Value pairs

      - Return type<span class="colon">:</span>
        int

</div>

</div>

</div>

</div>

<div class="clearer">

</div>

</div>

</div>

</div>

<div id="show_right_sidebar">

[<span class="icon">\<</span><span>Page contents</span>](#)

</div>

<div id="right_sidebar">

[<span class="icon">\></span><span>Page contents:</span>](#)

<div class="page_toc">

<span class="caption-text">Use Cases</span>

  - [Connectivity Use Cases](#document-connectivity)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.connectivity)
  - [Docsis Use Cases](#document-docsis)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.docsis)
  - [Erouter Use Cases](#document-erouter)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.erouter)
  - [Net\_tools Use Cases](#document-net_tools)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.net_tools)
  - [SNMP Use Cases](#document-snmp)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.snmp)
  - [TR069 Use Cases](#document-tr069)
      - [from boardfarm3\_docsis](index.html#module-boardfarm3_docsis.use_cases.tr069)

</div>

</div>

<div class="clearer">

</div>

</div>

<div class="button_nav_wrapper">

<div class="button_nav">

<div class="left">

</div>

<div class="right">

</div>

</div>

</div>

<div class="footer" role="contentinfo">

© Copyright 2025, Various. Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.

</div>

Styled using the [Piccolo Theme](https://github.com/piccolo-orm/piccolo_theme)
