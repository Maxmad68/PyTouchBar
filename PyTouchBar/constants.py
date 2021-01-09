#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CustomizationMode:
	none = 0
	allowed = 1
	required = 2
	
	
class Color:
	'''
	Some predefined and most used color constants
	'''
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
	'''
	Position of the image compared to the text
	'''
	noimage = 0
	imageonly = 1
	left = 2
	right = 3
	below = 4
	above = 5
	overlaps = 6
	
class ImageScale:
	'''
	Scale of an image in a touchbar item
	'''
	proportionnaly_down = 0
	axes_independently = 1
	none = 2
	proportionnaly_up_or_down = 3
	
class Alignment:
	'''
	Alignment of the text in the touchbar item
	'''
	left = 0
	right = 1
	center = 2
	justified = 3
	natural = 4