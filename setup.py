import setuptools

setuptools.setup(
    name="PyTouchBar", # Replace with your own username
    version="0.1.4",
    author="Maxmad68",
    author_email="maxime@madrau.fr",
    description="Use MacBook Pro's TouchBar in Python",
    long_description="Use MacBook Pro's TouchBar in Python. PyTouchBar make easy the use of the TouchBar with Python graphical modules Tkinter and Pygame (other are coming). Currently works with Buttons, Labels, Sliders, ColorPickers, Popovers, Segmented Controls and Spaces.\nSee <a href=\"https://github.com/Maxmad68/PyTouchBar/wiki\">my Github for docs</a>",
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
