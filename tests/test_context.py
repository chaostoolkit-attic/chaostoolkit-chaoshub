# -*- coding: utf-8 -*-

from chaoshub import Context, get_context


def test_get_context_from_cli():
    context = get_context({}, "", "myorg", "myworkspace", {})

    assert context.org == "myorg"
    assert context.workspace == "myworkspace"
    assert context.experiment is None
    assert context.hub_url is None
    assert context.token is None


def test_get_context_from_settings():
    context = get_context({}, "", None, None, {
        "vendor": {
            "chaoshub": {
                "organization": "mysettingsorg",
                "workspace": "mysettingsworkspace",
                "token": "XYZ",
                "hub_url": "https://chaoshub.com"
            }
        }
    })  

    assert context.org == "mysettingsorg"
    assert context.workspace == "mysettingsworkspace"
    assert context.experiment is None
    assert context.hub_url == "https://chaoshub.com"
    assert context.token == "XYZ"


def test_get_context_cli_override_all():
    context = get_context({
        "extensions": [
            {
                "name": "chaoshub",
                "experiment": "1234"
            }
        ]
    }, 
    "",
    "myorg",
    "myworkspace",
    {
        "vendor": {
            "chaoshub": {
                "organization": "mysettingsorg",
                "workspace": "mysettingsworkspace",
                "token": "XYZ",
                "hub_url": "https://chaoshub.com"
            }
        }
    })

    assert context.org == "myorg"
    assert context.workspace == "myworkspace"
    assert context.experiment == "1234"
    assert context.hub_url == "https://chaoshub.com"
    assert context.token == "XYZ"