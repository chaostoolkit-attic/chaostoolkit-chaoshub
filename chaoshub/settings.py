# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from chaoslib.types import Settings

__all__ = ["set_chaos_hub_settings"]


def set_chaos_hub_settings(hub_url: str, token: str, settings: Settings):
    """
    Set the Chaos Hub related entries in the Chaos Toolkit settings.
    """
    if 'auths' not in settings:
        settings['auths'] = {}

    # add an entry to authenticate against the ChaosHub endpoint whenever
    # we run and load an experiment via HTTP(s)
    p = urlparse(hub_url)
    for domain in settings['auths']:
        if domain == p.netloc:
            auth = settings['auths'][domain]
            auth["type"] = "bearer"
            auth["value"] = token
            break
    else:
        auth = settings['auths'][p.netloc] = {}
        auth["type"] = "bearer"
        auth["value"] = token

    # add an entry for the ChaosHub vendor entries
    if 'vendor' not in settings:
        settings['vendor'] = {}

    vendors = settings['vendor']

    if 'chaoshub' not in vendors:
        vendors['chaoshub'] = {}

    vendors['chaoshub'].update({
        'hub_url': hub_url,
        'token': token
    })
