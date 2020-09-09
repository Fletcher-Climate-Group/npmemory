import os
from setuptools import setup, find_packages

long_description = """# npmemory
"""

setup(
    name='package_name',
    version='0.1.0',
    description='TempDescription.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Hogg',
    author_email='danielhogg@protonmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    keywords='temp_keyword',
    packages=find_packages(exclude=['tests','examples']),

    python_requires='>=3.5, <4',
    install_requires=[],
)
