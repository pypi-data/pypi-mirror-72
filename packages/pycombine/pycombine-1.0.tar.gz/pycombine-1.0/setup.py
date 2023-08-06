from setuptools import setup

setup(
    name="pycombine",
    packages=["pycombine"],
    version="1.0",
    license="GPLv3",
    description="Combine files together",
    long_description="On your Command line / bar, just type in `pycombine main_file [file ...]`. For example, "
                     "`pycombine main.py partone.py parttwo.py`. Github is "
                     "https://github.com/jackprogramsjp/pycombine.",
    long_description_content_type="text/markdown",
    author="Jack Murrow",
    author_email="jack.murrow122005@gmail.com",
    url="https://github.com/jackprogramsjp/pycombine",
    keywords=["Python Combine", "Combine", "PyCombine"],
    entry_points={
        "console_scripts": [
            "pycombine = pycombine.pycombine:pycombine"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
