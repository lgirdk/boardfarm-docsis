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

### Fix

- remove get_cmts_type() from CMTS public API
- retry getting the cable modem ip

### BREAKING CHANGE

- BOARDFARM-1714

### Feat

- **acs.py**: add factory_reset usecase
- **cmts-device-classes**: add tcpdump support to cmts device classes

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

### Feat

- **acs.py**: add usecases add_object and del_object
- use env_helper.get_image instead of _get_image

### BREAKING CHANGE

- This is related to the changes added to allowd legacy CBN to boot from
a OFw build.

### Fix

- **erouter.py**: modify get_erouter_addresses use case to return link local IPv6 address as well

## 2022.01.0 (2022-01-05)

### Feat

- overrides env_helper.get_image
- add manufacturer and hardware_version properties to board object

### BREAKING CHANGE

- Needs boardfarm_docsis commit for docsis devices

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

### Refactor

- Inherit DocsisCPESw from BoardSwtemplate

### Fix

- **use_cases:online_usecases.py**: add post_boot_env in use cases to set the default password after boot

## 2021.47.0 (2021-11-24)

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

### Feat

- **board,mta_template**: allow FXO template derivate for docsis
- http default proto for snmp SW download
- **online_usecases**: add check board online after reset usecase
- **devices/base_devices/board.py**: adds pre_flash_factory_reset

### Refactor

- prov helper usecase class to functions
- **base_devices/board.py**: removes unnecessary code
- change lib to docsis_lib globally
