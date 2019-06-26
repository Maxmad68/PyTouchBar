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
 - text_color (tuple) : The color of the text to be shown as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (<a href="https://github.com/Maxmad68/PyTouchBar/blob/master/README.md#color">see below</a>)
 - alignment : The alignment of the text in the label. Alignments are defined in constants (see below)
 - font_name (String) : Default is Arial. The font name of the text to show
 - font_size (Int) : Default is 16. The font size of the text to show
 
### TouchBarButton

A button the user can click, that will call actions.

    def function(button):
      print ('Button clicked!')

    button = TouchBarButton(title = 'Click me!', action = function)
    
###### Parameters:
 - title (String or None) : The string that will be displayed in the button
 - color (tuple or None) : The button background color. Formatted as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (<a href="https://github.com/Maxmad68/PyTouchBar/blob/master/README.md#color">see below</a>)
 - image (String or None) : A path to an image file that will be shown on the button
 - image_position : The position of the image relative to the title. Image positions are defined in constants (see below)
 - image_scale : The image scaling. Image scales are defined in constants (see below)
 - action (function) : The function that will be called when the user touchs the button
 
 
### TouchBarColorPicker

A color picker right in the TouchBar.

    def function(picker):
      print ('Color:', picker.color)

    cpk = TouchBarColorPicker(action = function)
    
###### Parameters:
 - alpha (Bool) : True if user can select alpha value, False otherwise
 - type : The type of color picker. Color picker types are defined in constants (see below)
 - image (String) : If type is ColorPickerType.image, you can define the image displayed in the color picker button by specifying this parameter. This is the path of an image file.
 - action (function) : The function that will be called when the user change the value of the color picker
 
##### Extra Arguments:
 - color (tuple) : You can retrieve and set the selected color by using or setting this variable. Formatted as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (<a href="https://github.com/Maxmad68/PyTouchBar/blob/master/README.md#color">see below</a>).


### TouchBarSlider

A slider for the TouchBar

    def function(slider):
      print ('Value:', slider.value * 100)

    slider = TouchBarSlider(action = function)
    
###### Parameters:
 - title (String) : The title of the slider, that will be displayed next to the slider
 - value (Float) : The default value as a decimal number between 0 and 1
 - color (tuple) : The tint color of the slider. Formatted as (r, g, b, a) where values are decimal numbers between 0 and 1. You can use the color constants (<a href="https://github.com/Maxmad68/PyTouchBar/blob/master/README.md#color">see below</a>)
  - action (function) : The function that will be called when the user change the value of the slider

 
##### Extra Arguments:
 - value (float) : You can get and set the current value of the slider with this argument. Note: it is a decimal number between 0 and 1


### TouchBarPopover

A button that will show another TouchBar when clicked.

    label = TouchBarLabel(text = 'Foo Bar')    

    popover = TouchBarPopover([label])
    
###### Parameters:
 - title (String) : The title of the popover, that will be displayed next on the button
 - shows_close_button (Bool) : If True, once the popover is opened, will show a close button. If False, it won't and the only way to close the popover is to call popover.close()
 - holdItems (list) : A list containing items that will be shown if the button is touched and hold by the user. It's kind of another TouchBar

 
##### Methods:
 - popover.reload() : If the sub-TouchBar content is modified and the sub-TouchBar needs to be reloaded, this command will do so.
 - popover.open() : Open the popover
 - popover.close() : Close the popover
 
 
### TouchBarSpace

Space items.<br>
The flexible space will take all the place it can, so the items will be pushed on the other side of the TouchBar.
No parameters required, just use items like this:

#### TouchBarSpace.Small()
#### TouchBarSpace.Large()
#### TouchBarSpace.Flaxible()



## Constants

### Color
Color constants are not required, they just make easier the use of custom colors in TouchBar items.
For example, instead of setting a red color like this:  (1, 0, 0, 1)  , you could use: Color.red .

 - green
 - blue
 - red
 - yellow
 - orange
 - purple
 - cyan
 - white
 - black
 - clear


### ImagePosition

 - noimage
 - imageonly
 - left
 - right
 - below
 - above
 - overlaps
 
### ImageScale

 - proportionnaly_down
 - axes_independently
 - none
 - proportionnaly_up_or_down
 
### Alignment

 - left
 - right
 - center
 - justified
 - natural
 
### ColorPickerTyped
Note: it has no effects on the Color Picker, it will just change the image used on the button

- color
- text
- stroke
- image (In that case, define an image with the image parameter)
