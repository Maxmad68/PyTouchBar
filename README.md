# PyTouchBar
A NSTouchBar Wrapper for Python. It olny works (for the moment) with Tkinter and PyGame.<br>
It mainly depends on PyObjc to wrap NSTouchBar and related classes.<br>
Note: It will (of course) only works on MacBook Pro with TouchBars, or on a TouchBar Simulator (<a href="https://github.com/sindresorhus/touch-bar-simulator">you have a good one here</a>.)

# How to use
Just download the PyToucbBar.py into your project directory, import it and that's it!

# Documentation
Well, this is the interesting part.<br>
First, you'll need to prepare windows for "hosting" a TouchBar.<br>
To do so, you're gonna use a command depending on the graphic module you are using (Tkinter of PyGame)

## Preparing windows 
##### Tkinter
If you are using Tkinter, you'll need to use this command:

    ptb.prepare_tk_windows(window1, window2, ...)
    
For example, a typical example would be:

    root = Tk()
    ptb.prepare_tk_windows(root)
    lbl = Label(root, text="Button")
    lbl.pack()
    root.mainloop()
    
##### Pygame
If you are using PyGame, you'll need to use this command just after setting the window parameters:

     ptb.prepare_pygame()
   
For example, a typical example would be:

    pygame.init()
    surface = pygame.display.set_mode((100,200))
	  prepare_pygame()
    
	  pygame.display.set_caption('Title')
    while True:
	  	for event in pygame.event.get():
			  if event.type == pygame.QUIT:
				  pygame.quit()
				  break
        
 
## Setting TouchBar
Once you have prepared the windows you are using, you would have to set the different TouchBar items you will use (see below).<br>
To do so, you'll have to execute the command

    ptb.set_touchbar([item1, item2,...])

Example showing two labels:

    lbl1 = TouchBarLabel(text='Hello')
    space = TouchBarSpace.Flexible()
	  lbl2 = TouchBarLabel(text='World')
	  ptb.set_touchbar([lbl1, space, lbl2])
    
If at anytime, you need to reload the TouchBar, just call

    ptb.reload_touchbar()
   
## Different kind of TouchBar items

You have many kinds of items you can add to your TouchBar, wrapping most common kinds of NSTouchBarItems subclasses.
    
### TouchBarLabel

Just showing a standard label in the TouchBar.

    label = TouchBarLabel(text = 'Foo Bar')
    
###### Parameters:
 - text (String) : The text to be shown on the label
 - text_color (tuple) : The color of the text to be shown as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (see below)
 - alignment : The alignment of the text in the label. Alignments are defined in constants (see below)
 - font_name (String) : Default is Arial. The font name of the text to show
 - font_size (Int) : Default is 16. The font size of the text to show
 
### TouchBarButton

A button the user can click, that will call actions.

    def function(button):
      print ('Button clicked!')

    label = TouchBarLabel(title = 'Click me!', action = function)
    
###### Parameters:
 - title (String or None) : The string that will be displayed in the button
 - color (tuple or None) : The button background color. Formatted as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (see below)
 - image (String or None) : A path to an image file that will be shown on the button
 - image_position : The position of the image relative to the title. Image positions are defined in constants (see below)
 - image_scale : The image scaling. Image scales are defined in constants (see below)
 - action (function) : The function that will be called when the user touchs the button
 
 
 
