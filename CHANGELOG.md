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
