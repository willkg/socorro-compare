# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def test_supersearch(helper, variables):
    host_1 = variables['new_host']
    host_2 = variables['old_host']

    errors = 0
    for product in ['Firefox', 'FennecAndroid']:

        # Get the last 10 crash ids from each environment and compare them
        url = '/api/SuperSearch'
        params = {
            'product': product,
            '_columns': 'uuid',
            '_results_number': 10
        }
        crash_ids_1 = helper.fetch_json(host_1, url, params=params)['hits']
        crash_ids_1 = sorted([item['uuid'] for item in crash_ids_1])

        crash_ids_2 = helper.fetch_json(host_2, url, params=params)['hits']
        crash_ids_2 = sorted([item['uuid'] for item in crash_ids_2])

        if crash_ids_1 != crash_ids_2:
            print('/api/SuperSearch %s' % product)
            helper.print_compare(crash_ids_1, crash_ids_2)
            errors += 1

    assert errors == 0
