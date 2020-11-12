Xbox-Controller-for-Python
==============================

Use an Xbox 360 /XBone Controller with Python on Windows

A module for getting input from Microsoft XBox controllers via the XInput library on Windows.

Adapted from Jason R. Coombs' code here:
http://pydoc.net/Python/jaraco.input/1.0.1/jaraco.input.win32.xinput/
under the MIT licence terms

* Upgraded to Python 3
* Modified to add deadzones, reduce noise, and support vibration
* Only req is Pyglet ~1.2alpha1 or higher~ confirmed to work with 1.2.4 (latest): ```pip install pyglet``` 
