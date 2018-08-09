# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Experiment, Journal
from logzero import logger
import requests

from . import Context

__all__ = ["publish_to_hub"]


def build_url(hub_base_url: str, org: str, workspace: str) -> str:
    """
    Build the base URL of the Chaos Hub workspace where the experiment and
    the journal will be stored and be made visible.
    """
    return '/'.join([hub_base_url, 'api', org, workspace])


def build_experiment_url(base_url: str) -> str:
    """
    Build the URL for an experiment to be published to.
    """
    return '/'.join([base_url, 'experiment'])


def build_run_url(base_url: str, experiment_id: str) -> str:
    """
    Build the URL for a journal to be pushed to.
    """
    return '/'.join([base_url, 'experiment', experiment_id, 'execution'])


def publish_to_hub(context: Context, journal_path: str, journal: Journal):
    """
    Publish the experiment and the journal to the remote Chaos Hub instance.
    """
    if not context.hub_url or not context.token:
        logger.debug(
            "No Chaos Hub configured. Please execute `chaos login` before "
            "attempting to publish.")
        return

    if not context.org or not context.workspace:
        logger.debug(
            "Chaos Hub is configured but you did not specify an "
            "organization, or a workspace, to the `run` command, let's "
            "by-pass the publishing process.")
        return

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(context.token)
    }
    url = build_url(context.hub_url, context.org, context.workspace)

    experiment_url = build_experiment_url(url)
    logger.info(
        "Publishing experiment to Chaos Hub at {}".format(
            experiment_url))

    experiment = journal["experiment"]
    r = requests.post(
        experiment_url, headers=headers, json=experiment)

    # we will receive a 201 only when the experiment was indeed created
    # otherwise, it means it already exists
    if r.status_code not in [200, 201]:
        is_json = 'application/json' in r.headers["content-type"]
        error = r.json() if is_json else r.text
        logger.warning(
            "Experiment failed to be published to {}: {}".format(url, error))
    else:
        response = r.json()
        logger.info("Experiment available at {}".format(
            r.headers["Location"]))

        experiment_id = response["id"]
        url = build_run_url(url, experiment_id)
        logger.info("Publishing journal to Chaos Hub at {}".format(url))
        r = requests.post(url, headers=headers, json=journal)

        if r.status_code != 201:
            logger.debug(r.text)
            logger.warning(
                "Experimental findings in '{}' failed to publish".format(
                    journal_path))
        else:
            logger.info(
                "Experimental findings in '{}' published to {}".format(
                    journal_path, url))
