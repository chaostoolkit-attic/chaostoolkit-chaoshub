# -*- coding: utf-8 -*-
from chaoslib.settings import load_settings
from chaoslib.types import Journal
from chaostoolkit.cli import run as chtk_run
import click
from logzero import logger

from . import get_context
from .publish import publish_to_hub

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
@click.option('--org',
              help='Organization to push the experiment results to.')
@click.option('--workspace',
              help='Workspace to push the experiment results to.')
@click.argument('source')
@click.pass_context
def run(ctx: click.Context, source: str, org: str = None,
        workspace: str = None, journal_path: str = "./journal.json",
        dry: bool = False, no_validation: bool = False,
        no_publish: bool = False) -> Journal:
    # call the original chaostoolkit run command
    journal = ctx.invoke(
        chtk_run, source=source, journal_path=journal_path, dry=dry,
        no_validation=no_validation, fail_fast=False)

    if no_publish:
        return journal

    settings_path = ctx.obj["settings_path"]
    settings = load_settings(settings_path)
    experiment = journal["experiment"]
    context = get_context(experiment, source, org, workspace, settings)
    publish_to_hub(context, journal_path, journal)

    return journal
