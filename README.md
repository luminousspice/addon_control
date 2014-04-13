AddonControl
============
AddonControl is a work in progress addon manager for the Anki flashcard
application that intends to provide the following features:

* Install addons without leaving Anki (through a fuzzy search, similar to
  sublime package control)
* Remove installed addons
* Update adons
* Install all addons named in a file
* Allow addons to be installed from multiple repositories (don't only allow for
  easy installation from Ankiweb)

Status
======
Currently AddonControl allows easy installation and removal of Ankiweb plugins
through a (poor) UI or a text file

Todo
====
* Add more repositories and make it easy to configure which repositories are
  active.
* Add update functionality to UI and to Ankiweb repo

Usage
=====
To install AddonControl, clone this repository and copy AddonControl.py and the
AddonControl directory into the Anki data storage directory (~/Documents/Anki on
mac)