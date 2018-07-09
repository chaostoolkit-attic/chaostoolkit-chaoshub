# -*- coding: utf-8 -*-
import io
import json

from chaoshub.publish import publish_to_hub
from chaoshub.settings import update_chaos_hub_settings_in_place
from chaoslib.settings import load_settings, save_settings

import click
from logzero import logger

__all__ = ["login"]


@click.command()
@click.pass_context
def login(ctx: click.Context):
    """
    Login to a Chaos Hub.
    """
    settings = load_settings()
    hub_url = click.prompt(click.style("Chaos Hub Url", fg='green'), type=str)
    token = click.prompt(
        click.style("Chaos Hub Token", fg='green'), type=str, hide_input=True)
    update_chaos_hub_settings_in_place(hub_url, token, settings)
    save_settings(settings)
    click.echo("Chaos Hub details saved")


@click.command()
@click.argument('journal')
@click.option('--organisation', default="default",
              help='Organisation to push the experiment results to.')
@click.option('--workspace', default="default",
              help='Workspace to push the experiment results to.')
@click.pass_context
def publish(ctx: click.Context, journal: str, organisation: str,
            workspace: str):
    """
    Publish your experiment's findings to a Chaos Hub.

    \b
    In order to benefit from these features, you must have registered with
    a Chaos Hub and retrieved an access token. You should set that token in the
    configuration file with `chaos login hub`.
    """
    settings = load_settings()
    hub_url = settings.get('vendor', {}).get('chaoshub', {}).get('hub_url')
    token = settings.get('vendor', {}).get('chaoshub', {}).get('token')
    if hub_url and token:
        with io.open(journal) as f:
            journal_json = json.load(f)
            publish_to_hub(hub_url, token, organisation, workspace, journal,
                           journal_json)
    else:
        logger.warning("No Chaos Hub configured. Please execute " +
                       "`chaos login hub` before attempting to publish.")