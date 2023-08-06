from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))

version = '0.1.2'

install_requires = [
]

readme = open("README.md").read()

setup(name='cselector',
    version=version,
    description="Console single/multi selector for python.",
    long_description="https://github.com/aieater/python_console_selector\n\n"+readme,
    long_description_content_type='text/markdown',
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ),
    keywords='console temrinal selector pick picker menu',
    author='Pegara, Inc.',
    author_email='info@pegara.com',
    url='https://github.com/aieater/python_console_selector',
    license='MIT',
    packages=['cselector'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points={}
)
