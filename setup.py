from setuptools import find_packages, setup


install_requires = [
    "wagtail>=2.1,<2.9",
    "beautifulsoup4==4.6.0",
    "selenium>=3.141.0,<3.142.0",
]

tests_require = [
    "factory_boy==2.11.1",
    "Faker==1.0.7",
    "flake8-blind-except",
    "flake8-debugger",
    "flake8-imports",
    "flake8==3.7.7",
    "freezegun==0.3.12",
    "pycodestyle==2.5.0",
    "pytest-cov==2.7.1",
    "pytest-django==3.5.1",
    "pytest-pythonpath==0.7.3",
    "pytest-randomly==3.0.0",
    "pytest-sugar==0.9.2",
    "pytest==5.0.1",
    "wagtail_factories==1.1.0",
]

docs_require = ["sphinx>=2.4.0"]

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="wagtail-tag-manager",
    version="0.21.5",
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
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Wagtail :: 2",
    ],
)
