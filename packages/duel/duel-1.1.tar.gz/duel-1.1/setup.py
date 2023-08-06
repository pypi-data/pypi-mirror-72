import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="duel",
    version="1.1",
    description="Locally Multiplayer Dueling game",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexisDougherty13/Duel",
    author="Python Buds",
    author_email="zachary.s1110@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["duel"],
    include_package_data=True,
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "duel=duel.theMain:__main__",
        ]
    },
)
