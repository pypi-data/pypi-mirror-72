Units Converter
###############

Units Converter is a user interface utility module, to convert wave units into another, ex: namometers to electron-volts

Usage
-----

Units Converter user interface can be used as a standalone application or integrated with a more complex application
using the Qt5 framework.


Overview
--------

Units Converter is written in `Python`__ and uses Python 3.7+. It uses the `PyQt5`__ library and the excellent `pyqtgraph`__ package
for its user interface. For BeeActions to run smoothly, you need a Python distribution to be installed. Here are some advices.

__ https://docs.python-guide.org/
__ http://doc.qt.io/qt-5/qt5-intro.html
__ http://www.pyqtgraph.org/

On all platforms **Windows**, **MacOS** or **Linux**, `Anaconda`__ or `Miniconda`__ is the advised distribution/package
manager. Environments can be created to deal with different version of packages and isolate the code from other
programs. Anaconda comes with a full set of installed scientific python packages while *Miniconda* is a very
light package manager.

__ https://www.anaconda.com/download/
__ https://docs.conda.io/en/latest/miniconda.html




Setting up a new environment
----------------------------

* Download and install Miniconda3.
* Open a console, and cd to the location of the *condabin* folder, for instance: ``C:\Miniconda3\condabin``
* Create a new environment: ``conda create -n my_env python=3.7``, where my_env is your new environment name, could be
*unitconv_env*. This will create the environment with python version 3.7 that is currently the recommended one.
* Activate your environment so that only packages installed within this environment will be *seen* by Python:
  ``conda activate my_env``
* Install, using conda manager, some mandatory packages: ``conda install pip`` and ``conda install pyqt``

Installing Units Converter
--------------------------

Easiest part: in your newly created and activated environment enter: ``pip install units_converter``. This will install
*Units Converter* and all its dependencies.

Starting Units Converter
------------------------

Open a command line and **activate your environment** (if you're using anaconda or miniconda) and execute either:

*  ``python -m units_converter.main``


  .. _shortcut_section:

Creating shortcuts on **Windows**
---------------------------------

You can easily start BeeActions using the command line as stated above, but Windows users
will probably prefer using shortcuts on the desktop. Here is how to do it (Thanks to Christophe Halgand for the procedure):

* First create a shortcut (see :numref:`shortcut_create`) on your desktop (pointing to any file or program, it doesn't matter)
* Right click on it and open its properties (see :numref:`shortcut_prop`)
* On the *Start in* field ("Démarrer dans" in french and in the figure), enter the path to the condabin folder of your miniconda or
  anaconda distribution, for instance: ``C:\Miniconda3\condabin``
* On the *Target* field, ("Cible" in french and in the figure), enter this string:
  ``C:\Windows\System32\cmd.exe /k conda activate my_env & python -m units_converter.main``. This means that
  your shortcut will open the windows's command line, then execute your environment activation (*conda activate my_env* bit),
  then finally execute and start **Python**, opening the correct units_converter file (here *main.py*,
  starting the module, *python -m units_converter.main* bit)
* You're done!

   .. _shortcut_create:

.. figure:: documentation/image/shortcut_creation.png
   :alt: shortcut

   Create a shortcut on your desktop

   .. _shortcut_prop:

.. figure:: documentation/image/shortcut_prop.PNG
   :alt: shortcut properties

   Shortcut properties

