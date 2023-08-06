import setuptools


with open("README.md", "r") as file:
	long_description = file.read()

setuptools.setup(
	name = "pymemes",
	version = "0.0.1",
	author = "João Caldeira",
	author_email = "jt.brazaocaldeira@gmail.com",
	description = "Memes on Python - just for fun :)",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/JTCaldeira/pymemes",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
	python_requires = ">=3.6"
)
