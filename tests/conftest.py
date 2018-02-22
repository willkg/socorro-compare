# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

import isodate
import pytest
from _pytest.assertion.util import assertrepr_compare
import requests


UTC = isodate.UTC


def utc_now():
    return datetime.datetime.now(UTC)


def pytest_addoption(parser):
    parser.addoption(
        '--env1', action='store', required=True,
        help='name of environment in vars.json to compare'
    )
    parser.addoption(
        '--env2', action='store', required=True,
        help='name of environment in vars.json to compare'
    )


class Config:
    def __init__(self, cfg=None):
        cfg = cfg or {}
        self.cfg = cfg

    def getoption(self, opt):
        return self.cfg.get(opt)


class Helper:
    def __init__(self, env1, env2):
        self.env1 = env1
        self.env2 = env2

    def utc_now(self):
        return utc_now()

    def print_compare(self, left, right):
        cfg = Config({'verbose': 2})
        output = assertrepr_compare(cfg, '==', left, right)
        if output:
            print('\n'.join(output) + '\n----')

    def fetch_json(self, host, url, api_token=None, params=None):
        if api_token:
            headers = {
                'Auth-Token': api_token
            }
        else:
            headers = {}

        params = params or {}

        resp = requests.get(
            host + url,
            params=params,
            headers=headers
        )
        resp.raise_for_status()

        return resp.json()

    def fetch_crashids(self, host, product, api_token=None, results=100):
        startdate = utc_now() - datetime.timedelta(days=1)

        url = '/api/SuperSearch'
        params = {
            'product': product,
            'date': [
                '>=%s' % startdate.strftime('%Y-%m-%d')
            ],
            '_columns': 'uuid',
            '_sort': '-date',
            '_results_number': results
        }

        resp = self.fetch_json(host, url, api_token=api_token, params=params)
        return [item['uuid'] for item in resp['hits']]


@pytest.fixture
def helper(request, variables):
    env1 = request.config.getoption('env1')
    env2 = request.config.getoption('env2')

    assert env1 in variables, (
        '"%s" is not a valid environment. Available environments: %s' % (
            env1, ', '.join(variables.keys())
        )
    )
    assert env2 in variables, (
        '"%s" is not a valid environment. Available environments: %s' % (
            env2, ', '.join(variables.keys())
        )
    )

    return Helper(variables[env1], variables[env2])
