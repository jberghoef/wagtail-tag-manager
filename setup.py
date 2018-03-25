import re
from setuptools import find_packages, setup


install_requires = [
    'wagtail>=2.0,<2.1',
]

tests_require = [
    'factory_boy==2.8.1',
    'flake8-blind-except',
    'flake8-debugger',
    'flake8-imports',
    'flake8',
    'freezegun==0.3.8',
    'pytest-cov==2.4.0',
    'pytest-django==3.1.2',
    'pytest-pythonpath==0.7.2',
    'pytest-sugar==0.7.1',
    'pytest==3.1.0',
    'wagtail_factories==1.0.0',
]

docs_require = [
    'sphinx>=1.4.0',
]

with open('README.rst') as fh:
    long_description = re.sub(
        '^.. start-no-pypi.*^.. end-no-pypi', '', fh.read(), flags=re.M | re.S)

setup(
    name='wagtail-tag-manager',
    version='0.0.1',
    description='A Wagtail add-on for managing tags.',
    author='Jasper Berghoef',
    author_email='jasper.berghoef@gmail.com',
    url='http://jasperberghoef.com',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'test': tests_require,
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='GPLv3',
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 2.0',
        'Framework :: Wagtail :: 2.0',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
