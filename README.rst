*****************************
ImageSourcePy Device (Python)
*****************************

Overview
========

This package provides base classes for Karabo device classes that provide images
and are written in the bound Python API.


Testing
=======

Every Karabo device in Python is shipped as a regular python package.
In order to make the device visible to any device-server you have to install
the package to Karabo's own Python environment.

Simply type:

``pip install -e .``

in the directory of where the ``setup.py`` file is located, or use the ``karabo``
utility script:

``karabo develop imageSourcePy``


Running
=======

If you want to manually start a server using this device, simply type:

``karabo-pythonserver serverId=pythonServer/1 deviceClasses=ImageSource``

Or just use (a properly configured):

``karabo-start``


Contact
========

For questions, please contact opensource@xfel.eu.


License and Contributing
=========================

This software is released by the European XFEL GmbH as is and without any
warranty under the GPLv3 license.
If you have questions on contributing to the project, please get in touch at
opensource@xfel.eu.

Before contributing you are required to sign either a Contributors License Agreement,
or Entity Contributor License Agreement, which you can find in the root directory of
this project. Please mail the signed agreement to opensource@xfel.eu.
By signing the CLA you acknowledge that copyright and all intellectual property rights
of your contribution are transferred to the European X-ray Free Electron Laser
Facility GmbH.

You are free to use this software under the terms of the GPLv3 without signing a CLA.
