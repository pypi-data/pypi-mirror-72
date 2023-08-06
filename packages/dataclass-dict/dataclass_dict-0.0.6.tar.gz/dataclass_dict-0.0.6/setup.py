# type: ignore
'''
:author: Leandro (Cerberus1746) Benedet Garcia'''
import os
import re
import sys

import setuptools

try:
    #pylint: disable=import-error
    from sphinx.setup_command import BuildDoc
    SPHINX_LOADED = True
except ImportError:
    SPHINX_LOADED = False


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_REQUIRES = []
NAME = 'dataclass_dict'

sys.path.append(os.path.join(CURRENT_DIR, "src"))


def open_file(file_name):
    with open(file_name, "r") as file_handle:
        return file_handle.read()


def stripped_file(file_name):
    return open_file(file_name).strip().split("\n")


def find_version():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    version_file = open_file(os.path.join(current_dir, "src", NAME, "__version__.py"))
    version_match = re.search(r"^__version__:\s*str\s*=\s*['\"]([^'\"]*)['\"]", version_file)
    return version_match.group(1)


__version__ = find_version()

LONG_DESCRIPTION = open_file("README.md")
LICENSE = open_file("LICENSE")

TEST_PACKAGES = stripped_file("requirements-tests.txt")
REQUIREMENTS_DOCS = stripped_file("requirements-docs.txt")


if SPHINX_LOADED:
    CMDCLASS = {'build_sphinx': BuildDoc}

if sys.version_info < (3, 6):
    raise type("InvalidVersionError", (Exception,), {})("You must use python 3.6 or more to be "
                                                        "able to use this package")

if sys.version_info >= (3, 6) and sys.version_info < (3, 7):
    INSTALL_REQUIRES.append("dataclasses")

if sys.version_info >= (3, 6) and sys.version_info < (3, 8):
    INSTALL_REQUIRES.append("typing-extensions")


setuptools.setup(
    name=NAME,
    version=__version__,
    cmdclass=CMDCLASS if SPHINX_LOADED else {},
    author="Leandro (Cerberus1746) Benedet Garcia",
    author_email="leandro.benedet.garcia@gmail.com",
    description="With this package you are able to create a dataclass that works exactly like a "
                "dictionary.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT License",
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6",
    url="https://github.com/Cerberus1746/" + NAME,
    tests_require=["pytest-runner"],
    packages=setuptools.find_packages(where='src'),  # Required
    package_dir={'': 'src'},
    extras_require={
        'tests': TEST_PACKAGES,
        'docs': REQUIREMENTS_DOCS
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",

        "Topic :: Utilities",
        "Topic :: Internet"
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', __version__),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
        }
    } if SPHINX_LOADED else {},
)
