from setuptools import setup

with open('README_pypi.md') as f:
    long_description = f.read()

setup (name = 'styletx',
       version = '1.0.3',
       description = 'Initial release with StyleTransfer',
       packages = ['styletx'],
       author = 'Dinesh Kumar Gnanasekaran',
       author_email = 'dinesh.gna111@gmail.com',
       long_description = long_description,
       long_description_content_type = 'text/markdown',
       license = 'MIT',
       zip_safe = False,
       include_package_data=True)