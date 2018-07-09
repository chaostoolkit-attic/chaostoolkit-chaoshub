# -*- coding: utf-8 -*-

from chaoshub.settings import update_chaos_hub_settings_in_place

def test_adding_new_chaos_hub_settings():
    settings = {}
    hub_url = "myhub"
    token = "mytoken"
    update_chaos_hub_settings_in_place(hub_url,token,settings)
    assert 'vendor' in settings
    assert 'chaoshub' in settings['vendor']
    assert 'hub_url' in settings['vendor']['chaoshub']
    assert 'token' in settings['vendor']['chaoshub']
    assert settings['vendor']['chaoshub']['hub_url'] == hub_url
    assert settings['vendor']['chaoshub']['token'] == token


def test_updating_existing_chaos_hub_settings():
    settings = {'vendor': {
        'chaoshub': {
            'hub_url':'old-hub-url',
            'token':'old-token'
        }
    }}
    hub_url = "myhub"
    token = "mytoken"
    update_chaos_hub_settings_in_place(hub_url,token,settings)
    assert 'vendor' in settings
    assert 'chaoshub' in settings['vendor']
    assert 'hub_url' in settings['vendor']['chaoshub']
    assert 'token' in settings['vendor']['chaoshub']
    assert settings['vendor']['chaoshub']['hub_url'] == hub_url
    assert settings['vendor']['chaoshub']['token'] == token


def test_only_updating_existing_chaos_hub_settings():
    settings = {'vendor': {
        'chaoshub': {
            'hub_url':'old-hub-url',
            'token':'old-token',
            'misc':'misc-setting'
        }
    }}
    hub_url = "myhub"
    token = "mytoken"
    update_chaos_hub_settings_in_place(hub_url,token,settings)
    assert 'vendor' in settings
    assert 'chaoshub' in settings['vendor']
    assert 'hub_url' in settings['vendor']['chaoshub']
    assert 'token' in settings['vendor']['chaoshub']
    assert settings['vendor']['chaoshub']['hub_url'] == hub_url
    assert settings['vendor']['chaoshub']['token'] == token
    assert settings['vendor']['chaoshub']['misc'] == 'misc-setting'