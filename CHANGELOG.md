## 2025.05.0 (2025-01-29)

## 2025.03.0 (2025-01-15)

### Fix

- **devices/docsis,lib/docsis**: support sku with no voice support

## 2025.01.0 (2025-01-02)

## 2024.51.0 (2024-12-18)

## 2024.49.0 (2024-12-04)

### Fix

- **booting.py**: aftr device class impl

## 2024.45.0 (2024-11-06)

## 2024.43.0 (2024-10-23)

## 2024.41.0 (2024-10-10)

### Fix

- **base_devices/cmts_template.py**: increase cm online check time

## 2024.39.0 (2024-09-26)

## 2024.37.0 (2024-09-12)

## 2024.35.0 (2024-08-28)

## 2024.33.0 (2024-08-14)

### Fix

- **devices/topvision_cmts.py**: add fallback  when cmts is stuck in enable

## 2024.31.0 (2024-08-01)

## 2024.29.0 (2024-07-18)

### Fix

- **lib/booting_utils.py**: correct register fxs details util

## 2024.27.0 (2024-07-03)

## 2024.25.0 (2024-06-20)

## 2024.23.0 (2024-06-05)

## 2024.22.0 (2024-05-27)

## 2024.20.0 (2024-05-14)

### Fix

- **topvision_cmts**: enter password on enable cmd

## 2024.17.0 (2024-04-26)

## 2024.16.0 (2024-04-15)

## 2024.13.0 (2024-03-27)

### Feat

- **topvision_cmts.py**: add ser2net connectivity for topvision cmts
- **topvision_cmts.py**: add remove file method

## 2024.11.0 (2024-03-14)

## 2024.09.0 (2024-02-28)

## 2024.07.0 (2024-02-15)

## 2024.05.0 (2024-02-01)

## 2024.04.0 (2024-01-22)

### Fix

- **use_cases/provision_helper.py**: fix Use Case

## 2023.50.0 (2023-12-12)

### Fix

- **boardfarm_docsis**: allow boot for no shell images

## 2023.45.0 (2023-11-08)

## 2023.43.0 (2023-10-24)

## 2023.42.0 (2023-10-16)

### BREAKING CHANGE

- BOARDFARM-3531
- BOARDFARM-3531

### Feat

- flash image with no shell

### Fix

- **use_cases/boot_file_helper.py**: add dslite and tr69 params to bootfile

### Refactor

- update flash_meta signature

## 2023.39.0 (2023-09-29)

### Feat

- **devices/arris_cmts.py,-devices/topvision_cmts.py**: add method to get active upstream channel value

## 2023.37.0 (2023-09-13)

### Feat

- **devices/arris_cmts.py**: retrieve the downstream channel value
- **devices/topvision_cmts.py**: retrieve downstream channel value

## 2023.36.0 (2023-09-04)

### Refactor

- **base_devices/cmts_template.py**: remove the abstract methods from the template

## 2023.33.0 (2023-08-18)

## 2023.29.0 (2023-07-20)

### Refactor

- **use_cases/boot_file_helper.py**: refcator the Use Case switch_erouter_mode to add LLC filters
- **use_cases/boot_file_helper.py**: refactor the Use Case switch_erotuer_mode as the same available in v3

## 2023.27.0 (2023-07-05)

### Refactor

- **use_cases/boot_file_helper.py**: refactor the method add_tlvs to accpet config file as param
- **use_cases/boot_file_helper.py**: refactor the Use Case switch_erotuer_mode to add LLCfilters

## 2023.25.0 (2023-06-23)

## 2023.23.0 (2023-06-07)

## 2023.21.0 (2023-05-24)

### Fix

- **docsis**: randomize image name for snmp flash

### Refactor

- related to mv1cs booting dev firmware

## 2023.17.0 (2023-04-26)

## 2023.16.0 (2023-04-17)

### Feat

- **base_devices/cmts_template.py,-devices/topvision_cmts.py**: add abstract method and implementation for docsis version in v2

## 2023.13.0 (2023-03-30)

### Fix

- fix unittests and linting errors for python3.11

## 2023.11.0 (2023-03-15)

## 2023.09.0 (2023-03-02)

## 2023.08.0 (2023-02-20)

## 2023.05.0 (2023-02-03)

### Refactor

- **pre-commit-config.yaml**: update isort version

## 2023.03.0 (2023-01-18)

### Fix

- flake8 ignore  B028, B017
- **boardfarm_docsis/lib/voice.py**: change lan obj to fxs

## 2022.51.0 (2022-12-21)

## 2022.49.0 (2022-12-07)

### Fix

- **hooks:contingency_checks.py**: update voice cc checks for fxs instead of lan
- **lib/dns_helper.py**: fix dns_acs_config

## 2022.47.0 (2022-11-23)

### Fix

- **use_cases/provision_helper.py**: add missing args
- change gitlab to github
- **booting.py**: alter voice device list for configuration
- **lib:env_helper.py**: update based on the correction in json schema

## 2022.45.0 (2022-11-09)

### Fix

- **lib:env_helper.py**: add lan dhcpv4 check for tr-069 spv provisioning

## 2022.43.0 (2022-10-28)

### Fix

- **lib/env_helper.py**: correct the string

### Refactor

- **use_cases/provision_helper.py**: add configure bootfile

## 2022.41.0 (2022-10-12)

### Fix

- **topvision**: update BPI checks

## 2022.39.0 (2022-09-28)

### Fix

- **lib/env_helper.py**: update dhcp enable param

## 2022.37.0 (2022-09-21)

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
