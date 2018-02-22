======
README
======

What is this?
=============

This is a set of tests that compare the data in two Socorro environments.
Comparing data is a little hard since data ebbs and flows according to
the whims of the cosmos and it's unlikely that data in two environments
is identical. Still, these tests compare them and try to give an
approximation of whether they compare favorably or not.

Also, if you're not Miles, Brian, Will, Mike, or Lonnen, you probably
don't want to use this.

:Documentation: You're reading it!
:Bugs: https://github.com/willkg/socorro-compare/issues
:License: MPLv2


Usage
=====


You need Docker and a bash shell to run this.

Usage::

    $ ./pytest_run.sh --env1=ENV --env2=ENV [ARGS]


That'll build the ``socorro_compare_1`` Docker image if it doesn't exist.

Then it'll create an empty ``vars.json`` file if you don't already have one.
You'll need to open that file in your favorite text editor, remove the
comment, and add environment data.

After that, run it again and it'll execute in the container with the arguments
you passed.

To see pytest help after the container is built and there's a ``vars.json``,
pass in ``--help``::

    $ ./pytest_run.sh --help


vars.json
=========

This requires that you specify data for the environments you're comparing. You
do that in a ``vars.json`` in the root directory.

Example ``vars.json``::

    {
        "stage": {
            "host": "https://crash-stats-stage.example.com",
            "api_token": "xxxxx"
        },
        "newstage": {
            "host": "https://crash-stats-newstage.example.com",
            "api_token": "xxxxx"
        }
    }


NOTE: If you don't have API tokens for the environment, you can omit them or
make the values empty strings. Tests that require API tokens will degrade or
skip.

Then we'd run ``pytest_run.sh`` like this::

    $ pytest_run.sh --env1=stage --env2=newstage


NOTE: You can include as many environments as you like. You use the ``--env1``
and ``--env2`` command line variables to specify which two you're comparing.

NOTE: It has to be valid JSON. If it's not, then running ``pytest_run.sh`` will
fail.


To rebuild the image
====================

If Will or someone made changes to requirements or something, you'll need to
rebuild the image. To do that, do this::

    $ make clean


That'll wipe out the Docker image. Next time you run ``pytest_run.sh``, it'll
build a new one.
