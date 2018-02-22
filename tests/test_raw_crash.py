# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def normalize_raw_crash(raw_crash):
    # Drop keys that will never be equal
    for key in ('timestamp', 'submitted_timestamp'):
        if key in raw_crash:
            del raw_crash[key]
    return raw_crash


def test_raw_crash(helper):
    host_1 = helper.env1['host']
    api_token_1 = helper.env1.get('api_token')

    host_2 = helper.env2['host']
    api_token_2 = helper.env2.get('api_token')

    for product in ['Firefox', 'FennecAndroid']:
        crashids_1 = set(helper.fetch_crashids(host_1, product))
        crashids_2 = set(helper.fetch_crashids(host_2, product))

        common = crashids_1 & crashids_2

        # If we don't have at least 5 common crashes between the two hosts,
        # then something is awry and we should just call it a day
        assert len(common) > 5

        # Look at five crashes that are in both systems
        to_examine = list(common)[:5]

        for crash_id in to_examine:
            raw_crash_1 = helper.fetch_json(
                host_1,
                '/api/RawCrash/',
                api_token=api_token_1, params={
                    'crash_id': crash_id,
                    'format': 'meta'
                }
            )
            raw_crash_1 = normalize_raw_crash(raw_crash_1)

            raw_crash_2 = helper.fetch_json(
                host_2,
                '/api/RawCrash/',
                api_token=api_token_2, params={
                    'crash_id': crash_id,
                    'format': 'meta'
                }
            )
            raw_crash_2 = normalize_raw_crash(raw_crash_2)

            print('/api/RawCrash/ %s' % crash_id)
            assert raw_crash_1 == raw_crash_2
