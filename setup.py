import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="manga-dl",
        version=open("version", "r").read(),
        description="A Manga Downloader",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/namibsun/python/manga-dl",
        license="GNU GPL3",
        packages=find_packages(),
        scripts=list(map(lambda x: os.path.join("bin", x), os.listdir("bin"))),
        install_requires=[
            "requests",
            "sentry-sdk",
            "injector",
            "lxml",
            "matplotlib",
            "Pillow"
        ],
        tests_require=[
            "pytest",
            "pytest-unordered",
            "pytest-cov"
        ],
        include_package_data=True,
        zip_safe=False
    )
