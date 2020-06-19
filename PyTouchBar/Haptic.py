#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Cocoa import NSHapticFeedbackManager


class Pattern:
	'''
	Levels of haptic feedbacks
	See https://developer.apple.com/documentation/appkit/nshapticfeedbackpattern
	'''
	generic = 0
	alignment = 1
	levelChange = 2
	
class Time:
	'''
	A time at which to provide haptic feedback to the user.
	See https://developer.apple.com/documentation/appkit/nshapticfeedbackmanager/performancetime
	'''
	default = 0
	now = 1
	drawCompleted = 2
	
def perform(pattern = Pattern.generic, time = Time.now):
	'''
	Perform an haptic feedback on supported devices trackpad.
	
	Parameters:
		- pattern (Pattern enum) : the level of the haptic feedback
		- time (Time enum) : A time at which to provide haptic feedback
	'''
	NSHapticFeedbackManager.defaultPerformer().performFeedbackPattern_performanceTime_(pattern, time)
