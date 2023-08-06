import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ds-toolkit",
	version="0.0.1",
	author="David Silva",
	description="Toolkit for common programming needs",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/davidsilva2841/ds-toolkit',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
)
