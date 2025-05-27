# Boardfarm DOCSIS

This is the repo  that will contain DOCSIS specific tests and libraries for use for testing a docsis CM, CMTS, or other devices in a typical DOCSIS environment

To use this boardfarm plugin on Ubuntu, you must install:

```sh
# TCL for encoding of an MTA config file
sudo apt update
sudo apt install tcllib

# docsis for running docsis commands
sudo apt install automake libtool libsnmp-dev bison make gcc flex git libglib2.0-dev libfl-dev
git clone https://github.com/rlaager/docsis.git
cd docsis
./autogen.sh
./configure
make
sudo make install
```

## Execute tests

Please see the the demo test suite that utilizes some of the use-cases
from the ```boardfarm-docsis``` plugin.

```bash
.
└── tests
    ├── __init__.py
    ├── docsis
    │   ├── __init__.py
    │   └── test_demo_docsis_1.py
    ├── pytest.ini
    └── tr069
        ├── __init__.py
        └── test_demo_tr069_1.py
```

**_NOTE:_**  In order to run these test you will have to install pytest-boardfarm.

```bash
pip install git+https://github.com/lgirdk/pytest-boardfarm.git@boardfarm3
pip install git+https://github.com/lgirdk/boardfarm-docsis.git@boardfarm3
```

Sample run command:

```bash
pytest \
    --rootdir=. \
    --capture=tee-sys \
    --board-name <cpe-name> \
    --env-config <testbed_env.json>  \
    --junitxml ./results/pytest_run_report.xml \
    --ldap-credentials "username:password"  \
    --inventory-config <lab_devices.json> \
    --html=./results/pytest_run_report.html  \
    --self-contained-html  \
    --save-console-logs=./results  \
    ./boardfarm-docsis/tests/ \
    --skip-contingency-checks
```
