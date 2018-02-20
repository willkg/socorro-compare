# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from itertools import zip_longest


def test_adi(helper, variables):
    host_1 = variables['new_host']
    host_2 = variables['old_host']

    TODAY = datetime.datetime.utcnow()
    LAST_WEEK = TODAY - datetime.timedelta(days=7)

    TODAY = TODAY.strftime('%Y-%m-%d')
    LAST_WEEK = LAST_WEEK.strftime('%Y-%m-%d')

    # Compare ADI data for product/platform combinations between the two
    # environments for the last 7 days. It should be the same.
    for product, platform in [
            ('Firefox', 'Mac OS X'),
            ('Firefox', 'Linux'),
            ('Firefox', 'Windows'),
            ('Firefox', 'Unknown'),
            ('FennecAndroid', 'Linux')
    ]:
        # Get the active versions
        versions = [
            item['version'] for item in
            helper.fetch_json(host_2, '/api/ProductVersions', params={
                'product': product,
                'active': 'true',
                'is_featured': 'true',
            })['hits']
        ]

        print('/api/ADI -> %s (%s)' % (product, versions))

        url = '/api/ADI'
        params = {
            'start_date': LAST_WEEK,
            'end_date': TODAY,
            'product': product,
            'platforms': platform,
            'versions': versions
        }

        adi_1 = helper.fetch_json(host_1, url, params=params)['hits']
        adi_1 = sorted(adi_1, key=lambda item: item['date'])

        adi_2 = helper.fetch_json(host_2, url, params=params)['hits']
        adi_2 = sorted(adi_2, key=lambda item: item['date'])

        errors = 0
        for item_1, item_2 in zip_longest(adi_1, adi_2, fillvalue={}):
            if item_1 != item_2:
                helper.print_compare(item_1, item_2)
                errors += 1

        assert errors == 0
