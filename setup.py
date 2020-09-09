"""
Copyright © 2020 Daniel Hogg

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
from setuptools import setup, find_packages

# Get the long description from the README file
long_description = """# npmemory
"""

# OS detection in order to set dynamic libraries correctly
package_data = dict()

if os.name == 'posix':
    package_data['npmemory.clibs'] = ['box_average.so']
elif os.name == 'nt':
    package_data['npmemory.clibs'] = ['box_average.dll']
else:
    raise OSError(f"OS not supported: {os.name}")

setup(
    name='npmemory',
    version='1.0.0',
    description='NumPy memory editing for maximum performance.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Hogg',
    author_email='dhogg@uwaterloo.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    keywords='numpy',
    packages=find_packages(exclude=['tests','examples']),
    # Distributing binary as a possible alternative to CPython extensions
    package_data=package_data,
    python_requires='>=3.5, <4',
    install_requires=['numpy'],
)
