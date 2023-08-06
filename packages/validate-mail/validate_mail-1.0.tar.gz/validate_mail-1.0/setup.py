from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup (
	name='validate_mail',
	version='1.0',
	description='Validating the e-mail ID passed',
        long_description=long_description,
        long_description_content_type='text/markdown',
	py_modules=['validate_mail'],
	package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        author='Maria Irudaya Regilan J',
        author_email='britsa.tech@gmail.com'
)
