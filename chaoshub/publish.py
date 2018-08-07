# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Experiment, Journal
from logzero import logger
import requests

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


def publish_to_hub(hub_base_url: str, token: str, org: str,
                   workspace: str, journal_path: str, journal: Journal):
    """
    Publish the experiment and the journal to the remote Chaos Hub instance.
    """
    if not hub_base_url or not token:
        logger.debug(
            "No Chaos Hub configured. Please execute `chaos login` before "
            "attempting to publish.")
        return

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    url = build_url(hub_base_url, org, workspace)

    experiment_url = build_experiment_url(url)
    logger.info(
        "Publishing experiment to Chaos Hub at {}".format(
            experiment_url))

    r = requests.post(
        experiment_url, headers=headers, json=journal["experiment"])

    response = r.json()

    # we will receive a 201 only when the experiment was indeed created
    # otherwise, it means it already exists
    if r.status_code not in [200, 201]:
        logger.warning(
            "Experiment failed to be published to {}: {}".format(
                url, response.get('message')))
    else:
        logger.info("Experiment available at {}".format(
            r.headers["Location"]))

        experiment_id = response["id"]
        logger.info("Publishing journal to Chaos Hub at {}".format(url))
        
        url = build_run_url(url, experiment_id)
        r = requests.post(url, headers=headers, json=journal)

        if r.status_code != 201:
            logger.debug(r.text)
            logger.warning(
                "Experimental findings in '{}' failed to publish".format(
                                j=journal_path))
        else:
            logger.info(
                "Experimental findings in '{}' published to {}".format(
                    journal_path, url))
