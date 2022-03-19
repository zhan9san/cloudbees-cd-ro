import os
from setuptools import find_packages
from setuptools import setup

# with open(os.path.join("cloudbees", "VERSION")) as file:
#     version = file.read().strip()
version = '0.0.1'

with open("README.rst") as file:
    long_description = file.read()

setup(
    name="cloudbees-cd-ro",
    description="Python Cloudbees CD/RO REST API Wrapper",
    long_description=long_description,
    license="Apache License 2.0",
    version=version,
    download_url="https://github.com/zhan9san/cloudbees-cd-ro",
    author="Jack Zhang",
    author_email="jack4zhang@gmail.com",
    url="https://github.com/zhan9san/zhan9san/cloudbees-cd-ro",
    keywords="cloudbees cd/ro rest api",
    packages=find_packages(include=["cloudbees*"]),
    package_dir={"cloudbees": "cloudbees"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["deprecated", "requests", "six"],
    extras_require={},
    platforms="Platform Independent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
