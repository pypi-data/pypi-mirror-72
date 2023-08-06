import os

from setuptools import setup, find_packages

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "bson_timezone", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bson_timezone",
    version=about["__version__"],
    description="Provides timezone support for bson.json_util.dumps and bson.json_util.loads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AgileTek Engineering",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=["pymongo", "pytz"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-mock"],
    extras_require={
        "pre-commit": "pre-commit",
        "flake8": "flake8",
        "black": "black",
    },
    include_package_data=True,
    zip_safe=False,
)
