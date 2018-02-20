# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def test_product_versions(helper, variables):
    host_1 = variables['new_host']
    host_2 = variables['old_host']

    for product in ['Firefox', 'FennecAndroid']:
        print('/api/ProductVersions -> %s' % product)
        url = '/api/ProductVersions'
        params = {
            'product': product,
            'active': 'true',
        }

        versions_1 = helper.fetch_json(host_1, url, params=params)['hits']

        versions_2 = helper.fetch_json(host_2, url, params=params)['hits']

        # Go through and add sentinels for msising versions
        versions_map_1 = dict([(item['version'], item) for item in versions_1])
        versions_map_2 = dict([(item['version'], item) for item in versions_2])

        errors = 0
        same = 0

        # Compare left to right
        for key in versions_map_1.keys():
            item_1 = versions_map_1.get(key, {})
            item_2 = versions_map_2.get(key, {})

            if item_1 != item_2:
                helper.print_compare(item_1, item_2)
                errors += 1
            else:
                same += 1

        # Compare right to left
        for key in versions_map_2.keys():
            item_1 = versions_map_1.get(key, {})
            item_2 = versions_map_2.get(key, {})

            if item_1 != item_2:
                helper.print_compare(item_1, item_2)
                errors += 1
            else:
                same += 1

        assert errors == 0
