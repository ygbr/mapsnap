#!/usr/bin/env python3

from setuptools import find_packages, setup

from mapsnap import __version__


def main():
    setup(
        name="mapsnap",
        version=__version__,
        description="Apple Maps Web Snapshots on Python",
        keywords="apple mapkit web snapshot maps",
        author="Ygor Lemos",
        author_email="ygbr@mac.com",
        license="MIT",
        url="https://mapsnap.ygor.dev",
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
        install_requires=["ecdsa[gmpy2]", "requests"],
        tests_require=["pytest", "black"],
        include_package_data=True,
        project_urls={
            "Bug Tracker": "https://github.com/ygbr/mapsnap/issues",
            "Documentation": "https://mapsnap.ygor.dev",
            "Source Code": "https://github.com/ygbr/mapsnap",
        },
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Communications :: Chat",
            "Topic :: Internet",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
    )


if __name__ == "__main__":
    main()
