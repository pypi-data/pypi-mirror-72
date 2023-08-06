"""Install the dock-r library."""

import os
from pathlib import Path

from setuptools import setup

DETECTED_VERSION = None
VERSION_FILEPATH = "VERSION"
PACKAGE_NAME = "dock-r"
PACKAGE_ONELINER = "Tools to go faster with docker."
GIT_REPO_URL = "https://www.github.com/aaronsteers/runnow"
AUTHOR_NAME = "Aaron (AJ) Steers"
AUTHOR_EMAIL = "aj.steers@slalom.com"


def _get_build_number():
    return os.environ.get("BUILD_NUMBER", os.environ.get("GITHUB_RUN_NUMBER", None))


if "VERSION" in os.environ:
    DETECTED_VERSION = os.environ["VERSION"]
    if "/" in DETECTED_VERSION:
        DETECTED_VERSION = DETECTED_VERSION.split("/")[-1]
if not DETECTED_VERSION and os.path.exists(VERSION_FILEPATH):
    DETECTED_VERSION = Path(VERSION_FILEPATH).read_text()
    if len(DETECTED_VERSION.split(".")) <= 3:
        build_num = _get_build_number()
        if build_num:
            DETECTED_VERSION = f"{DETECTED_VERSION}.{build_num}"
if not DETECTED_VERSION:
    raise RuntimeError("Error. Could not detect version.")
DETECTED_VERSION = DETECTED_VERSION.replace(".dev0", "")
if os.environ.get("BRANCH_NAME", "unknown") not in ["master", "refs/heads/master"]:
    DETECTED_VERSION = f"{DETECTED_VERSION}.dev0"

DETECTED_VERSION = DETECTED_VERSION.lstrip("v")
print(f"Detected version: {DETECTED_VERSION}")
Path(VERSION_FILEPATH).write_text(f"v{DETECTED_VERSION}")

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME.replace("-", "_")],
    version=DETECTED_VERSION,
    license="MIT",
    description=f"{PACKAGE_NAME} - {PACKAGE_ONELINER}",
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    url=GIT_REPO_URL,
    download_url=f"{GIT_REPO_URL}/archive",
    keywords=["DOCKER"],
    package_data={"": [VERSION_FILEPATH]},
    entry_points={
        "console_scripts": [
            # Register CLI commands:
            "dock-r = dock_r.cli:_main",
        ]
    },
    include_package_data=True,
    install_requires=[
        "docker",
        "fire",
        "logless",
        "runnow",
        "uio",
    ],
    extras_require={},
    classifiers=[
        "Development Status :: 4 - Beta",  # "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
# Revert `.dev0` suffix
# Path(VERSION_FILEPATH).write_text(f"v{DETECTED_VERSION.replace('.dev0', '')}")
