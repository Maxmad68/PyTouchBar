#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


from tkinter import *
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

from .constants import *
from .exceptions import *
from . import action
from . import items as TouchBarItems


main = sys.modules[__name__]
TouchBarItems.main = main
action.main = main

Action = action.Action



global DEBUG_LEVEL, buttonIds, tbdelegate, touchbar_items, customization_identifier, touchbar_items_id
DEBUG_LEVEL = 0

buttonIds = {}
touchbar_items = []
touchbar_items_id = {}
touchbar_escape_item = None
customization_identifier = None

	

	
class NSWindowControllerTBModified (NSWindowController):
	'''
	A NSWindowController that handle touchbar methods.
	It will be applied to windows with the "prepare_window" functions.
	'''
	
	def touchBar(self):
		''' Give the touchbar to the window'''
		global DEBUG_LEVEL, buttonIds, touchbar_items_id, touchbar_items, tbdelegate, touchbar_items_customization, touchbar_escape_item, customization_identifier
		if DEBUG_LEVEL == 1:
			print ('TouchBar initializing') 
			
		tb = NSTouchBar.alloc().init()
		
		#self.tbdelegate = TouchBarDelegate.alloc().init()
		
		try:
			if customization_identifier:
				tb.setCustomizationIdentifier_(customization_identifier)
		except:
			traceback.print_exc()
			
		tb.setDelegate_(tbdelegate)
		tb.setDefaultItemIdentifiers_([item.id for item in touchbar_items])
		tb.setCustomizationAllowedItemIdentifiers_([item.id for item in touchbar_items_id.values() if item.customization_mode == 1])
		tb.setCustomizationRequiredItemIdentifiers_([item.id for item in touchbar_items_id.values() if item.customization_mode == 2])
		
		if touchbar_escape_item:
			tb.setEscapeKeyReplacementItemIdentifier_(touchbar_escape_item.id)
			
		if DEBUG_LEVEL == 1:
			print ('TouchBar initialized')
			
			
		return tb
	
		
	
		
class TouchBarDelegate(NSObject):
	'''
	A TouchBarDelegate that will create and render touchbar from its content-list items's id
	'''
	def touchBar_makeItemForIdentifier_(self, bar, ident):
		global touchbar_items_id, touchbar_items, DEBUG_LEVEL
		
		if DEBUG_LEVEL == 1:	
			print ('touchBar_makeItemForIdentifier_ : '+ ident)
			
		if ident not in touchbar_items_id.keys():
			warnings.warn("Requested ID that doesn't belong to any TouchbarItem", InternalWarning)
			return
		
		item = touchbar_items_id[ident].makeItem()
		if DEBUG_LEVEL == 1:
			print ("Item: ",item)
		return item
	
	
	
def set_customization_identifier(identifier, menu = None):
	'''
	Prepare the TouchBar to be customizable.
	Give it an identifier (which will allow the user customization to be saved), and indicate if the app menu
	should have a "Customize TouchBar" menu-item.

	Parameters:
		identifier (str) : TouchBar identifier (https://developer.apple.com/documentation/appkit/nstouchbar/2544730-customizationidentifier?language=objc)
		menu (Bool / None) : Set a "Customize TouchBar" menu item (None = unchanged)
	'''
	global customization_identifier
	customization_identifier = identifier
	
	if menu is not None:
		NSApplication.sharedApplication().setAutomaticCustomizeTouchBarMenuItemEnabled_(menu)
	
		
		

	

def set_touchbar(items, define = [], esc_key = None):
	'''
	Set the content of the touchbar
	
	Parameters:
		- items ( [TouchBarItem class instances] ) : The items that will be presented in the touchbar
	'''
	
	global touchbar_items_id, touchbar_items, touchbar_escape_item
	
	touchbar_items = items
	touchbar_items_id = {}
	
	if esc_key:
		touchbar_escape_item = esc_key
		touchbar_items_id[esc_key.id] = esc_key
		
	for item in items:
		touchbar_items_id[item.id] = item
		
	for item in define:
		touchbar_items_id[item.id] = item
		

def customize(sender = None):
	'''
	Toggle the TouchBar Customization Palette.

	Parameters:
		sender (Any = None) : Sender of the action: will be passed to the ObjC method. (Not really useful, you should keep it None)
	'''
	NSApplication.sharedApplication().toggleTouchBarCustomizationPalette_(sender)
	
	
	
global delegate, window_controllers

window_controllers = []
tbdelegate = TouchBarDelegate.alloc().init()

def notify(a):
	'''
	A function that will be called when a Tk window is opened. This is bined to the window in the prepare_tk_windows method
	'''
	global delegate, DEBUG_LEVEL
	make_crash = False
	
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))
		
	if make_crash:
		if DEBUG_LEVEL == 1:
			print ('Making crash')
		objc.informal_protocol('NSTouchBarProvider', selectors = [1]) # Make crash (don't know why, but it does.)
	
def reload_touchbar():
	'''
	Rebuild the touchbar, after a modification or a change in its content
	'''
	global delegate, window_controllers, DEBUG_LEVEL
	for controller in window_controllers:
		if DEBUG_LEVEL == 1:
			print ('Making new touchbar')
		controller.setTouchBar_(controller.touchBar())

def prepare_tk_windows(windows):
	'''
	This function is needed to prepare Tk window(s) to "host" a touchbar.
	Call this function before mainlooping the window.
	
	Parameters:
		- windows ( [Tk] or Tk) : A Tk instance OR a list of Tk instances
	'''
	global delegate
	if isinstance(windows, list):
		for window in windows:
			window.bind("<Map>", notify)
	else:
		prepare_tk_windows([windows])
		
def resetPreparedWindows():
	'''
	Clear touchbar from all windows
	'''
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))
		
def prepare_pygame():
	'''
		This function is needed to prepare Pygame window to "host" a touchbar.
		Call this function before mainlooping the pygame.
	'''
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		if window.windowController() == None:
			window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))

def set_touchbar_pygame():
	'''
	WIP
	'''
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		view = window.contentView().subviews()[0]


class TouchBarTk(Tk):
	'''
	A Tk subclassed to automatically be prepared to host a touchbar
	It takes same arguments as Tk
	'''
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		prepare_tk_windows(self)


if __name__ == '__main__':
	from . import tests
	tests.testTk()
	