import setuptools

setuptools.setup(
    name="PyTouchBar",
    version="0.3.1",
    author="Maxmad68, Emilio Dalla Torre",
    author_email="maxime@madrau.fr, info@emiliodallatorre.it",
    description="Use MacBook Pro's TouchBar in Python",
    long_description="Use MacBook Pro's TouchBar in Python. PyTouchBar make easy the use of the TouchBar with Python graphical modules Tkinter and Pygame (other are coming). Currently works with Buttons, Labels, Sliders, Steppers, ColorPickers, Popovers, Segmented Controls and Spaces.\nSee <a href=\"https://github.com/Maxmad68/PyTouchBar/wiki\">my Github for docs</a>",
    long_description_content_type="text/markdown",
    url="https://github.com/Maxmad68/PyTouchBar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
