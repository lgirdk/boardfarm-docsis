import logging

import pytest
from boardfarm.exceptions import BftEnvMismatch

from boardfarm_docsis.lib.env_helper import DocsisEnvHelper

logger = logging.getLogger("bft")


class TestEnvHelper:

    environments = [
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {},
                    }
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {  # this is empty in the env_helper
                            "vendor_specific": {
                                "component": "eRouter",
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    }
                }
            },
            True,
        ],
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "dual",
                        "config_boot": {
                            "vendor_specific": {
                                "component": "eRouter",
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    },
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "component": "eRouter",
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|true"',  # different
                                ],
                            }
                        },
                    },
                }
            },
            True,
        ],
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "dual",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    },
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "component": "eRouter",  # not in env_helper
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    }
                }
            },
            True,
        ],
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "dual",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    },
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                ],
                            }
                        },
                    }
                }
            },
            False,
        ],
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "dual",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetIP|string|172.16.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetMask|string|255.255.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetIP|string|10.0.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetMask|string|255.0.0.0"',
                                ],
                            }
                        },
                    },
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetIP|string|172.16.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetMask|string|255.255.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetIP|string|10.0.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetMask|string|255.0.0.0"',
                                ],
                            }
                        },
                    }
                }
            },
            False,
        ],
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "dual",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetIP|string|172.16.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetMask|string|255.255.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetIP|string|10.0.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetMask|string|255.0.0.0"',
                                ],
                            }
                        },
                    },
                },
                "version": 2.3,
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_CloudUI.HideCustomerDhcpLanChange|boolean|false"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetIP|string|172.16.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_3].LanAllowedSubnetMask|string|255.255.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetIP|string|10.0.0.0"',
                                    'TlvCode 12 TlvString "Device.DHCPv4.Server.Pool.1.X_LGI-COM_LanAllowedSubnetTable.[alias_4].LanAllowedSubnetMask|string|255.255.0.0"',  # different
                                ],
                            }
                        },
                    }
                }
            },
            True,
        ],
    ]

    @pytest.mark.parametrize(
        "environment, requested, raises",
        [
            (environments[0][0], environments[0][1], environments[0][2]),
            (environments[1][0], environments[1][1], environments[1][2]),
            (environments[2][0], environments[2][1], environments[2][2]),
            (environments[3][0], environments[3][1], environments[3][2]),
            (environments[4][0], environments[4][1], environments[4][2]),
            (environments[5][0], environments[5][1], environments[5][2]),
        ],
    )
    def test_env_check(self, environment, requested, raises):
        env_helper = DocsisEnvHelper(environment)
        if raises:
            with pytest.raises(BftEnvMismatch) as e:
                env_helper.env_check(requested)
        else:
            env_helper.env_check(requested)
