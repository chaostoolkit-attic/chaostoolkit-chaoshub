# -*- coding: utf-8 -*-
import json

from chaoslib.settings import load_settings
from chaostoolkit.cli import run as chtk_run
from chaoshub.publish import publish_to_hub

import click

__all__ = ["run"]


@click.command(help=chtk_run.__doc__)
@click.option('--journal-path', default="./journal.json",
              help='Path where to save the journal from the execution.')
@click.option('--dry', is_flag=True,
              help='Run the experiment without executing activities.')
@click.option('--no-validation', is_flag=True,
              help='Do not validate the experiment before running.')
@click.option('--no-publish', is_flag=True,
              help='Run the experiment without publishing to a Chaos Hub.')
@click.option('--organisation', default="default",
              help='Organisation to push the experiment results to.')
@click.option('--workspace', default="default",
              help='Workspace to push the experiment results to.')
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def run(ctx: click.Context, path: str, organisation: str, workspace: str,
        journal_path: str="./journal.json",
        dry: bool=False, no_validation: bool=False, no_publish: bool=False):
    journal = ctx.invoke(chtk_run,
                         path=path,
                         journal_path=journal_path,
                         dry=dry,
                         no_validation=no_validation)
    if not no_publish:
        settings = load_settings()
        hub_url = settings.get('vendor', {}).get('chaoshub', {}).get('hub_url')
        token = settings.get('vendor', {}).get('chaoshub', {}).get('token')
        publish_to_hub(hub_url, token, organisation, workspace, journal_path,
                       journal)
    return journal
