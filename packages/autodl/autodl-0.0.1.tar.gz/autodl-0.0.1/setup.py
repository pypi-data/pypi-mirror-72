import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

NAME = "autodl"
REQUIRES_PYTHON = ">=3.5"
VERSION = None

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


REQUIRED = [
    "numpy",
    "scikit-learn",
    "tqdm",
    "tensorflow>=2.0.0",
    "torch>=1.3.0",
    "keras",
    "pandas>=0.25.0",
    "matplotlib>=3.1.0",
    "psutil==5.6.7",
]

# What packages are optional?
EXTRAS = {"dev": ["twine"]}

# Commands
class UploadCommand(Command):
    """
    Support setup.py upload.

    pip install twine
    """

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


class TestUploadCommand(Command):
    """Support setup.py testupload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")

        sys.exit()


class TestInstallCommand(Command):
    """Support setup.py testinstall"""

    description = "Install deephyper from TestPyPI."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status("Downloading the package from Test PyPI and installing it")
        os.system("pip install --index-url https://test.pypi.org/simple/ autodl")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    python_requires=REQUIRES_PYTHON,
    entry_points={"console_scripts": ["autodl=autodl.cli.cli:main"]},
    license="BSD-2",
    classifiers=[
        # Trove classifiers
        # https://pypi.org/classifiers/
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={
        "upload": UploadCommand,
        "testupload": TestUploadCommand,
        "testinstall": TestInstallCommand,
    },
)
