import os
import json
import logging
from functools import cached_property

from dotenv import load_dotenv


class Config:

    def __init__(self, filename):
        self.filename = filename
        logging.info("Using config file %s", filename)
        load_dotenv()

    @cached_property
    def raw(self):
        # TODO Parse/validate the config information
        with open(self.filename, 'r') as f:
            return json.load(f)

    def redemption_details(self, name):
        for redemption_details in self.raw["callbacks"]["redemptions"]:
            if redemption_details["name"] == name:
                return redemption_details
        return None

    @cached_property
    def client_id(self):
        return os.getenv('client_id')

    @cached_property
    def client_secret(self):
        return self.os.get('client_secret')
