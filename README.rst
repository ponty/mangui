GUI generator for command-line programs on Linux.
The parameters are read from the man page using doclifter_.

Links:
 * home: https://github.com/ponty/mangui
 * documentation: http://ponty.github.com/mangui

Features:
 - implemented in Python_
 - runs on Linux
 - GUI is based on wxPython_
 - doclifter_ is used for parsing man pages
 
Known problems:
 - experimental program
 - GUI is not fully implemented
 - doclifter_ can not parse all manual-pages
 - only some commands are tested

Basic usage
------------
::

    $ python -m mangui.wxgui ls


Installation
============

General
--------

 * install Python_
 * install pip_
 * install doclifter_
 * install wxPython_ 
 * install the program::

    # as root
    pip install https://github.com/ponty/mangui/zipball/master    


Ubuntu
----------
::

    sudo apt-get install python-pip doclifter
    sudo pip install https://github.com/ponty/mangui/zipball/master

Uninstall
----------

::
	
    # as root
    pip uninstall mangui
    

.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _Python: http://www.python.org/
.. _wxPython: http://www.wxpython.org/
.. _doclifter: http://www.catb.org/~esr/doclifter/