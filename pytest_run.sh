#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


if [ "$INNER"  != "1" ]
then
    # Build-and-run and execute pytest_run.sh in the container
    HASIMAGE=$(docker images | grep socorro_compare_1)

    if [ "$HASIMAGE" == "" ]
    then
        # Build the image
        docker build \
            --file ./Dockerfile \
            --rm \
            --tag socorro_compare_1 \
            .
        echo ""
    fi

    # Make sure there's a vars file and exit out if not
    if [ ! -e "vars.json" ]
    then
        echo "Creating an empty vars.json file..."
        cat > vars.json <<EOF
{
    # Fill in data for each environment you want to test. You
    # need at least two, but can have as many as you like.
    #
    # After you're done, remove this comment because it's not
    # valid JSON.
    "ENV1 NAME": {
        "host": "HOST URL",
        "api_token": ""
    },
    "ENV2 NAME": {
        "host": "HOST URL",
        "api_token": ""
    }
}
EOF
        echo ""
        echo "Please fill in the new_host and old_host values."
        exit 1
    fi

    # Execute "pytest" in the image
    docker run \
        --rm \
        -v `pwd`:/app \
        --workdir /app \
        --env INNER=1 \
        --tty \
        --interactive \
        socorro_compare_1 ./pytest_run.sh $@

    exit
fi

# At this point, we're running inside the docker container.

echo ""
echo "**********************************************************************"
echo "NOTE: If pytest fails with KeyError: 'new_host' type errors, then your"
echo "vars.json file doesn't parse."
echo "**********************************************************************"
echo ""

# Run pytest with the arguments passed
pytest --variables vars.json $@
