import click
import json
import logging
import os
import subprocess

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

def _read_config(config_filename):
    # TODO Parse/validate the config information
    with open(config_filename, 'r') as f:
        return json.load(f)


def _get_twitch_secrets():
    load_dotenv()

    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    return client_id, client_secret


def _get_redemption_details(name, config):
    # Get the command for the trigger name
    for redemption_details in config["callbacks"]["redemptions"]:
        if redemption_details["name"] == name:
            return redemption_details

    return None


def _start_twitch_client():
    load_dotenv()

    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    # create instance of twitch API
    twitch = Twitch(client_id, client_secret)
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
    pubsub = PubSub(twitch)
    pubsub.start()


@click.group()
@click.option("--config", default="config.json")
@click.option("--log", default="jsonTest.log")
@click.pass_context
def cli(ctx, config, log):
    ctx.obj["config"] = _read_config(config)
    ctx.obj["log"] = log

    logging.basicConfig(filename=log, level=logging.DEBUG)
    logging.info("Started twitchAPIBot")

    logging.info("Using config file " + config)


@cli.command()
@click.pass_context
def dryrun(ctx):
    config = ctx.obj["config"]
    click.echo('Running stream chaos')

    # TODO start the client


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

    redemption_details = _get_redemption_details(name, config)
    command_list = redemption_details["commands"]

    for command in command_list:
        click.echo(f"Executing command: {command}")
        result = subprocess.run(command.split(), capture_output=True)
        click.echo(f"Command output : {result.stdout}")


if __name__ == '__main__':
    cli(obj={})

# Usecases:
# Base usecase to run the app
#   stream_chaos.py --config config.json run
#
#   stream_chaos.py --config config.json trigger backgroundchange
