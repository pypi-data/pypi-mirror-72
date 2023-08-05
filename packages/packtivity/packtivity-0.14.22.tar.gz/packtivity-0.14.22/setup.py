import os
from setuptools import setup, find_packages

deps = [
    "requests[security]",
    "jsonschema",
    "jsonref",
    "pyyaml",
    "click",
    "glob2",
    "jsonpointer",
    "jsonpath-rw",
    "jq",
    "yadage-schemas",
    "mock",
    "checksumdir",
]

if not "READTHEDOCS" in os.environ:
    deps += ["jq"]


setup(
    name="packtivity",
    version="0.14.22",
    description="packtivity - general purpose schema + bindings for PROV activities",
    url="https://github.com/yadage/packtivity",
    author="Lukas Heinrich",
    author_email="lukas.heinrich@cern.ch",
    packages=find_packages(),
    include_package_data=True,
    install_requires=deps,
    extras_require={"celery": ["celery", "redis"],},
    entry_points={
        "console_scripts": [
            "packtivity-run=packtivity.cli:runcli",
            "packtivity-util=packtivity.cli:utilcli",
            "packtivity-validate=packtivity.cli:validatecli",
            "packtivity-checkproxy=packtivity.cli:checkproxy",
        ],
    },
    dependency_links=[],
)
