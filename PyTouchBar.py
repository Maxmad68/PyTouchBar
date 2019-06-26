#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


from tkinter import *
import os
import uuid

import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import Cocoa

global DEBUG_LEVEL, buttonIds, tbdelegate
DEBUG_LEVEL = 0

buttonIds = {}

__author__ = "Maxime Madrau (maxime@madrau.fr)"

# Constants

class Color:
	green = (0,1,0,1)
	blue = (0,0,1,1)
	red = (1,0,0,1)
	yellow = (1,1,0,1)
	orange = (1,0.5,0,1)
	purple = (1,0,1,1)
	cyan = (0,1,1,1)
	white = (1,1,1,1)
	black = (0,0,0,1)
	clear = (1,1,1,0)
	
class ImagePosition:
	noimage = 0
	imageonly = 1
	left = 2
	right = 3
	below = 4
	above = 5
	overlaps = 6
	
class ImageScale:
	proportionnaly_down = 0
	axes_independently = 1
	none = 2
	proportionnaly_up_or_down = 3
	
class Alignment:
	left = 0
	right = 1
	center = 2
	justified = 3
	natural = 4
	
class ColorPickerType:
	color = 0
	text = 1
	stroke = 2
	image = 3
	
# TouchBar Items	


class TouchBarSpace:
	class Small(object):
		def __init__(self):
			self.id = "NSTouchBarItemIdentifierFixedSpaceSmall"
			
	class Large(object):
		def __init__(self):
			self.id = "NSTouchBarItemIdentifierFixedSpaceLarge"
						
	class Flexible(object):
		def __init__(self):
			self.id = "NSTouchBarItemIdentifierFlexibleSpace"
			
			
class TouchBarPopover(object):
	def __init__(self, items, **kwargs):
		global tbdelegate
		self.id = str(uuid.uuid4())

		self.title = kwargs.get('title','Popover')
		self.shows_close_button = kwargs.get('shows_close_button', True)
		self.holdItems = kwargs.get('hold', None)


		#self.tbdelegate = TouchBarDelegate.alloc().init()
		
		
		self.items = items
		self.item = NSPopoverTouchBarItem.alloc().init()
		

	def makeItem(self):
		global touchbar_items_id
		#instanciedItems = list(map(lambda item: item.makeItem(), self.items))

		self.item = NSPopoverTouchBarItem.alloc().init()
		self.item.setShowsCloseButton_(self.shows_close_button)
		
		self.reload()

		
		self.item.setCollapsedRepresentationLabel_(self.title)
		

		self.item.setCustomizationLabel_(self.id)
		return self.item
		
	def reload(self):
		global touchbar_items_id, tbdelegate
		
		self.secondaryTouchBar = NSTouchBar.alloc().init()
		self.holdTouchbar = NSTouchBar.alloc().init()
		self.secondaryTouchBar.setDelegate_(tbdelegate)
		self.holdTouchbar.setDelegate_(tbdelegate)
		
		for item in self.items:
			touchbar_items_id[item.id] = item
			
		self.secondaryTouchBar.setDefaultItemIdentifiers_(list(map(lambda item: item.id, self.items)))
		self.item.setPopoverTouchBar_(self.secondaryTouchBar)
		
		if self.holdItems:
			for item in self.holdItems:
				touchbar_items_id[item.id] = item
				
			self.holdTouchbar.setDefaultItemIdentifiers_(list(map(lambda item: item.id, self.holdItems)))
			self.item.setPressAndHoldTouchBar_(self.holdTouchbar)
		
		
	def open(self, *dontcare):
		self.item.showPopover_(None)
		
	def close(self, *dontcare):
		self.item.dismissPopover_(None)
		

class TouchBarGroup(object):
	def __init__(self, items):
		self.id = str(uuid.uuid4())

		self.items = items

	def makeItem(self):
		instanciedItems = list(map(lambda item: item.makeItem(), self.items))

		self.item = NSGroupTouchBarItem.groupItemWithIdentifier_items_(self.id, instanciedItems)
		self.item.setCustomizationLabel_(self.id)
		return self.item



	
class TouchBarLabel(object):
	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self.text = NSString(kwargs.get('text','Label'))
		self.text_color = kwargs.get('text_color',Color.white)
		self.alignment = kwargs.get('alignment',Alignment.center)
		self.font_name = kwargs.get('font', "Arial")
		self.font_size = kwargs.get('font_size', 16)
		
	def makeItem(self):
		item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		
		label = NSTextField.labelWithString_(self.text)
		label.setTextColor_(NSColor.colorWithRed_green_blue_alpha_( * self.text_color))
		label.setAlignment_(self.alignment)
		font = NSFont.fontWithName_size_(self.font_name,self.font_size)

		item.setView_(label)
		item.setCustomizationLabel_(self.id)

		return item
		

