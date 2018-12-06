import re
from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.1,<2.4",
    "beautifulsoup4==4.6.0",
    "selenium>=3.141.0,<3.142.0",
]

tests_require = [
    "factory_boy==2.7.0",
    "fake-factory==0.7.4",
    "flake8-blind-except",
    "flake8-debugger",
    "flake8-imports",
    "flake8==3.4.1",
    "freezegun==0.3.8",
    "pycodestyle==2.3.1",
    "pytest-cov==2.4.0",
    "pytest-django==3.1.2",
    "pytest-pythonpath==0.7.2",
    "pytest-sugar==0.7.1",
    "pytest==3.1.0",
    "wagtail_factories==1.0.0",
]

docs_require = ["sphinx>=1.4.0"]

with open("README.rst") as fh:
    long_description = re.sub(
        "^.. start-no-pypi.*^.. end-no-pypi", "", fh.read(), flags=re.M | re.S
    )

setup(
    name="wagtail-tag-manager",
    version="0.4.5",
    description="A Wagtail add-on for managing tags.",
    author="Jasper Berghoef",
    author_email="jasper.berghoef@gmail.com",
    url="https://github.com/jberghoef/wagtail-tag-manager",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="BSD 3-Clause",
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Wagtail :: 2",
    ],
)
