import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ts3audiobot-api",
    version="0.0.2",
    author="EverHype Systems",
    author_email="abajrami@everhype-systems.eu",
    description="API Wrapper for TS3AudioBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EverHype-Systems/ts3audiobot-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
