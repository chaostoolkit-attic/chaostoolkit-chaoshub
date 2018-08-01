# -*- coding: utf-8 -*-
import requests
from logzero import logger

__all__ = ["publish_to_hub"]


def publish_to_hub(hub_base_url: str, token: str, org: str,
                   workspace: str, journal_path: str, journal: dict):
    if hub_base_url and token:
        url = "{u}/{org}/{ws}".format(u=hub_base_url,
                                      org=org,
                                      ws=workspace)
        logger.info("Publishing journal to Chaos Hub at " +
                    "{url}".format(url=url))
        token_contents = "Bearer {token}".format(token=token)
        r = requests.put(url, headers={"Accept": "application/json",
                                       "Authorization": token_contents},
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
                     "`chaos login` before attempting to publish.")
