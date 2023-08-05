"""
avwx Package Setup
"""

from setuptools import find_namespace_packages, setup

VERSION = "1.4.6"

dependencies = [
    "geopy~=1.22",
    "httpx~=0.13",
    "python-dateutil~=2.8",
    "xmltodict~=0.12",
]

test_dependencies = ["pytest-asyncio~=0.12", "time-machine~=1.1"]

extras = {
    "scipy": ["scipy~=1.5"],
    "docs": ["mkdocs~=1.1"],
    "tests": test_dependencies,
}

setup(
    name="avwx-engine",
    version=VERSION,
    description="Aviation weather report parsing library",
    url="https://github.com/avwx-rest/avwx-engine",
    author="Michael duPont",
    author_email="michael@mdupont.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">= 3.7",
    install_requires=dependencies,
    packages=find_namespace_packages(include=["avwx*"]),
    package_data={"avwx.data": ["aircraft.json", "stations.json"]},
    tests_require=test_dependencies,
    extras_require=extras,
)
