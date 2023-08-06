from setuptools import setup

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='greetuvm',
    version='0.0.1',
    description='Say hello to someone (or thing)',
    url="https://gitlab.com/monden/greetuvm",
    author="Monde",
    author_email="xytuple@gmail.com",
    py_modules=['hello'],
    package_dir={'': 'src'},
    # Declaring prod dependencies:
    install_requires=[
        # "blessings ~= 1.7",    # eg
        # "click ~= 7.1.2",
    ],
    # Declare development dependencies
    extras_require={
        "dev": [
            "pytest>=3.7",
            "check-manifest>=0.42",
            "twine>=3.2.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)

