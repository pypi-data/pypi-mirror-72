from setuptools import setup
import os
import re
from gitlab import config


def long_description():
    with open('README.md') as fp:
        return fp.read()


def get_requirements():
    with open("requirements.txt") as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


def get_metadata():
    with open(os.path.join(config.MAIN_PACKAGE, "_about.py")) as file:
        file_content = file.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__\s*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(file_content):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return groups


metadata = get_metadata()

setup(
    name=config.PROJECT_NAME,
    version=metadata['version'],
    description="Python algorithms used to perform machine learning.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Dec0Ded",
    author_email="4323565-dec0ded@users.noreply.gitlab.com",
    license="LGPL-3.0-ONLY",
    url="https://gitlab.com/michkaro/teardrop",
    packages=['teardrop'],
    python_requires="> 3.7",
    install_requires=get_requirements(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)