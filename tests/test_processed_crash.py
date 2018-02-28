# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


IGNORE_KEYS = [
    # timestamps always differ
    'startedDateTime',
    'date_processed',
    'completeddatetime',

    # processor notes includes node information and timestamps
    'processor_notes',
]


def normalize_processed_crash(processed_crash):
    # Drop keys that will never be equal
    for key in IGNORE_KEYS:
        if key in processed_crash:
            del processed_crash[key]
    return processed_crash


def get_crashids(helper, host_1, host_2):
    """Retrieve a list of crashids common between the two hosts"""
    crashids = []

    for product in ['Firefox', 'FennecAndroid']:
        crashids_1 = set(helper.fetch_crashids(host_1, product))
        crashids_2 = set(helper.fetch_crashids(host_2, product))

        common = crashids_1 & crashids_2

        # If we don't have at least 5 common crashes between the two hosts,
        # then something is awry and we should just call it a day
        assert len(common) > 5
        crashids.extend(list(common))

    return crashids


def test_processed_crash(request, helper):
    requested_crashids = [
        item.strip()
        for item in request.config.getoption('crashids').split(',')
        if item.strip()
    ]

    host_1 = helper.env1['host']
    api_token_1 = helper.env1.get('api_token')

    host_2 = helper.env2['host']
    api_token_2 = helper.env2.get('api_token')

    to_examine = requested_crashids or get_crashids(helper, host_1, host_2)[:5]

    for crash_id in to_examine:
        processed_crash_1 = helper.fetch_json(
            host_1,
            '/api/ProcessedCrash/',
            api_token=api_token_1, params={
                'crash_id': crash_id,
                'format': 'meta'
            }
        )
        processed_crash_1 = normalize_processed_crash(processed_crash_1)

        processed_crash_2 = helper.fetch_json(
            host_2,
            '/api/ProcessedCrash/',
            api_token=api_token_2, params={
                'crash_id': crash_id,
                'format': 'meta'
            }
        )
        processed_crash_2 = normalize_processed_crash(processed_crash_2)

        print('/api/ProcessedCrash/ %s' % crash_id)
        assert processed_crash_1 == processed_crash_2
