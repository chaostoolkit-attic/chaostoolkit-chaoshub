# -*- coding: utf-8 -*-
from chaoslib.types import Settings

__all__ = ["update_chaos_hub_settings_in_place"]


def update_chaos_hub_settings_in_place(hub_url: str,
                                       token: str,
                                       settings: Settings):
    if 'vendor' not in settings:
        settings['vendor'] = {}

    vendors = settings['vendor']

    if 'chaoshub' not in vendors:
        vendors['chaoshub'] = {
            'hub_url': hub_url,
            'token': token
        }
    else:
        vendors['chaoshub']['hub_url'] = hub_url
        vendors['chaoshub']['token'] = token
