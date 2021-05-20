class ProvisionHelper:
    """Provision related use cases"""

    def __init__(self, devices):
        self.dev = devices

    def provision_board(self, provisioner, dev_name):
        dev = getattr(self.dev, dev_name)
        prov = getattr(self.dev, provisioner)
        return dev.reprovision(prov)
