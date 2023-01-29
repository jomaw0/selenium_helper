import setuptools

setuptools.setup(
	name='selenium_helper',
	version='0.0.1',
	author='Jonas Wolf',
	author_email='jonas.wolf8@me.com',
	description='Helper Class for Selenium',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/jomaw0/selenium_helper',
	license='MIT',
	packages=['selenium_helper'],
	install_requires=['selenium', 'webdriver-manager'],
)