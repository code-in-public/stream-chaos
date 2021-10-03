import click
import json
import logging
import os
import subprocess
from functools import cached_property

from dotenv import load_dotenv

from twitchAPI.twitch import Twitch
from twitchAPI.pubsub import PubSub
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator

# Followers
#    leoeliass
#    iLTanoMarco
#    ishahanm
#    augvst_
#    xphallicjanitorx
#    ItsMeToeKnee
#    darkcreation876
#    Diegorellana_
#    PJZ_here
#    owaisbukhari
#    reachMGS
#    RoboDom711
#    tommaydos
#    iHel
#
# Cheers
#    xphallicjanitorx
#    AlongWithCris
#    robotichead
#
# Gifted subs
#   YogaWithJen
#
# Subs!!!!
#   AlongWithCris
#   natnatenatelift151
#
# TIER 3 SUBS
#    TripolarBears


class Config:

    def __init__(self, filename):
        self.filename = filename
        logging.info("Using config file %s", filename)

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


def _get_twitch_secrets():
    load_dotenv()

    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    return client_id, client_secret


class RedemptionPointsClient:

    def __init__(self):
        self.redemption_call_backs = {}
        self.pubsub = None
        self.points_redeem_uuid = None

    def callback_points(self, uuid, data):
        """
        Extracted to the channel points
        Followers:
            MrsFabrik
            aquafunkalisticbootywhap
        """
        print('got points callback for UUID ' + str(uuid))

        # TODO Make sure this doesn't totally explode
        redemption_id = data['data']['redemption']['reward']['id']

        print('Redemption id is' + str(redemption_id))

        if redemption_id in self.redemption_call_backs:
            self.redemption_call_backs[redemption_id](data)
        else:
            print('Unexpected points redemption!!!!')

    def start(self):
        load_dotenv()

        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        # create instance of twitch API
        self.twitch = twitch = Twitch(client_id, client_secret)
        twitch.authenticate_app([])

        # get ID of user
        user_info = twitch.get_users(logins=['codeinpublic'])
        user_id = user_info['data'][0]['id']

        target_scope = [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_READ_REDEMPTIONS]
        auth = UserAuthenticator(twitch, target_scope, force_verify=False)

        # this will open your default browser and prompt you with the twitch verification website
        token, refresh_token = auth.authenticate()

        twitch.set_user_authentication(token, target_scope, refresh_token)

        # starting up PubSub
        self.pubsub = pubsub = PubSub(twitch)
        pubsub.start()

        self.points_redeem_uuid = pubsub.listen_channel_points(user_id, self.callback_points)

    def stop(self):
        # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
        self.pubsub.unlisten(self.points_redeem_uuid)
        self.pubsub.stop()

    @classmethod
    def run(cls):
        client = cls()
        client.start()

        # Prevents early termination
        input('press ENTER to close...')

        client.stop()


@click.group()
@click.option("--config", default="config.json")
@click.option("--log", default="jsonTest.log")
@click.pass_context
def cli(ctx, config, log):
    ctx.obj["config"] = Config(config)
    ctx.obj["log"] = log

    logging.basicConfig(filename=log, level=logging.DEBUG)
    logging.info("Started twitchAPIBot")



@cli.command()
@click.pass_context
def dryrun(ctx):
    config = ctx.obj["config"]
    click.echo('Running stream chaos')

    RedemptionPointsClient.run()


@cli.command()
@click.pass_context
def run(ctx):
    config = ctx.obj["config"]
    click.echo('Running stream chaos')

    # TODO start the client


@cli.command()
@click.pass_context
# TODO Provide a list of valid command names
# https://click.palletsprojects.com/en/8.0.x/options/#choice-options
@click.option("--name", required=True)
def trigger(ctx, name):
    config = ctx.obj["config"]
    click.echo(f"Triggering command {name}")

    redemption_details = config.redemption_details(name)
    command_list = redemption_details["commands"]

    for command in command_list:
        click.echo(f"Executing command: {command}")
        result = subprocess.run(command.split(), capture_output=True)
        click.echo(f"Command output : {result.stdout}")


def main():
    cli(obj={})


if __name__ == '__main__':
    main()

# Usecases:
# Base usecase to run the app
#   stream_chaos.py --config config.json run
#
#   stream_chaos.py --config config.json trigger backgroundchange
