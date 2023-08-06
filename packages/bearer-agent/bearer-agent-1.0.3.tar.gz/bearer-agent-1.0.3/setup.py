import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Internet",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Internet :: WWW/HTTP",
]


# read long description
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

install_requires = [
    # We depend on functioning pkg_resources.working_set.add_entry() and
    # pkg_resources.load_entry_point(). These both work as of 3.0 which
    # is the first version to support Python 3.4 which we require as a
    # floor.
    "setuptools>=3.0",
    "urllib3>=1,<2",
    "wrapt>=1,<2",
]

tests_require = ["black", "flake8", "pytest", "requests", "httpx"]

setup(
    name="bearer-agent",
    version="1.0.3",
    description="Bearer Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bearer Team",
    author_email="engineering+python@bearer.sh",
    license="Apache License 2.0",
    url="http://www.bearer.sh",
    python_requires=">=3.5",
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
    zip_safe=False,
    packages=find_packages(include=["bearer_agent*"]),
    include_package_data=True,
    tests_require=tests_require,
    extras_require={"tests": tests_require},
    cmdclass={"test": PyTest},
)
