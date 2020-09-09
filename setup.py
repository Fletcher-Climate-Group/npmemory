import os
from setuptools import setup, find_packages

# Get the long description from the README file
long_description = """# npmemory
"""

# OS detection in order to set dynamic libraries correctly
package_data = dict()

if os.name == 'posix':
    package_data['npmemory.box_average'] = ['box_average.so']
elif os.name == 'nt':
    package_data['npmemory.box_average'] = ['box_average.dll']
else:
    raise OSError(f"OS not supported: {os.name}")

setup(
    name='',
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
