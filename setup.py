from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in minom/__init__.py
from minom import __version__ as version

setup(
	name="minom",
	version=version,
	description="Frappe App to Enhancement of Events and Utility to mark Minutes of Meeting and it\'s follow-up",
	author="efeone Pvt. Ltd.",
	author_email="info@efeone.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
