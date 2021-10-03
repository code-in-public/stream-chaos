import logging
import subprocess

import click

from .config import Config
from .twitch_clients import RedemptionPointsClient

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
    """
    Run streamchaos, but instead of executing commands,
    echo what _would_ be executed
    """
    config = ctx.obj["config"]
    click.echo('Running stream chaos')

    RedemptionPointsClient.run(config)


@cli.command()
@click.pass_context
def run(ctx):
    """
    Run streamchaos
    """
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
