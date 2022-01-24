from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.11,<2.16",
    "selenium>=3.141.0,<3.142.0",
]

tests_require = [
    "factory_boy==3.2.0",
    "Faker==6.1.1",
    "flake8-blind-except",
    "flake8-debugger",
    "flake8-imports",
    "flake8",
    "freezegun==1.1.0",
    "pycodestyle==2.6.0",
    "pytest-cov==2.11.1",
    "pytest-django==4.1.0",
    "pytest-pythonpath==0.7.3",
    "pytest-randomly==3.5.0",
    "pytest-sugar==0.9.4",
    "pytest==6.2.2",
    "wagtail_factories==2.0.1",
]

docs_require = ["sphinx>=2.4.0"]

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="wagtail-tag-manager",
    version="1.2.1",
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
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail :: 2",
    ],
)
