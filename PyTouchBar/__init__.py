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

global DEBUG_LEVEL, buttonIds, tbdelegate, touchbar_items
DEBUG_LEVEL = 0

buttonIds = {}
touchbar_items = []

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
	
# TouchBar Items	



			
class TouchBarItems:	
	
	class Space:
		class Small(object):
			def __init__(self):
				self.id = "NSTouchBarItemIdentifierFixedSpaceSmall"
				
		class Large(object):
			def __init__(self):
				self.id = "NSTouchBarItemIdentifierFixedSpaceLarge"
							
		class Flexible(object):
			def __init__(self):
				self.id = "NSTouchBarItemIdentifierFlexibleSpace"
						
	class Popover(object):
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

			self.item = NSPopoverTouchBarItem.alloc().initWithIdentifier_(self.id)
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
			

	class Group(object):
		def __init__(self, items):
			self.id = str(uuid.uuid4())

			self.items = items

		def makeItem(self):
			instanciedItems = list(map(lambda item: item.makeItem(), self.items))

			self.item = NSGroupTouchBarItem.groupItemWithIdentifier_items_(self.id, instanciedItems)
			self.item.setCustomizationLabel_(self.id)
			return self.item


	class CustomNSView(object):
		def __init__(self, view):
			self.id = str(uuid.uuid4())
			
			self.item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
			self.item.setCustomizationLabel_(self.id)
			#self.item.view().addSubview_(view)
			self.item.setView_(view)


		def makeItem(self):		
			return self.item

		
	class Label(object):
		def __init__(self, **kwargs):
			self.id = str(uuid.uuid4())
			self.textBase = NSString(kwargs.get('text','Label'))
			self.text_color_ = kwargs.get('text_color',Color.white)
			self.alignment_ = kwargs.get('alignment',Alignment.center)
			self.font_name_ = kwargs.get('font', "Arial")
			self.font_size_ = kwargs.get('font_size', 16)
			
		def makeItem(self):
			item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
			
			self.label = NSTextField.labelWithString_(self.textBase)
			self.label.setTextColor_(NSColor.colorWithRed_green_blue_alpha_( * self.text_color_))
			self.label.setAlignment_(self.alignment_)
			font = NSFont.fontWithName_size_(self.font_name_,self.font_size_)

			item.setView_(self.label)
			item.setCustomizationLabel_(self.id)

			return item
			
		# Properties
		#	# Text
		def textGetter(self):
			return self.label.stringValue()
		
		def textSetter(self, newValue):
			self.label.setStringValue_(NSString(newValue))
			
		text = property(textGetter, textSetter)
		
		#	#Text Color
		def textColorGetter(self):
			return self.text_color_
		
		def textColorSetter(self, newValue):
			self.label.setTextColor_(NSColor.colorWithRed_green_blue_alpha_( * newValue))
			self.text_color_ = newValue
			
		text_color = property(textColorGetter, textColorSetter)
		
		#	#Font
		def fontGetter(self):
			return self.font_name_
		
		def fontSetter(self, newValue):
			font = NSFont.fontWithName_size_(newValue,newValue)
			self.label.setFont_(font)
			self.font_name_ = newValue
			
		font_name = property(fontGetter, fontSetter)
		
		#	#Font Size
		def fontSizeGetter(self):
			return self.font_size_
		
		def fontSizeSetter(self, newValue):
			font = NSFont.fontWithName_size_(self.font_name_,newValue)
			self.label.setFont_(font)
			self.font_size_ = newValue
			
		font_size = property(fontSizeGetter, fontSizeSetter)
		
		#	# Alignment
		def alignmentGetter(self):
			return self.alignment_
		
		def alignmentSetter(self, newValue):
			self.label.setAlignment_(newValue)
			self.alignment_ = newValue
			
		alignment = property(alignmentGetter, alignmentSetter)
			

	class Button(object):
		def __init__(self, **kwargs):
			self.id = str(uuid.uuid4())
			
			self.title_ = kwargs.get('title', None)
			self.color_ = kwargs.get('color', None)
		
			self.image_ = kwargs.get('image',None)

			# Image
			if self.image_:
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
			title = self.title_ if self.title_ else ''
			self.button = NSButton.buttonWithTitle_target_action_(title, self.actionManager ,"buttonPressed:")
			
			if self.image_:
				image = NSImage.alloc().initByReferencingFile_(os.path.realpath(self.image_))
				self.button.setImage_(image)
				
			self.button.setImagePosition_(self.image_position)
			self.button.setImageScaling_(self.image_scale)
			
			self.button.setIdentifier_(str(id(self)))
			buttonIds[str(id(self))] = self
			
			if self.color_:
				self.button.setBezelColor_(NSColor.colorWithRed_green_blue_alpha_( * self.color_))
					
			item.setCustomizationLabel_(self.id)
			item.setView_(self.button)
			
			return item
			
		# Properties
		#	# Title
		def titleGetter(self):
			return self.title_
		
		def titleSetter(self, newValue):
			self.button.setTitle_(NSString(newValue))
			self.title_ = newValue
			
		title = property(titleGetter, titleSetter)
		
		#	#Color
		def colorGetter(self):
			return self.color_
		
		def colorSetter(self, newValue):
			self.button.setBezelColor_(NSColor.colorWithRed_green_blue_alpha_( * newValue))
			self.color_ = newValue
			
		color = property(colorGetter, colorSetter)
		
		#	#Image
		def imageGetter(self):
			return self.image_
		
		def imageSetter(self, newValue):
			image = NSImage.alloc().initByReferencingFile_(os.path.realpath(newValue))
			self.button.setImage_(image)
			self.image_ = newValue
			
		image = property(imageGetter, imageSetter)
			
			
	class SegmentedControls(object):
		class Control(object):
			def __init__(self, **kwargs):
				self.title_ = kwargs.get('title', 'Control')
				imageName = kwargs.get('image', None)
				
				if imageName:
					self.image = NSImage.alloc().initByReferencingFile_(os.path.realpath(imageName))
				else:
					self.image = None
					
				self.imageScaling = kwargs.get('image_scale', ImageScale.none)
				self.width = kwargs.get('width', None)
				self.enabled_ = kwargs.get('enabled', True)
				self.selectedBase = kwargs.get('selected', False)
				
				self.index = -1
				self.segmentedControl = None
					
			
			def isSelected(self):
				if self.segmentedControl == None:
					raise SystemError("Can't check selection until TouchBar is presented")
				else:
					return self.segmentedControl.NSSegmentedControl.isSelectedForSegment_(self.index)
				
			def setSelected(self, status):
				if self.segmentedControl == None:
					raise SystemError("Can't set selection until TouchBar is presented")
				else:
					return self.segmentedControl.NSSegmentedControl.setSelected_forSegment_(status, self.index)
				
			selected = property(isSelected, setSelected)
			
			def titleGetter(self):
				return self.title_
			
			def titleSetter(self, newValue):
				self.title_ = newValue
				if self.segmentedControl:
					self.segmentedControl.NSSegmentedControl.setLabel_forSegment_(newValue, self.index)
				else:
					print ('i')
				
			title = property(titleGetter, titleSetter)
			
			def enabledGetter(self):
				return self.enabled_
			
			def enabledSetter(self, newValue):
				self.enabled_ = newValue
				if self.segmentedControl:
					self.segmentedControl.NSSegmentedControl.setEnabled_forSegment_(newValue, self.index)
				
			enabled = property(enabledGetter, enabledSetter)
			
			def __repr__(self):
				return ('<SegmentedControls.Item index = {idx}, title = "{title}">'.format(idx = self.index, title = self.title))
				
				
		class Type:
			select_one = 0
			select_any = 1
			momentary = 2
				
		def __init__(self, controls = ["Segmented","Controls"], **kwargs):
			self.id = str(uuid.uuid4())
			
			self.controls = controls
			self.initializedControls = []
			self.type = kwargs.get('type', TouchBarItems.SegmentedControls.Type.select_one)
			
			self.actionManager = Action.alloc().init()
			self.action = kwargs.get('action', None)

			
		def makeItem(self):
			global buttonIds

			customItem = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
			self.initializedControls = []

			segmentedControl = NSSegmentedControl.segmentedControlWithLabels_trackingMode_target_action_([], self.type, self.actionManager ,"buttonPressed:")
			self.NSSegmentedControl = segmentedControl
			segmentedControl.setSegmentCount_(len(self.controls))
			
			
			for idx, control in enumerate(self.controls):
				if isinstance(control, TouchBarItems.SegmentedControls.Control):
					self.initializedControls.append(control)
					control.index = idx
					control.segmentedControl = self
					segmentedControl.setLabel_forSegment_(control.title, idx)
					
					if control.image:
						segmentedControl.setImage_forSegment_(control.image, idx)
						segmentedControl.setImageScaling_forSegment_(control.imageScaling, idx)
					
					if control.width:
						segmentedControl.setWidth_forSegment_(control.width, idx)
					segmentedControl.setEnabled_forSegment_(control.enabled, idx)
					segmentedControl.setSelected_forSegment_(control.selectedBase, idx)
				
				else:
					initializedControl = TouchBarItems.SegmentedControls.Control(title = str(control))
					initializedControl.index = idx
					initializedControl.segmentedControl = self
					self.initializedControls.append(initializedControl)
					
					segmentedControl.setLabel_forSegment_(str(control), idx)
			
			self.controls = self.initializedControls					
					
					
			segmentedControl.setIdentifier_(str(id(self)))
			buttonIds[str(id(self))] = self
			customItem.setCustomizationLabel_(self.id)
			customItem.setView_(segmentedControl)
			
			return customItem
			
			
		def selectedItems(self):
			for item in self.initializedControls:
				if item.selected:
					yield item
			
			
			
	class ColorPicker(object):
		class Type:
			color = 0
			text = 1
			stroke = 2
			image = 3
			
			
		def __init__(self, **kwargs):
			self.id = str(uuid.uuid4())
			
			self.alpha = kwargs.get('alpha', False)
			self.type = kwargs.get('type', TouchBarItems.ColorPicker.Type.color)
			
			self.image = kwargs.get('image', None)

			self.actionManager = Action.alloc().init()
			self.actionManager.__dict__
			self.action = kwargs.get('action', None)


			
		def makeItem(self):
			global buttonIds
					
			try:
				self.item
			except:
				if self.type == TouchBarItems.ColorPicker.Type.color:
					self.item = NSColorPickerTouchBarItem.colorPickerWithIdentifier_(self.id)
				elif self.type == TouchBarItems.ColorPicker.Type.text:
					self.item = NSColorPickerTouchBarItem.textColorPickerWithIdentifier_(self.id)
				elif self.type == TouchBarItems.ColorPicker.Type.stroke:
					self.item = NSColorPickerTouchBarItem.strokeColorPickerWithIdentifier_(self.id)
				elif self.type == TouchBarItems.ColorPicker.Type.image:
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



	class Slider(object):
		def __init__(self, **kwargs):
			self.id = str(uuid.uuid4())
			self.makeNumber = 0
			
			self.title = kwargs.get('title', '')

			self.actionManager = Action.alloc().init()
			self.actionManager.__dict__
			self.action = kwargs.get('action', None)
			self.defaultValue = kwargs.get('value',0.5)
			
			self.color = kwargs.get('color', None)
			
			self.item = NSSliderTouchBarItem.alloc().initWithIdentifier_(self.id)

			
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
		
		item = touchbar_items_id[ident].makeItem()
		if DEBUG_LEVEL == 1:	
			print ("Item: ",item)
		return item
		
		

	

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
		
def resetPreparedWindows():
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))
		
def prepare_pygame():
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		if window.windowController() == None:
			window_controllers.append(NSWindowControllerTBModified.alloc().initWithWindow_(window))

def set_touchbar_pygame():
	windows = NSApplication.sharedApplication().windows()
	for window in windows:
		view = window.contentView().subviews()[0]


class TouchBarTk(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		prepare_tk_windows(self)


def testTk():
	fen = Tk()
		
	prepare_tk_windows(fen)
	btn = Button(fen, text="Hello")
	btn.pack()
	
	btn1 = TouchBarItems.SegmentedControls.Item(title='Hello', alignment = Alignment.left, selected = True, width = 100)
	btn2 = TouchBarItems.SegmentedControls.Item(title='World', alignment = Alignment.right, enabled = True, width = 100)
	
	def action(segCont):
		print (list(segCont.selectedItems()))
		pass
	
	segcon = TouchBarItems.SegmentedControls([
		btn1,
		btn2
	], action = action, type = TouchBarItems.SegmentedControls.Type.select_one)
	
	set_touchbar([segcon])
	
	#fen.set_touchbar()
	
	fen.mainloop()

if __name__ == '__main__':
	testTk()