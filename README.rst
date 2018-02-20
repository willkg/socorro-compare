======
README
======

You need Docker and a bash shell to run this.

Usage::

    $ ./pytest_run.sh [ARGS]


That'll build the ``socorro_compare_1`` Docker image if it doesn't exist.

Then it'll create an empty ``vars.json`` file if you don't already have one.
You'll need to open that file in your favorite text editor, remove the
comment, and set the variable values.

After that, run ``pytest_run.sh`` again and it'll execute ``pytest_build.sh``
in the container with the arguments you passed.

Example::

    $ ./pytest_run.sh --help
