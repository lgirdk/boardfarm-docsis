import logging

import boardfarm
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
                "version": "2.3",
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
                "version": "2.3",
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
                "version": "2.3",
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
                "version": "2.3",
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
                "version": "2.3",
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
                "version": "2.3",
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
        [
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": "none",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
                                ],
                            }
                        },
                    },
                },
                "version": "2.3",
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": [
                            "ipv6",
                            "dual",
                            "ipv4",
                        ],  # missing "none"
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
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
                        "eRouter_Provisioning_mode": "none",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
                                ],
                            }
                        },
                    },
                },
                "version": "2.3",
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": [
                            "non",
                            "ipv6",
                            "dual",
                            "ipv4",
                        ],  # misspelled "non"
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
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
                        "eRouter_Provisioning_mode": "none",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
                                ],
                            }
                        },
                    },
                },
                "version": "2.3",
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["none", "ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
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
                        "eRouter_Provisioning_mode": "none",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
                                ],
                            }
                        },
                    },
                },
                "version": "2.3",
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["none", "ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 1",  # differs
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
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
                        "eRouter_Provisioning_mode": "none",
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
                                ],
                            }
                        },
                    },
                },
                "version": "2.3",
            },
            {
                "environment_def": {
                    "board": {
                        "eRouter_Provisioning_mode": ["none", "ipv6", "dual", "ipv4"],
                        "config_boot": {
                            "vendor_specific": {
                                "tlvs": [
                                    "InitializationMode 0",
                                    "TlvCode 12 TlvString 'Device.X_LGI-COM_General.CustomerId|unsignedInt|20'",
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
                    "CMTS": {"model": "C4", "type": "arris"},
                    "board": {
                        "config_boot": {
                            "vendor_specific": {
                                "component": "eRouter",
                                "tlvs": [
                                    "InitializationMode 0",
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_General.CustomerId|unsignedInt|20"',
                                ],
                            }
                        },
                        "country": "NL",
                        "eRouter_Provisioning_mode": "none",
                        "emta": {"config_template": "CH_Compal"},
                        "model": "CH7465LG",
                        "software": {
                            "flash_strategy": "all",
                            "image_uri": "/OneFirmware/DailyBuilds/Jan_2021/20210112/arm-image-rdkb-mv1intel-20210112072903.img",
                        },
                    },
                    "tr-069": {},
                    "voice": {},
                },
                "version": "2.10",
            },
            {
                "environment_def": {
                    "board": {
                        "config_boot": {
                            "vendor_specific": {
                                "component": "eRouter",
                                "tlvs": [
                                    "InitializationMode 0",
                                    'TlvCode 12 TlvString "Device.X_LGI-COM_General.CustomerId|unsignedInt|20"',
                                ],
                            }
                        },
                        "eRouter_Provisioning_mode": "none",
                    },
                }
            },
            False,
        ],
    ]

    """
    environment: env definition (e.g. from Jira)
    requested: env requested (e.g.iwhat a test wants)
    raises: whether this test will raise an exception or not
    """

    @pytest.mark.parametrize(
        "environment, requested, raises",
        [
            (environments[0][0], environments[0][1], environments[0][2]),
            (environments[1][0], environments[1][1], environments[1][2]),
            (environments[2][0], environments[2][1], environments[2][2]),
            (environments[3][0], environments[3][1], environments[3][2]),
            (environments[4][0], environments[4][1], environments[4][2]),
            (environments[5][0], environments[5][1], environments[5][2]),
            (environments[6][0], environments[6][1], environments[6][2]),
            (environments[7][0], environments[7][1], environments[7][2]),
            (environments[8][0], environments[8][1], environments[8][2]),
            (environments[9][0], environments[9][1], environments[9][2]),
            (environments[10][0], environments[10][1], environments[10][2]),
            (environments[11][0], environments[11][1], environments[11][2]),
        ],
    )
    def test_env_check(self, environment, requested, raises):
        env_helper = DocsisEnvHelper(environment)
        if raises:
            with pytest.raises(BftEnvMismatch) as e:
                env_helper.env_check(requested)
        else:
            env_helper.env_check(requested)


class TestEnvHelperBootFileCheck:

    env_boot_file = {
        "environment_def": {
            "board": {
                "boot_file": 'Main \n{\n\t/* eRouter Mode */\n        VendorSpecific\n        {\n                VendorIdentifier 0x02a613;\n                eRouter\n                {\n                        InitializationMode 3;\n                }\n        }\n        /* TR69 Management Server */\n        VendorSpecific\n        {\n                VendorIdentifier 0x02a613;\n                eRouter\n                {\n                        TR69ManagementServer\n                        {\n                                URL "http://acs_server.boardfarm.com:9675";\n                                ACSOverride 1;\n                        }\n                }\n        }\n}',
                "eRouter_Provisioning_mode": "dual",
            },
        },
        "version": "1.0",
    }

    env_with_boot_file = DocsisEnvHelper(env_boot_file)

    def test_boot_file_not_contains_regex(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "not_contains_regex": r"\s*eRouter\s*\n\s*{\s*\n\s*TR69ManagementServer\s*\n\s*{\s*\n(.*;\s*\n)*\s*EnableCWMP\s*[0-9].*"
                    }
                }
            }
        }
        assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_contains_regex(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "contains_regex": r"\s*eRouter\s*\n\s*{\s*\n\s*TR69ManagementServer\s*\n\s*{\s*\n(.*;\s*\n)*\s*ACSOverride\s*[0-9].*"
                    }
                }
            }
        }
        assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_contains_exact(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "contains_exact": 'eRouter\n                {\n                        TR69ManagementServer\n                        {\n                                URL "http://acs_server.boardfarm.com:9675";'
                    }
                }
            }
        }
        assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_not_contains_exact(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "not_contains_exact": "Dummy\n                {\n                        TR69ManagementServer\n                        {\n                                EnableCWMP "
                    }
                }
            }
        }
        assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_not_contains_regex_negative_negative(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "not_contains_regex": r"\s*eRouter\s*\n\s*{\s*\n\s*TR69ManagementServer\s*\n\s*{\s*\n(.*;\s*\n)*\s*ACSOverride\s*[0-9].*"
                    }
                }
            }
        }
        with pytest.raises(boardfarm.exceptions.BftEnvMismatch):
            assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_contains_regex_negative(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "contains_regex": r"\s*eRouter\s*\n\s*{\s*\n\s*TR69ManagementServer\s*\n\s*{\s*\n(.*;\s*\n)*\s*EnableCWMP\s*[0-9].*"
                    }
                }
            }
        }
        with pytest.raises(boardfarm.exceptions.BftEnvMismatch):
            assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_contains_exact_negative(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "contains_exact": "eRouter\n                {\n                        TR69ManagementServer\n                        {\n                                URL Dummy;"
                    }
                }
            }
        }
        with pytest.raises(boardfarm.exceptions.BftEnvMismatch):
            assert self.env_with_boot_file.env_check(test_req)

    def test_boot_file_not_contains_exact_negative(self):
        test_req = {
            "environment_def": {
                "board": {
                    "boot_file": {
                        "not_contains_exact": 'eRouter\n                {\n                        TR69ManagementServer\n                        {\n                                URL "http://acs_server.boardfarm.com:9675";'
                    }
                }
            }
        }
        with pytest.raises(boardfarm.exceptions.BftEnvMismatch):
            assert self.env_with_boot_file.env_check(test_req)
