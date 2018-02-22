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


class Config:
    def __init__(self, cfg=None):
        cfg = cfg or {}
        self.cfg = cfg

    def getoption(self, opt):
        return self.cfg.get(opt)


class Helper:
    def __init__(self, variables):
        self.new_host = variables['new_host']
        self.old_host = variables['old_host']

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

    def fetch_crashids(self, host, product, results=100):
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

        return [item['uuid'] for item in self.fetch_json(host, url, params=params)['hits']]


@pytest.fixture
def helper(variables):
    return Helper(variables)
