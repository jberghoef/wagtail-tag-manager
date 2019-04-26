import re
from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.1,<2.5",
    "beautifulsoup4==4.6.0",
    "selenium>=3.141.0,<3.142.0",
]

tests_require = [
    "factory_boy==2.11.1",
    "Faker==1.0.2",
    "flake8-blind-except",
    "flake8-debugger",
    "flake8-imports",
    "flake8==3.7.6",
    "freezegun==0.3.11",
    "pycodestyle==2.5.0",
    "pytest-cov==2.6.1",
    "pytest-django==3.4.7",
    "pytest-pythonpath==0.7.3",
    "pytest-sugar==0.9.2",
    "pytest==4.3.0",
    "wagtail_factories==1.1.0",
]

docs_require = ["sphinx>=1.4.0"]

setup(
    name="wagtail-tag-manager",
    version="0.16.4",
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
    long_description="",
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
