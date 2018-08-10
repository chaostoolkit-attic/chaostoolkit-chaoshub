# -*- coding: utf-8 -*-
from collections import namedtuple
import os.path
from typing import Dict
from urllib.parse import urlparse

from chaoslib.extension import get_extension
from chaoslib.types import Experiment, Settings

__version__ = '0.1.1'
__all__ = ["get_context"]


Context = namedtuple("Context", [
    "org",
    "workspace",
    "experiment",
    "token",
    "hub_url"
])


def get_context(experiment: Experiment, source: str, org: str,
                workspace: str, settings: Settings) -> Context:
    """
    Load the current Chaos Hub context from the given parameters, in the
    following order (higher has more precedence):

    * as passed to the command line
    * from the "chaoshub" extension block (if any) in the experiment
    * from the settings under the chaoshub vendor section in the settings

    We may parse the URL from the source some day but for now, this sounds
    a little flaky.

    Additionaly, load the hub_url and token from the extension plugin
    settings.
    """
    token = hub_url = None

    extension = get_extension(experiment, "chaoshub")
    if extension:
        if not org:
            org = extension.get("organization")

        if not workspace:
            workspace = extension.get("workspace")

    if settings:
        plugin = settings.get('vendor', {}).get('chaoshub', {})
        if not org:
            org = plugin.get('organization')

        if not workspace:
            workspace = plugin.get('workspace')

        hub_url = plugin.get('hub_url')
        token = plugin.get('token')

    context = Context(
        org=org,
        workspace=workspace,
        experiment=extension.get("experiment") if extension else None,
        hub_url=hub_url,
        token=token
    )

    return context
