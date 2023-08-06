import re

from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ""
with open('pyud/__init__.py') as f:
    for line in f:
        match = re.search(
            r'__version__\s*=\s*[\'"](?P<version>[^\'"]*)[\'"]', line
        )

        if match:
            version = match.group('version')
            break

if not version:
    raise RuntimeError('Version info was not found')

readme = ""
with open('README.rst') as f:
    readme = f.read()

setup(
    name="pyud",
    version=version,
    description="A simple wrapper for the Urban Dictionary API",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/WilliamWFLee/pyud",
    author="William Lee",
    author_email="wlee753159@gmail.com",
    license="GNU GPL v3.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords='urbandictionary api async',
    project_urls={
        "Documentation": "https://pyud.readthedocs.io",
        "Source": "https://github.com/WilliamWFLee/pyud",
    },
    packages=['pyud'],
    install_requires=requirements,
    python_requires="~=3.6",
)