class TouchBarButton(object):
	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		
		self.title = kwargs.get('title', None)
		self.color = kwargs.get('color', None)
	
		self.image = kwargs.get('image',None)

		# Image
		if self.image:
			defaultPosition = ImagePosition.left
		else:
			defaultPosition = ImagePosition.noimage
			
		self.image_position = kwargs.get('image_position', defaultPosition)
		self.image_scale = kwargs.get('image_scale', 0)

		self.actionManager = Action.alloc().init()
		self.action = kwargs.get('action', None)

		
	def makeItem(self):
		global buttonIds
		item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		title = self.title if self.title else ''
		button = NSButton.buttonWithTitle_target_action_(title, self.actionManager ,"buttonPressed:")
		
		if self.image:
			image = NSImage.alloc().initByReferencingFile_(os.path.realpath(self.image))
			button.setImage_(image)
			
		button.setImagePosition_(self.image_position)
		button.setImageScaling_(self.image_scale)
		
		button.setIdentifier_(str(id(self)))
		buttonIds[str(id(self))] = self
		
		if self.color:
			button.setBezelColor_(NSColor.colorWithRed_green_blue_alpha_( * self.color))
				
		item.setCustomizationLabel_(self.id)
		item.setView_(button)
		
		return item
		
class TouchBarColorPicker(object):
	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		
		self.alpha = kwargs.get('alpha', False)
		self.type = kwargs.get('type', ColorPickerType.color)
		
		self.image = kwargs.get('image', None)

		self.actionManager = Action.alloc().init()
		self.actionManager.__dict__
		self.action = kwargs.get('action', None)


		
	def makeItem(self):
		global buttonIds
				
		try:
			self.item
		except:
			if self.type == ColorPickerType.color:
				self.item = NSColorPickerTouchBarItem.colorPickerWithIdentifier_(self.id)
			elif self.type == ColorPickerType.text:
				self.item = NSColorPickerTouchBarItem.textColorPickerWithIdentifier_(self.id)
			elif self.type == ColorPickerType.stroke:
				self.item = NSColorPickerTouchBarItem.strokeColorPickerWithIdentifier_(self.id)
			elif self.type == ColorPickerType.image:
				image = NSImage.alloc().initByReferencingFile_(os.path.realpath(self.image))
				self.item = NSColorPickerTouchBarItem.colorPickerWithIdentifier_buttonImage_(self.id, image)

		
		self.item.setShowsAlpha_(self.alpha)
		
		self.item.setTarget_(self.actionManager)
		self.item.setAction_("buttonPressed:")

		buttonIds[self.id] = self
				
		self.item.setCustomizationLabel_(self.id)
		
		return self.item

	def getColor(self):
		color = self.item.color()
		alpha = color.alphaComponent()
		red = color.redComponent()
		green = color.greenComponent()
		blue = color.blueComponent()
		return (red, green, blue, alpha)
		
	def setColor(self, color):
		color = NSColor.NSColor.colorWithRed_green_blue_alpha_( * color)
		self.item.setColor_(color)
		
	color = property(getColor, setColor)



class TouchBarSlider(object):
	def __init__(self, image = None, **kwargs):
		self.id = str(uuid.uuid4())
		self.makeNumber = 0
		
		self.title = kwargs.get('title', '')

		self.actionManager = Action.alloc().init()
		self.actionManager.__dict__
		self.action = kwargs.get('action', None)
		
		self.defaultValue = kwargs.get('value',0.5)
		
		self.color = kwargs.get('color', None)
		
		self.item = NSSliderTouchBarItem.alloc().init()	

		
	def makeItem(self):
		global buttonIds
		self.makeNumber += 1
		if self.makeNumber == 1:
			self.setValue(self.defaultValue)
			
		if self.color:	
			self.item.slider().setTrackFillColor_(NSColor.colorWithRed_green_blue_alpha_( * self.color))
		
		self.item.setTarget_(self.actionManager)
		self.item.setAction_("buttonPressed:")
		
		self.item.setLabel_(self.title)
		
		self.item.slider().setMinValue_(0)
		self.item.slider().setMaxValue_(1)
		

		self.item.slider().setIdentifier_(str(id(self)))
		buttonIds[str(id(self))] = self
				
		self.item.setCustomizationLabel_(self.id)
		
		return self.item
	
	def getValue(self):
		return float(self.item.slider().doubleValue())
		
	def setValue(self, value):
		self.item.slider().setDoubleValue_(float(value))
		
	value = property(getValue, setValue)
		

