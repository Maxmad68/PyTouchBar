# PyTouchBar

A `NSTouchBar` wrapper for Python. It currently works with Tkinter and PyGame.

This library depends on `PyObjC` to wrap `NSTouchBar` and related classes. It also includes a wrapper for the haptic trackpad, allowing your Python programs to trigger trackpad vibrations.

**Note:** This will only work on MacBook Pro with TouchBars, or on a TouchBar Simulator ([you have a good one here](https://github.com/sindresorhus/touch-bar-simulator)).

## What's New

### 0.3.1
* Upgraded dependencies
* Fixed some typos

### 0.2.0

* Added user-customization of the TouchBar
* Better error management
* New Stepper item (macOS 10.15+)
* Added escape key modification
* Improved file structure of the module

## Installation

To install PyTouchBar, run the following command:

```bash
pip install PyTouchBar
```

## Example

Here is a simple example displaying a window with a label and a button in the TouchBar.

```python
from tkinter import *
import PyTouchBar

root = Tk()
PyTouchBar.prepare_tk_windows(root)  # Tell PyTouchBar that the "root" window will have a TouchBar

# Build Tkinter interface
lbl = Label(root, text="Hello World")
lbl.pack()

# Build TouchBar
def action(button):
    print("Button Pressed!")

btn = PyTouchBar.items.Button(title="Button", action=action)
PyTouchBar.set_touchbar([btn])


root.mainloop()
```

## Documentation

All documentation is available in the [wiki](https://github.com/Maxmad68/PyTouchBar/wiki):

* [Integrate into your project](https://github.com/Maxmad68/PyTouchBar/wiki/Integrate-into-your-project)
* [Add items to TouchBar](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar)
  - [Spaces](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Spaces)
  - [Labels](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Label)
  - [Buttons](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Button)
  - [Color Picker](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#ColorPicker)
  - [Slider](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Slider)
  - [Stepper](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Stepper)
  - [Segmented Controls](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#SegmentedControls)
  - [Popover](https://github.com/Maxmad68/PyTouchBar/wiki/Populate-TouchBar#Popover)
* [Constants](https://github.com/Maxmad68/PyTouchBar/wiki/Constants)
* [Change Escape key](https://github.com/Maxmad68/PyTouchBar/wiki/Set-Escape-Key)
* [User Customization](https://github.com/Maxmad68/PyTouchBar/wiki/User-customization)
* [Haptic Feedback](https://github.com/Maxmad68/PyTouchBar/wiki/Haptic-Feedback)
