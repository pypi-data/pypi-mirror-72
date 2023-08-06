mandelbrot-orbit
================

This is a command line application to generate Mandelbrot Set point orbits.
An orbit is the series of values for the basic Mandelbrot Set formula: `f(z) = z² + c`

Please have a look at the repo on GitHub:
https://github.com/josecelano/mandelbrot-orbit

Usage
-----

Generate orbit graph for point (-1.3,0) with 100 iterations::

    $ python3 -m mandelbrot_orbit -1.3 0 100
    Executing mandelbrot-orbit version 1.0.0.
    List of argument strings: ['-1.3', '0', '100']

That command will generate an image ``mandelbrot_orbit.png``

Flexible invocation
*******************

The application can be run right from the source directory, in different
ways:

1) Treating the ``mandelbrot_orbit`` directory as a package *and* as the main script::

    $ python3 -m mandelbrot_orbit zx zy num_iterations
    Executing mandelbrot-orbit version 1.0.0.
    List of argument strings: ['zx', 'zy', 'num_iterations']

2) Using ``setup.py develop`` (documented `here <https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode>`_)::

    # This installs the `mandelbrot-orbit` command linking back
    # to the current checkout, quite neat for development!
    $ python setup.py develop
    ...
    $ mandelbrot-orbit zx zy num_iterations

3) Using the ``mandelbrot-orbit-runner.py`` wrapper::

    $ ./mandelbrot-orbit-runner.py zx zy num_iterations
    Executing mandelbrot-orbit version 1.0.0.
    List of argument strings: ['zx', 'zy', 'num_iterations']

Installation sets up bootstrap command
**************************************

Situation before installation::

    $ mandelbrot-orbit
    bash: mandelbrot-orbit: command not found

Installation right from the source tree (or via pip from PyPI)::

    $ python3 setup.py install

Now, the ``mandelbrot-orbit`` command is available::

    $ mandelbrot-orbit -1.3 0 100
    Executing mandelbrot-orbit version 1.0.0.
    List of argument strings: ['-1.3', '0', '100']


On Unix-like systems, the installation places a ``mandelbrot-orbit`` script into a
centralized ``bin`` directory, which should be in your ``PATH``. On Windows,
``mandelbrot-orbit.exe`` is placed into a centralized ``Scripts`` directory which
should also be in your ``PATH``.