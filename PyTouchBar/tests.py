#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def testTk():
	fen = Tk()
	
	prepare_tk_windows(fen)
	btn = Button(fen, text="Hello")
	btn.pack()
	
	btn1 = TouchBarItems.SegmentedControls.Control(title='Hello', alignment = Alignment.left, selected = True, width = 100)
	btn2 = TouchBarItems.SegmentedControls.Control(title='World', alignment = Alignment.right, enabled = True, width = 100)
	
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