#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import traceback
import warnings

import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import Cocoa



main = None


class Action(NSObject):
	'''
	A "bridge" between an objc selector and a Python Action
	This class is needed in order to keep a reference of the selector.
	'''
	def buttonPressed_(self, view):
		if main.DEBUG_LEVEL == 1:
			print (main.buttonIds)
			print (view)
			
		if isinstance(view, NSSliderTouchBarItem):
			view = view.slider()	
			
		instance = main.buttonIds[str(view.identifier())]
		
		if instance.action:
			
			try:
				instance.action.__call__(instance)
			except: # Print beautified traceback instead of mac crash log
				print ("PyTouchBar: Async error:")
				tcb = traceback.format_exc()
				print (tcb)