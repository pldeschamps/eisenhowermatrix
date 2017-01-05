#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""eisenhower.py: Getting Things Done (GTD) software using an Eisenhower matrix"""

__author__ = "Pierre-Louis Deschamps https://github.com/pldeschamps"
__license__ = "CC BY-SA https://creativecommons.org"

from GUILayout import MVC
from LogicLayout import Tasks

main = MVC.Controller()
main.run()

