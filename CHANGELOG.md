## 1.0.0 (2025-09-15)

### BREAKING CHANGE

- BOARDFARM-2018
- BOARDFARM-1786
- BOARDFARM-1610
- BOARDFARM-1610
- BOARDFARM-3531
- BOARDFARM-3531

### Feat

- depends on boardfarm3==2025.*
- **use_cases/snmp**: implementation
- **use_cases/net_tools**: implementation
- **use_cases/erouter**: implementation
- **use_cases/tr069**: implementation
- **use_cases/connectivity**: implementation
- **use_cases/docsis**: add implementation
- **templates/cable_modem**: add ABCs for DOCSIS modems
- **isc_provisioner**: changing mv command to cat
- update pyproject version
- **isc_provisioner**: add dhcp snooping logic
- **boardfarm3_docsis/**: added device class changes for nw utility
- **devices/isc_provisioner.py,-templates/provisioner.py**: added property
- **devices/isc_provisioner.py,-templates/provisioner.py**: added property
- **devices**: add async skip boot flow for isc provisioner and mini cmts
- **noxfile.py**: update noxfile to python 3.11
- **devices/minicmts.py,templates/cmts.py**: add cm channel method
- **templates/cmts.py**: add abstract method to get upstream channel value
- **devices/minicmts.py**: add method to return active upstream channel value
- **devices/minicmts.py**: retrieve downstream channel value
- **templates/cmts.py**: add abstract method to get downstream channel value
- encode mta with -eu (excentis sha1)
- **templates/cmts.py,devices/minicmts.py**: add abstract methods and implementation to check docsis version
- **lib/docsis_encoder.py**: save console logs to disk
- **devices.isc_provisioner.py**: add contingency checks for isc provisioner
- add docsis mta compilation
- **cmts**: get cpe mta ipv4 address
- add mta provisioning
- add get_ertr_ipv(4/6) methods
- add mta to provisioner signature
- add clear_cm_reset to cmts
- **minicmts.py,cmts.py**: add method to get ip routes from quagga router
- **devices,templates**: add get_cmts_ip_bundle and get_provision_mode api's
- **POM**: add data needed by GUI tests to CM template
- preparing master to port boardfarm3
- **topvision_cmts.py**: add ser2net connectivity for topvision cmts
- **topvision_cmts.py**: add remove file method
- flash image with no shell
- **devices/arris_cmts.py,-devices/topvision_cmts.py**: add method to get active upstream channel value
- **devices/arris_cmts.py**: retrieve the downstream channel value
- **devices/topvision_cmts.py**: retrieve downstream channel value
- **base_devices/cmts_template.py,-devices/topvision_cmts.py**: add abstract method and implementation for docsis version in v2

### Fix

- **boardfarm3_docsis**: add start and stop tcpdump
- **connectivity.py**: change use case signature
- **boardfarm3_docsis**: move usecases
- **pre-commit**: stick to flynt v1.0.3
- add documentation and readme for docsis usecases
- **boardfarm3_docsis/devices/isc_provisioner.py**: fixed dhcpd conf generation
- **boardfarm-docsis/.pylintrc**: pylint py version change to 3.11
- **CMTS**: inherit from LTS template
- **.vscode**: update ruff settings
- **minicmts**: add retry for interact
- **boardfarm3_docsis/devices/minicmts.py**: add fix
- **devices/isc_provisioner.py**: add resource name to skip boot
- workaround cmts disconnect error
- **isc_provisioner.py**: fetch boardname from config instead of command line args
- **boardfarm3_docsis/devices/minicmts.py**: add fix
- **boardfarm3_docsis/devices/minicmts.py**: add connect and run
- **isc_provisioner.py**: PD assignment from PD list according to station id
- **isc_provisioner,docsis_encoder**: support sku without voice feature
- **isc_provisioner.py**: Updating PD length to /60 from /56
- update dependencies version
- **boardfarm3_docsis/**: compatibility for packet capture
- remove the warning on delim_whitespace
- pin nox pylint==3.2.6
- **minicmts.py**: use aysnc to login into server
- **minicmts.py:cmts.py**: router impl for tcpdump
- **isc_provisioner.py**: add station number attr
- **provisioner.py**: provisioner class inheriting base provisioner
- **boardfarm3_docsis/**: added iface_dut property
- **isc_dhcp**: limit pool size to 10 addresses
- use bootfile name for ipv6 provisioning
- **isc**: exctract name from bootfile path
- **minicmts**: restore logic modified by linter process
- **minicmts.py**: is_cable_modem_online() ignore_bpi
- **minicmts**: add login step
- **isc_provisioner.py,-minicmts.py**: add skip boot hookimpl for provisioner and minicmts
- **boardfarm3_docsis/devices/minicmts.py**: allow console interaction with the cmts
- **minicmts**: the cmts is not a linux device
- **.pylintrc**: update .pylintrc file to fix warnings
- change gitlab to github
- **minicmts.py,cmts.py**: reduce duplicate code and fix docstring
- **pyproject.toml**: fix plugin path
- do not skip the 1st cm
- **axiros_acs.py**: get tr69 cpe-id from board
- remove yaml formatters
- **base_devices/cmts_template.py**: increase rety time for cmts check
- **devices/docsis,lib/docsis**: support sku with no voice support
- **booting.py**: aftr device class impl
- **base_devices/cmts_template.py**: increase cm online check time
- **devices/topvision_cmts.py**: add fallback  when cmts is stuck in enable
- **lib/booting_utils.py**: correct register fxs details util
- **topvision_cmts**: enter password on enable cmd
- **use_cases/provision_helper.py**: fix Use Case
- **boardfarm_docsis**: allow boot for no shell images
- **use_cases/boot_file_helper.py**: add dslite and tr69 params to bootfile
- **docsis**: randomize image name for snmp flash
- fix unittests and linting errors for python3.11
- flake8 ignore  B028, B017
- **boardfarm_docsis/lib/voice.py**: change lan obj to fxs
- **hooks:contingency_checks.py**: update voice cc checks for fxs instead of lan
- **lib/dns_helper.py**: fix dns_acs_config
- **use_cases/provision_helper.py**: add missing args
- change gitlab to github
- **booting.py**: alter voice device list for configuration
- **lib:env_helper.py**: update based on the correction in json schema
- **lib:env_helper.py**: add lan dhcpv4 check for tr-069 spv provisioning
- **lib/env_helper.py**: correct the string
- **topvision**: update BPI checks
- **lib/env_helper.py**: update dhcp enable param

### Refactor

- update save_console_logs
- introduce ruff linter
- **pre-commit-config.yaml**: update isort version
- update syntax to py3.9
- **py.typed**: add py.typed file to indicate the package is type hinted
- remove tox.ini
- **docsis_cable_modem.py,cable_modem.py**: remove unused code after cable modem class refactoring with sw and hw
- **devices,plugins**: boardfarm v3 docsis devices and plugins
- **lib,devices,tests**: cleanup boardfarm-docsis for v3
- update flash_meta signature
- **base_devices/cmts_template.py**: remove the abstract methods from the template
- **use_cases/boot_file_helper.py**: refcator the Use Case switch_erouter_mode to add LLC filters
- **use_cases/boot_file_helper.py**: refactor the Use Case switch_erotuer_mode as the same available in v3
- **use_cases/boot_file_helper.py**: refactor the method add_tlvs to accpet config file as param
- **use_cases/boot_file_helper.py**: refactor the Use Case switch_erotuer_mode to add LLCfilters
- related to mv1cs booting dev firmware
- **pre-commit-config.yaml**: update isort version
- **use_cases/provision_helper.py**: add configure bootfile

## 2022.35.0 (2022-08-31)

### Feat

- **use_cases/cmts**: allow CMTS to be passed as parameter for is_route_present_on_cmts()
- **booting.py**: add securing sam url check

### Fix

- **unittests/boardfarm/devices/__init__.py**: fn expects positional arguments
- **unittests/boardfarm/orchestration.py**: remove file with error

### Refactor

- **use_cases/ripv2**: address docstring and type hinting issues
- **use_cases/cmts**: Fix type hinting

## 2022.33.0 (2022-08-17)

## 2022.31.0 (2022-08-03)

## 2022.29.0 (2022-07-20)

### Fix

- **ripv2.py**: add fix for frame time

## 2022.27.0 (2022-07-07)

### BREAKING CHANGE

- Related to BOARDFARM-2075

### Fix

- related to wifi board fail at post boot

## 2022.25.0 (2022-06-20)

### Feat

- **pylint**: bump pylint to 2.14.1

## 2022.23.0 (2022-06-08)

### Fix

- **devices:topvision_cmts.py**: fix _get_cmts_ip_bundle to use connect_and_run

## 2022.21.0 (2022-05-25)

### Feat

- **use_cases:boot_file_helper.py**: add a usecase to fetch vendor identifier from bootfile

### Fix

- **ripv2.py**: add fix for empty values
- **cBR8_cmts**: add ip route method

## 2022.19.0 (2022-05-11)

### Refactor

- **boardfarm_docsis:lib:env_helper.py**: segregate docsis and non-docsis env_helper

## 2022.17.0 (2022-04-28)

### Feat

- **booting.py,booting_utils.py,env_helper.py**: add support to set static ip for lan/wlan clients
- **lib/env_helper.py,-use_cases/software_update.py**: add methods to get alternative software properties from env
- **lib:hooks:contingency_checks.py**: Contingency Check Functionality Segregation

### Fix

- **software_update.py**: modify the singleton snmp class to pick the ipv4 CM IP always

### Refactor

- **boardfarm_docsis:use_cases**: move usecases out of boardfarm-docsis

## 2022.15.0 (2022-04-14)

### BREAKING CHANGE

- Depends-on: I6c67cd2828257eec3c1818c9eae3366021d7c660

### Feat

- update api to resolve board type

### Fix

- remove yamlfmt/yamllint from pre-commit
- **use_cases:software_update.py**: fix use case generate_bootfile_with_docsis_mibs
- **pre-commit**: update pre-commit hooks to latest versions and autofix issues
- boot_board unittest fix

## 2022.13.0 (2022-03-31)

### Feat

- **use_cases/acs.py**: implement usecases for GPA and SPA
- **cmts.py,-ripv2.py**: add new usecases for ripv2
- **booting.py,-env_helper.py**: add support to configure invalid dhcp gateway ip

### Fix

- **acs.py**: update method call to sw object
- **provision_helper.py**: access provisioning messages via sw board object

## 2022.11.0 (2022-03-16)

### Feat

- **use_cases:software_update.py**: implement software update usecases
- add usecase to modify boot file

## 2022.09.0 (2022-03-02)

### BREAKING CHANGE

- BOARDFARM-1714

### Feat

- **acs.py**: add factory_reset usecase
- **cmts-device-classes**: add tcpdump support to cmts device classes

### Fix

- remove get_cmts_type() from CMTS public API
- retry getting the cable modem ip

## 2022.07.0 (2022-02-16)

### Feat

- **base_cmts.py**: remove base cmts class as its not used anymore
- **cmts-router-device-class**: add device class for mini cmts router update cmts classes
- **casa_cmts.py**: inherit cmts_template and refactor
- **cmts_template.py**: topvision class use cmts template

### Fix

- **erouter.py**: update exception handling to parent class pexpect.TIMEOUT
- retry connecting on failure

## 2022.05.0 (2022-02-02)

### Fix

- **use_cases:online_usecases.py**: revert the workaround added for OFW-2175 as it is fixed
- **erouter.py**: fix a typo, update type hint
- retries on cmts connection failure

## 2022.03.0 (2022-01-20)

### BREAKING CHANGE

- This is related to the changes added to allowd legacy CBN to boot from
a OFw build.

### Feat

- **acs.py**: add usecases add_object and del_object
- use env_helper.get_image instead of _get_image

### Fix

- **erouter.py**: modify get_erouter_addresses use case to return link local IPv6 address as well

## 2022.01.0 (2022-01-05)

### BREAKING CHANGE

- Needs boardfarm_docsis commit for docsis devices

### Feat

- overrides env_helper.get_image
- add manufacturer and hardware_version properties to board object

### Fix

- **docsis.py,booting.py**: change post boot lan conditions

## 2021.51.0 (2021-12-22)

### Fix

- **pylint**: Add pylint to pre-commit. Fix pylint issues.
- **boardfarm_docsis:use_cases:online_usecases.py**: add a workaround to check ipiptun0 interface after DUT boot
- **booting.py,-online_usecases.py**: moved wait_for_board into device specific finalize board function
- Remove TypedDict until we upgrade to python >3.8
- **use_cases:provision_helper.py**: fix the reprovision_board usecase to reboot after reprovisioning

## 2021.49.0 (2021-12-09)

### Feat

- **acs**: add spv and gpv use cases
- **provision_helper.py**: add use cases for verifcation of cfg file download/apply process
- **board.py**: add the provisioning_messages property under DocsisCPESw
- **erouter.py**: Add board use cases to verify erouter status
- **acs.py**: Create use case for ACS connectivity check

### Fix

- **use_cases:online_usecases.py**: add post_boot_env in use cases to set the default password after boot

### Refactor

- Inherit DocsisCPESw from BoardSwtemplate

## 2021.47.0 (2021-11-24)

### Feat

- **board,mta_template**: allow FXO template derivate for docsis
- http default proto for snmp SW download
- **online_usecases**: add check board online after reset usecase
- **devices/base_devices/board.py**: adds pre_flash_factory_reset

### Fix

- board not online on cmts
- tr69provisioning fix for pre_flash_factory_reset
- **lib/voice.py**: modify the cleanup_voice_prompt method
- remove check based on customer id in bootfile
- **online_usecases**: add board boot started check
- **online_usecases**: add post boot checks
- **lib/docsis.py**: Tolerate IPv6tun0 taking around 15 minutes in boot
- **devices/docsis.py**: uses mgmt to fetch the build
- fix pylint errors
- Replace parser delimiter regex with native flag

### Refactor

- prov helper usecase class to functions
- **base_devices/board.py**: removes unnecessary code
- change lib to docsis_lib globally
