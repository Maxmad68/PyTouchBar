#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def color_to_hex(color):
	
	if len(color) == 4:
		r, g, b, a = color
	else:
		r, g, b = color
		a = 0
		
	return '#' + str(hex(int(r * 255)))[2:].zfill(2) + str(hex(int(g * 255)))[2:].zfill(2) + str(hex(int(b * 255)))[2:].zfill(2)


def hex_to_color(hex):
	hex = hex.replace('#','')
	
	if len(hex) == 6:
		r = int(hex[:2], 16) / 255.
		g = int(hex[2:4], 16) / 255.
		b = int(hex[4:6], 16) / 255.
		a = 1.
		
	elif len(hex) == 8:
		r = int(hex[:2], 16) / 255.
		g = int(hex[2:4], 16) / 255.
		b = int(hex[4:6], 16) / 255.
		a = int(hex[6:8], 16) / 255.
		
	elif len(hex) == 3:
		r = int(hex[0], 16) / 15.
		g = int(hex[1], 16) / 15.
		b = int(hex[2], 16) / 15.
		a = 1.
		
	elif len(hex) == 4:
		r = int(hex[0], 16) / 15.
		g = int(hex[1], 16) / 15.
		b = int(hex[2], 16) / 15.
		a = int(hex[3], 16) / 15.
		
	elif len(hex) == 9:
		r = int(hex[:3], 16) / 4095.
		g = int(hex[3:6], 16) / 4095.
		b = int(hex[6:9], 16) / 4095.
		a = 1.
		
	elif len(hex) == 12:
		r = int(hex[:3], 16) / 4095.
		g = int(hex[3:6], 16) / 4095.
		b = int(hex[6:9], 16) / 4095.
		a = int(hex[9:12], 16) / 4095.

	return (r, g, b, a)



def color_to_255(color):
	comp255 = []
	
	for comp in color:
		comp255.append(comp * 255)
		
	return tuple(comp255)