class Action(NSObject):
	def buttonPressed_(self, view):
		global buttonIds, DEBUG_LEVEL
		if DEBUG_LEVEL == 1:
			print (buttonIds)
			print (view)
		
		if isinstance(view, NSSliderTouchBarItem):
			view = view.slider()	
			
		instance = buttonIds[str(view.identifier())]

		if instance.action:
			instance.action.__call__(instance)

	
class NSWindowControllerTBModified (NSWindowController):
	def touchBar(self):
		global DEBUG_LEVEL, buttonIds, touchbar_items_id, touchbar_items, tbdelegate
		if DEBUG_LEVEL == 1:
			print ('TouchBar initializing') 
			
		tb = NSTouchBar.alloc().init()
		#self.tbdelegate = TouchBarDelegate.alloc().init()
		tb.setDelegate_(tbdelegate)
		tb.setDefaultItemIdentifiers_(list(map(lambda item: item.id, touchbar_items)))
		
		if DEBUG_LEVEL == 1:
			print ('TouchBar initialized')
			
			
		return tb
		
	
		
class TouchBarDelegate(NSObject):
	def touchBar_makeItemForIdentifier_(self, bar, ident):
		global touchbar_items_id, touchbar_items, DEBUG_LEVEL
			
		if DEBUG_LEVEL == 1:	
			print ('touchBar_makeItemForIdentifier_ : '+ ident)
			
		return touchbar_items_id[ident].makeItem()
		
		

	

def set_touchbar(items):
	global touchbar_items_id, touchbar_items
	
	touchbar_items = items
	touchbar_items_id = {}
	
	for item in items:
		touchbar_items_id[item.id] = item
	
	
	
	
global delegate, window_controllers

window_controllers = []
tbdelegate = TouchBarDelegate.alloc().init()

def notify(a):
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
	global delegate, window_controllers, DEBUG_LEVEL
	for controller in window_controllers:
		if DEBUG_LEVEL == 1:
			print ('Making new touchbar')
		controller.setTouchBar_(controller.touchBar())

def prepare_tk_windows(windows):
	global delegate
	if isinstance(windows, list):
		for window in windows:
			window.bind("<Map>", notify)
	else:
		prepare_tk_windows([windows])
		
def prepare_pygame():
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		if window.windowController() == None:
			window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))




def test_pygame():
	import pygame
		
	def lol(item):
			button1.title = 'Bonsoir'
			reload_touchbar()
			
	def buh(item):
		print ('buh!')
		
	button1 = TouchBarButton(title="Coucou",action=lol)
	button2 = TouchBarButton(title="Bouh",action=buh, color = Color.cyan)

	set_touchbar([button1,button2])

	pygame.init()

	surface = pygame.display.set_mode((100,200))
	prepare_pygame()
	pygame.display.set_caption('Coucou')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Quit event (sent by red-cross-button)
				pygame.quit()
				break

def test_tk():
	def lol(item):
		button2.title = 'Changé'
		popover.reload()
		reload_touchbar()
		
	def buh(item):
		popover.close()
		
	def openpop(item):
		popover.open()
		
	button1 = TouchBarButton(title="Coucou",action=openpop,image='/Volumes/SHARED/ISN Jeu/Ressources/Tiles/box.png', image_scale = ImageScale.proportionnaly_up_or_down)
	button2 = TouchBarButton(title= "Bouh",action=buh, color = Color.cyan)
	#label1 = TouchBarLabel(text="bjr")
	cpk = TouchBarColorPicker(type=ColorPickerType.image, action = buh, image='/Volumes/SHARED/ISN Jeu/Ressources/Tiles/box.png')
	sld = TouchBarSlider(value = 0.2)
	spc = TouchBarSpace.Small()
	
	l = []
	for i in range(4):
		l.append(TouchBarButton(title= "Test %i"%i,action=buh))
	group = TouchBarGroup(l)
	popover = TouchBarPopover([button2], title = "Salut", shows_close_button = True, hold=[group])
	
	
	
	fen = Tk()

	
	prepare_tk_windows(fen)
	set_touchbar([button1,button2])


	
	def change():
		button1.title = 'Bonsoir'
		reload_touchbar()
	
	bouton = Button(fen, text="Change text", command = change)
	bouton.pack()

	fen.mainloop()
	
	



if __name__ == '__main__':
	fen = Tk()
	prepare_tk_windows(fen)
	lbl1 = TouchBarLabel(text="Coucou")
	lbl2 = TouchBarLabel(text="Bonjour")
	set_touchbar([lbl1, TouchBarSpace.Flexible(), lbl2])

	fen.mainloop()