import re

from boardfarm.exceptions import BftEnvMismatch


class SkuHelper:
    """helps with SKU verification and handling"""

    def __init__(self, devices):
        self.dev = devices

    def verify_sku(self):
        self.dev.board.check_sku()

    def verify_sku_customer_id(self):
        """Verify if SKU and Customer_id are available in env json and match them
        :rtype value: boolean
        """

        board = self.dev.board
        env_helper = board.env_helper

        if env_helper.has_board_sku():

            board_sku = env_helper.get_board_sku()

            if env_helper.has_customer_id():
                bootfile = env_helper.get_board_boot_file()

                if bootfile.find(
                    "CustomerId|unsignedInt|" + str(board.sku_dict[board_sku])
                ):
                    return True
                else:
                    bootfile_cust_id = re.search(
                        r"CustomerId\|unsignedInt\|(\d{0,3})", bootfile
                    )
                    raise BftEnvMismatch(
                        f"SKU and Customer_id mismatch {board.sku_dict[board_sku]} != {bootfile_cust_id},check bootfile"
                    )
            else:
                if env_helper.is_production_image():
                    # returns True until there is a method to check inventory json
                    return True
                else:
                    env_helper.add_customerid_to_bootfile(board.sku_dict[board_sku])
                    return True
        elif board.is_customer_id_supported():
            raise BftEnvMismatch("Board SKU missing while board supports it")
