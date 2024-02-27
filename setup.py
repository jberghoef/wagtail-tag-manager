from setuptools import find_packages, setup


install_requires = [
    "wagtail>=4.0,<7.0",
    "wagtail_modeladmin>=2.0.0,<2.1.0",
    "selenium>=3.141.0,<3.142.0",
]

tests_require = [
    "factory_boy",
    "Faker",
    "flake8-blind-except",
    "flake8-debugger",
    "flake8-imports",
    "flake8",
    "freezegun",
    "pycodestyle",
    "pytest-cov",
    "pytest-django",
    "pytest-pythonpath",
    "pytest-randomly",
    "pytest-sugar",
    "pytest",
    "wagtail_factories",
]

docs_require = ["sphinx>=2.4.0"]

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="wagtail-tag-manager",
    version="2.0.0",
    description="A Wagtail add-on for managing tags.",
    author="Jasper Berghoef",
    author_email="j.berghoef@me.com",
    url="https://github.com/jberghoef/wagtail-tag-manager",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="BSD 3-Clause",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "Framework :: Wagtail :: 5",
        "Framework :: Wagtail :: 6",
    ],
)
