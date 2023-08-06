#!/usr/bin/env python

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as fd:
    README = fd.read()


setup(
    name="fedora-elections-messages",
    version="1.0.0",
    description="A schema package for messages sent by fedora-elections",
    long_description=README,
    url="https://pagure.io/elections-messages",
    # Possible options are at https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    license="GPLv2+",
    maintainer="Fedora Infrastructure Team",
    maintainer_email="infrastructure@lists.fedoraproject.org",
    platforms=["Fedora", "GNU/Linux"],
    keywords="fedora",
    packages=find_packages(
        exclude=("fedora_elections_messages.tests", "fedora_elections_messages.tests.*")
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=["fedora_messaging"],
    test_suite="fedora_elections_messages.tests",
    entry_points={
        "fedora.messages": [
            "fedora_elections.election.new=fedora_elections_messages.election_new:NewElectionV1",
            "fedora_elections.election.edit=fedora_elections_messages.election_edit:EditElectionV1",
            "fedora_elections.candidate.new=fedora_elections_messages.candidate_new:NewCandidateV1",
            (
                "fedora_elections.candidate.edit="
                "fedora_elections_messages.candidate_edit:EditCandidateV1"
            ),
            (
                "fedora_elections.candidate.delete="
                "fedora_elections_messages.candidate_delete:DeleteCandidateV1"
            ),
        ]
    },
)
