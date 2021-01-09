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

from .action import Action
from .constants import *


main = None


# Base Classes
class TouchBarBaseItem(object):
	pass
	
class TouchBarItem(TouchBarBaseItem):
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
	
	def makeItem(self):
		item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		return item
	
	
	
	
# Item Definitions

class Space:
	'''
	A Space item is an empty item, its only purpose is to take place
	'''
	class Small(TouchBarBaseItem):
		def __init__(self, customication_mode = 0):
			self.id = "NSTouchBarItemIdentifierFixedSpaceSmall"
			self.customization_mode = customization_mode
			
	class Large(TouchBarBaseItem):
		def __init__(self, customication_mode = 0):
			self.id = "NSTouchBarItemIdentifierFixedSpaceLarge"
			self.customization_mode = customization_mode
			
	class Flexible(TouchBarBaseItem):
		'''
		A Flexible space is a space item that take all the space it can
		'''
		def __init__(self, customization_mode = 0):
			self.id = "NSTouchBarItemIdentifierFlexibleSpace"
			self.customization_mode = customization_mode
			
			
class Popover(TouchBarItem):
	'''
	A Popover item is an item that will act just like a "subtouchbar": is looks like a button that
	will present another touchbar content when pressed.
	
	Parameters:
		- title (String) : the title of the popover button
		- shows_close_button (Bool) : Optional: if true, a "x" button will be presented in the popover to close it
		- holdItems ([TouchBarItem]) : The list of touchbar items contained by the popover
	
	Methods:
		reload() : Reload the popover content
		open() : Open the popover
		close() : Close the popover
	'''
	
	
	def __init__(self, items, **kwargs):
		
		self.id = kwargs.get('id', str(uuid.uuid4()))
		
		
		self.title = kwargs.get('title','Popover')
		self.shows_close_button = kwargs.get('shows_close_button', True)
		self.holdItems = kwargs.get('hold', None)
		
		
		#self.main.tbdelegate = TouchBarDelegate.alloc().init()
		
		
		self.items = items
		self.item = NSPopoverTouchBarItem.alloc().init()
		
		self.customization_label = kwargs.get('customization_label', 'Popover')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
	def makeItem(self):
		
		#instanciedItems = list(map(lambda item: item.makeItem(), self.items))
		
		self.item = NSPopoverTouchBarItem.alloc().initWithIdentifier_(self.id)
		self.item.setShowsCloseButton_(self.shows_close_button)
		
		self.reload()
		
		
		self.item.setCollapsedRepresentationLabel_(self.title)
		
		
		self.item.setCustomizationLabel_(self.customization_label)
		return self.item
	
	
	def reload(self):
		
		
		self.secondaryTouchBar = NSTouchBar.alloc().init()
		self.holdTouchbar = NSTouchBar.alloc().init()
		self.secondaryTouchBar.setDelegate_(main.tbdelegate)
		self.holdTouchbar.setDelegate_(main.tbdelegate)
		
		for item in self.items:
			main.touchbar_items_id[item.id] = item
			
		self.secondaryTouchBar.setDefaultItemIdentifiers_(list(map(lambda item: item.id, self.items)))
		self.item.setPopoverTouchBar_(self.secondaryTouchBar)
		
		if self.holdItems:
			for item in self.holdItems:
				main.touchbar_items_id[item.id] = item
				
			self.holdTouchbar.setDefaultItemIdentifiers_(list(map(lambda item: item.id, self.holdItems)))
			self.item.setPressAndHoldTouchBar_(self.holdTouchbar)
			
			
	def open(self, *dontcare):
		self.item.showPopover_(None)
		
	def close(self, *dontcare):
		self.item.dismissPopover_(None)
		
		
class Group(TouchBarItem):
	def __init__(self, items, id = str(uuid.uuid4()), customization_label = "Group", customization_mode = 0):
		self.id = id
		
		self.customization_label = customization_label
		self.customization_mode = customization_mode
		
		self.items = items
		
	def makeItem(self):
		instanciedItems = list(map(lambda item: item.makeItem(), self.items))
		
		self.item = NSGroupTouchBarItem.groupItemWithIdentifier_items_(self.id, instanciedItems)
		self.item.setCustomizationLabel_(self.customization_label)
		return self.item
	
	
