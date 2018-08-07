# -*- coding: utf-8 -*-
from chaoslib.types import Settings

__all__ = ["set_chaos_hub_settings"]


def set_chaos_hub_settings(hub_url: str, token: str, settings: Settings):
    """
    Set the Chaos Hub related entries in the Chaos Toolkit settings.
    """
    if 'vendor' not in settings:
        settings['vendor'] = {}

    vendors = settings['vendor']

    if 'chaoshub' not in vendors:
        vendors['chaoshub'] = {}

    vendors['chaoshub'].update({
        'hub_url': hub_url,
        'token': token
    })
