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

    $ ./pytest_run.sh [ARGS]


That'll build the ``socorro_compare_1`` Docker image if it doesn't exist.

Then it'll create an empty ``vars.json`` file if you don't already have one.
You'll need to open that file in your favorite text editor, remove the
comment, and set the variable values.

After that, run ``pytest_run.sh`` again and it'll execute ``pytest_build.sh``
in the container with the arguments you passed.

Example::

    $ ./pytest_run.sh --help


To rebuild the image
====================

If Will or someone made changes to requirements or something, you'll need to
rebuild the image. To do that, do this::

    $ make clean


That'll wipe out the Docker image. Next time you run ``pytest_run.sh``, it'll
build a new one.
