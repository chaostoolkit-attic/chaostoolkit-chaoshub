# -*- coding: utf-8 -*-
import requests
from logzero import logger

__all__ = ["publish_to_hub"]


def publish_to_hub(hub_base_url: str, token: str, organisation: str,
                   workspace: str, journal_path: str, journal: dict):
    if hub_base_url and token:
        url = "{u}/{org}/{ws}".format(u=hub_base_url,
                                      org=organisation,
                                      ws=workspace)
        logger.info("Publishing journal to Chaos Hub at " +
                    "{url}".format(url=url))
        r = requests.put(url, headers={"Accept": "application/json",
                                       "CHAOSHUB-TOKEN": token},
                         json=journal)
        if r.status_code != 200:
            logger.warning("Experimental findings in " +
                           "'{j}' failed to publish to {u}"
                           .format(j=journal_path, u=url))
        else:
            logger.info("Experimental findings in "
                        "'{j}' published to {u}"
                        .format(j=journal_path, u=url))
    else:
        logger.debug("No Chaos Hub configured. Please execute " +
                     "`chaos login hub` before attempting to publish.")