class CustomNSView(TouchBarItem):
	def __init__(self, view):
		self.id = str(uuid.uuid4())
		
		self.item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		self.item.setCustomizationLabel_("Custom View")
		#self.item.view().addSubview_(view)
		self.item.setView_(view)
		
		
	def makeItem(self):		
		return self.item
	
	
class Label(TouchBarItem):
	'''
	A popover is a touchbar item that will present text.
	
	Parameters:
		- text (String) : The string to be presented
		- text_color ( (r, g, b, a) or Color constant, optional) : The foreground color of the text
		- alignment (Alignment constant, optional) : Where the text needs to be presented in the item
		- font_name (String, optional) : The font family name
		- font_size (Int, optional) : The size of the font in pts
	'''
	
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		self.label = None
		
		self.textBase = NSString(kwargs.get('text','Label'))
		self.text_color_ = kwargs.get('text_color',Color.white)
		self.alignment_ = kwargs.get('alignment',Alignment.center)
		self.font_name_ = kwargs.get('font', "Arial")
		self.font_size_ = kwargs.get('font_size', 16)
		
		self.customization_label = kwargs.get('customization_label', 'Label')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
	def makeItem(self):
		item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		
		self.label = NSTextField.labelWithString_(self.textBase)
		self.label.setTextColor_(NSColor.colorWithRed_green_blue_alpha_( * self.text_color_))
		self.label.setAlignment_(self.alignment_)
		font = NSFont.fontWithName_size_(self.font_name_,self.font_size_)
		
		item.setView_(self.label)
		item.setCustomizationLabel_(self.customization_label)
		
		return item
	
	# Properties
	#	# Text
	def textGetter(self):
		return self.label.stringValue()
	
	def textSetter(self, newValue):
		if self.label:
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
	
	
class Button(TouchBarItem):
	'''
	A Button is an item that will call an action when tapped
	It can shows text, image or both.
	
	Parameters:
		- title (String, optional) : The text that will be shown on the button
		- color ( (r, g, b, a) or Color constant, optional) : The background color of the button
		- image (String, optional) : The path of the image file that will be shown on the button
		- image_position (ImagePosition constant, optional) : The position of the image compared to the text
		- image_scale (ImageScale constant) : The image scaling
		- action ( function(self) ) : The action that will be called when button is pressed
	'''
	
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		
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
		
		self.customization_label = kwargs.get('customization_label', 'Button')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
	def makeItem(self):
		
		item = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		title = self.title_ if self.title_ else ''
		self.button = NSButton.buttonWithTitle_target_action_(title, self.actionManager ,"buttonPressed:")
		
		if self.image_:
			image = NSImage.alloc().initByReferencingFile_(os.path.realpath(self.image_))
			self.button.setImage_(image)
			
		self.button.setImagePosition_(self.image_position)
		self.button.setImageScaling_(self.image_scale)
		
		self.button.setIdentifier_(str(id(self)))
		main.buttonIds[str(id(self))] = self
		
		if self.color_:
			self.button.setBezelColor_(NSColor.colorWithRed_green_blue_alpha_( * self.color_))
			
		item.setCustomizationLabel_(self.customization_label)
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
	
	
class SegmentedControls(TouchBarItem):
	'''
	A SegmentedControls item if a group of several buttons that can act one of the folowing way:
		- Multiple buttons grouped
		- Select one of the buttons
		- Select several buttons of the group
	It can be populate with strings (which will just act like buttons title), or with 
		SegmentedControls.Control that allows to create more complex buttons.
		
	Parameters:
		- controls ([String and/or SegmentedControls.Control]) : Controls of the SegmentedControls
		- type (SegmentedControls.Type enum constant) : How the SegControls will act (see list up there)
		- action ( function(self) ) : Action that will be called when the user press/select a control
		
	Methods:
		- sc.selectedItems() -> [SegmentedControls.Control] : When called, will return the list containing every selected controls
	'''
	class Control(object):
		'''
		A SegmentedControls.Control] is a SegmentedControls button more complex than just a title.
		You can add image to it, change its width and more.
		
		Parameters:
			- title (String, optional) : Text that will be shown on the control
			- image (String, optional) : The image file path to show on the button
			- width (Int, optional) : The width of the button in pxs
			- enabled (Bool) : If False, the button will be grayed out and not clickable
			- selected (Bool) : Is the button currently selected?
			- image_scale (ImageScale constant) : The image scaling
		'''
		
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
		''' How the Seg Controls will act'''
		select_one = 0
		select_any = 1
		momentary = 2
		
	def __init__(self, controls = ["Segmented","Controls"], **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		
		self.controls = controls
		self.initializedControls = []
		self.type = kwargs.get('type', SegmentedControls.Type.select_one)
		
		self.actionManager = Action.alloc().init()
		self.action = kwargs.get('action', None)
		
		self.customization_label = kwargs.get('customization_label', 'Segmented Controls')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
	def makeItem(self):
		
		
		customItem = NSCustomTouchBarItem.alloc().initWithIdentifier_(self.id)
		self.initializedControls = []
		
		segmentedControl = NSSegmentedControl.segmentedControlWithLabels_trackingMode_target_action_([], self.type, self.actionManager ,"buttonPressed:")
		self.NSSegmentedControl = segmentedControl
		segmentedControl.setSegmentCount_(len(self.controls))
		
		
		for idx, control in enumerate(self.controls):
			if isinstance(control, SegmentedControls.Control):
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
				initializedControl = SegmentedControls.Control(title = str(control))
				initializedControl.index = idx
				initializedControl.segmentedControl = self
				self.initializedControls.append(initializedControl)
				
				segmentedControl.setLabel_forSegment_(str(control), idx)
				
		self.controls = self.initializedControls
		
		
		segmentedControl.setIdentifier_(str(id(self)))
		main.buttonIds[str(id(self))] = self
		customItem.setCustomizationLabel_(self.customization_label)
		customItem.setView_(segmentedControl)
		
		return customItem
	
	
	def selectedItems(self):
		for item in self.initializedControls:
			if item.selected:
				yield item
				
				
				
class ColorPicker(TouchBarItem):
	'''
	A ColorPicker item is a button that when it is pressed, will display a color selector in the touchbar.
	It is used in Word or Pages to set font color for example
	
	Parameters:
		- alpha (Bool) : If True, user can change r, g, b AND alpha value. If False, just r, g, b.
		- type (ColorPicker.Type constant) : The style of the ColorPicker button
		- image (string) : If type == Type.image, the button will present an image, the path of its file is this parameter.
		- action ( function(self) ) : A method that will be called when user change the color value
		- color ( (r, g, b, a) or Color constant) : The current color of the picker.
	'''
	
	class Type:
		''' The style of the ColorPicker button'''
		color = 0
		text = 1
		stroke = 2
		image = 3
		
		
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		
		self.alpha = kwargs.get('alpha', False)
		self.type = kwargs.get('type', ColorPicker.Type.color)
		
		self.image = kwargs.get('image', None)
		
		self.actionManager = Action.alloc().init()
		self.actionManager.__dict__
		self.action = kwargs.get('action', None)
		
		self.customization_label = kwargs.get('customization_label', 'Color Picker')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
		
	def makeItem(self):
		
		
		try:
			self.item
		except:
			if self.type == ColorPicker.Type.color:
				self.item = NSColorPickerTouchBarItem.colorPickerWithIdentifier_(self.id)
			elif self.type == ColorPicker.Type.text:
				self.item = NSColorPickerTouchBarItem.textColorPickerWithIdentifier_(self.id)
			elif self.type == ColorPicker.Type.stroke:
				self.item = NSColorPickerTouchBarItem.strokeColorPickerWithIdentifier_(self.id)
			elif self.type == ColorPicker.Type.image:
				image = NSImage.alloc().initByReferencingFile_(os.path.realpath(self.image))
				self.item = NSColorPickerTouchBarItem.colorPickerWithIdentifier_buttonImage_(self.id, image)
				
				
		self.item.setShowsAlpha_(self.alpha)
		
		self.item.setTarget_(self.actionManager)
		self.item.setAction_("buttonPressed:")
		
		main.buttonIds[self.id] = self
		
		self.item.setCustomizationLabel_(self.customization_label)
		
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
	
	
	
class Slider(TouchBarItem):
	'''
	A Slider is an item that will allows the user to change a number value by dragging a control over the touchbar.
	
	Parameters:
		- title (String, optional) : A text that will be presented next to the slider
		- value (Float) : The value of the slider, between 0 and 1
		- color ( (r, g, b, a) or Color constant, optional) : The tint color of the slider
		- action ( function(self) ) : The function that will be called when the user change the value of the slider
	''' 
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		self.makeNumber = 0
		
		self.title = kwargs.get('title', '')
		
		self.actionManager = Action.alloc().init()
		self.actionManager.__dict__
		self.action = kwargs.get('action', None)
		self.defaultValue = kwargs.get('value',0.5)
		
		self.color = kwargs.get('color', None)
		
		self.item = NSSliderTouchBarItem.alloc().initWithIdentifier_(self.id)
		
		self.customization_label = kwargs.get('customization_label', 'Slider')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
	def makeItem(self):
		
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
		main.buttonIds[str(id(self))] = self
		
		self.item.setCustomizationLabel_(self.customization_label)
		return self.item
	
	def getValue(self):
		return float(self.item.slider().doubleValue())
	
	def setValue(self, value):
		self.item.slider().setDoubleValue_(float(value))
		
	value = property(getValue, setValue)
	
	
	
class Stepper(TouchBarItem):
	'''
	A stepper is an item that will allow the user to select a numeric value between specified min and max.
	If will contain a label showing the current value, and two buttons + and - to change the value from specified step.

	Parameters:
		- value (int) : Value of the stepper
		- min (int) : Minimum value
		- max (int) : Maximum value
		- step (int) : Increment step
		- action ( function(self) ) : The function that will be called when the user change the value of the stepper
	'''
	def __init__(self, **kwargs):
		self.id = kwargs.get('id', str(uuid.uuid4()))
		
		self.actionManager = Action.alloc().init()
		self.actionManager.__dict__
		self.action = kwargs.get('action', None)
		
		self.defaultValue = kwargs.get('value', 5)
		self.defaultMin = kwargs.get('min', 0)
		self.defaultMax = kwargs.get('max', 10)
		self.defaultStep = kwargs.get('step', 1)
		
		self.item = NSStepperTouchBarItem.alloc().initWithIdentifier_(self.id)
		self.item.setValue_(float(self.defaultValue))
		self.item.setMinValue_(self.defaultMin)
		self.item.setMaxValue_(self.defaultMax)
		self.item.setIncrement_(self.defaultStep)
		
		self.customization_label = kwargs.get('customization_label', 'Stepper')
		self.customization_mode = kwargs.get('customization_mode', 0)
		
		
		
	def makeItem(self):
		
		
		self.item.setTarget_(self.actionManager)
		self.item.setAction_("buttonPressed:")
		
		main.buttonIds[self.id] = self
		
		self.item.setCustomizationLabel_(self.customization_label)
		return self.item
	
	
	# Properties
	#	# Value
	def getValue(self):
		return float(self.item.value())
	
	def setValue(self, value):
		self.item.setValue_(float(value))
		
	value = property(getValue, setValue)
	
	#	# Max
	def getMax(self):
		return float(self.item.maxValue())
	
	def setMax(self, value):
		self.item.setMaxValue_(float(value))
		
	max = property(getMax, setMax)
	
	#	# Min
	def getMin(self):
		return float(self.item.minValue())
	
	def setMin(self, value):
		self.item.setMinValue_(float(value))
		
	min = property(getMin, setMin)
	
	#	# Step
	def getStep(self):
		return float(self.item.increment())
	
	def setStep(self, value):
		self.item.setIncrement_(float(value))
		
	step = property(getStep, setStep)