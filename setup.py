from setuptools import setup, find_packages

with open('pglogmon/version.txt') as fptr:
    VERSION = fptr.read().strip()

with open('README.rst') as fptr:
    LONG_DESCRIPTION = fptr.read().strip()


setup(
    name='pglogmon',
    version=VERSION,
    description="Tool to monitor postgresql CSV logs",
    long_description=LONG_DESCRIPTION,
    author="Michel Albert",
    author_email="michel@albert.lu",
    url='https://github.com/exhuma/postgresql-logmon',
    license="MIT",
    include_package_data=True,
    install_requires=[
        'blessings'
    ],
    entry_points={
        'console_scripts': [
            'pglogmon=pglogmon.main:main',
        ]
    },
    packages=find_packages(exclude=["test", "tests.*", "tests"]),
    keywords='postgresql sysadmin',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: Stackless',

    ]
)
