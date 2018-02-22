# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

import isodate


UTC = isodate.UTC


def utc_now():
    return datetime.datetime.now(UTC)


def crashid_key(crashid):
    return (crashid[-6:], crashid)


def to_str(crashids):
    crashids = sorted(crashids, key=crashid_key, reverse=True)

    if len(crashids) > 10:
        return '%s...' % crashids[:10]
    else:
        return '%s' % crashids


# Number of results to look at
N = 500

# Percent of results that should be the same between both environments
# to "pass"
CUTOFF = 0.75


def test_supersearch(helper, variables):
    """Compare Supersearch results between two environments

    Look at two sets of crash ids from a Supersearch for a specific product.
    The two sets of N crash ids won't be exactly the same because the two
    systems are processing out of sync, but there should be some common set of
    crashes between the two.

    Let's say N * CUTOFF of them should be common to "pass".

    """
    host_1 = variables['new_host']
    host_2 = variables['old_host']

    startdate = utc_now() - datetime.timedelta(days=1)


    errors = 0
    for product in ['Firefox', 'FennecAndroid']:
        # Get the last N crash ids from each environment and compare them
        url = '/api/SuperSearch'
        params = {
            'product': product,
            'date': [
                '>=%s' % startdate.strftime('%Y-%m-%d')
            ],
            '_columns': 'uuid',
            '_sort': '-date',
            '_results_number': N
        }
        crash_ids_1 = helper.fetch_json(host_1, url, params=params)['hits']
        crash_ids_1 = set([item['uuid'] for item in crash_ids_1])

        assert len(crash_ids_1) > 0

        crash_ids_2 = helper.fetch_json(host_2, url, params=params)['hits']
        crash_ids_2 = set([item['uuid'] for item in crash_ids_2])

        assert len(crash_ids_2) > 0

        if crash_ids_1 != crash_ids_2:
            print('/api/SuperSearch %s' % product)

            # Figure out intersection of crash ids
            inter = crash_ids_1 & crash_ids_2
            print('Common crash_ids: %s %s' % (len(inter), to_str(inter)))
            if len(inter) >= (N / 4):
                print('Good enough (%s >= %d).' % (len(inter), (N * CUTOFF)))
                continue

            print('Not good enough (%s < %d).' % (len(inter), (N * CUTOFF)))

            # Figure out the symmetric difference (in either left OR right, but
            # not both)
            sym_diff = crash_ids_1 ^ crash_ids_2
            print('Number of crash ids in one but not the other: %s' % len(sym_diff))
            print('')

            # helper.print_compare(crash_ids_1, crash_ids_2)
            errors += 1

    assert errors == 0
