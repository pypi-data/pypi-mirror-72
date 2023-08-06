from setuptools import setup, find_packages

setup(
	version="0.1",
	author="Gintaras D.",
	license="GPLv3",

	name="castberry",
	url="https://github.com/GintarasD/Castberry",
	download_url="https://github.com/GintarasD/Castberry/archive/0.1.tar.gz",
	description="Cast youtube to a video player",
	long_description=open("README.rst").read(),
	long_description_content_type='text/x-rst',
	keywords="youtube cast raspberrypi",
	classifiers=[
		"Topic :: Multimedia",
		"Topic :: Internet",
		"Topic :: Games/Entertainment",

		"Natural Language :: English",
		"Intended Audience :: End Users/Desktop",
		"Environment :: No Input/Output (Daemon)",
		"Operating System :: OS Independent",

		"Typing :: Typed",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.7",
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	],

	entry_points={
		"console_scripts": {
			"castberry=castberry.main:main"
		}
	},

	packages=find_packages(),
	include_package_data=True,
	package_data={
		"": ["castberry/resources/*"]
	},
	install_requires=[
		"youtube-dl",
		"python-vlc"
	],
)
