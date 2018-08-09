# -*- coding: utf-8 -*-
import io
import json

from chaoslib.settings import load_settings, save_settings, \
    CHAOSTOOLKIT_CONFIG_PATH
import click
from logzero import logger

from chaoshub.publish import publish_to_hub
from chaoshub.settings import set_chaos_hub_settings

__all__ = ["login", "publish"]


@click.command()
@click.pass_context
def login(ctx: click.Context):
    """
    Login to a Chaos Hub.
    """
    settings_path = ctx.obj["settings_path"]
    settings = load_settings(settings_path)

    hub_url = click.prompt(
        click.style("Chaos Hub Url", fg='green'), type=str, show_default=True,
        default="https://chaoshub.com")

    token = click.prompt(
        click.style("Chaos Hub Token", fg='green'), type=str, hide_input=True)

    set_chaos_hub_settings(hub_url, token, settings)
    save_settings(settings, settings_path)

    click.echo("Chaos Hub details saved at {}".format(
        settings_path))


@click.command()
@click.argument('journal')
@click.option('--org', default="default",
              help='Organization to push the experiment results to.')
@click.option('--workspace', default="default",
              help='Workspace to push the experiment results to.')
@click.pass_context
def publish(ctx: click.Context, journal: str, org: str, workspace: str):
    """
    Publish your experiment's findings to a Chaos Hub.

    \b
    In order to benefit from these features, you must have registered with
    a Chaos Hub and retrieved an access token. You should set that token in the
    configuration file with `chaos login`.
    """
    settings_path = ctx.obj["settings_path"]
    settings = load_settings(settings_path)
    hub_url = settings.get('vendor', {}).get('chaoshub', {}).get('hub_url')
    token = settings.get('vendor', {}).get('chaoshub', {}).get('token')

    context = get_context(experiment, source, org, workspace, settings)

    with io.open(journal) as f:
        publish_to_hub(context, journal, json.load(f))
