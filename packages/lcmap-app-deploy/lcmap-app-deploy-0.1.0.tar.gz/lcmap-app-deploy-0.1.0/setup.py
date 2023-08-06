"""
LCMAP App Deploy - package setup information.
"""

from setuptools import setup, find_packages
import app_deploy


def readme():
    """Use the README as a long description for publishing to PyPI"""
    with open("README.rst") as file:
        return file.read()


setup(
    name="lcmap-app-deploy",
    version=app_deploy.version(),
    description="Backup/restore Marathon app job definitions.",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="usgs eros lcmap",
    url="https://eroslab.cr.usgs.gov/lcmap/deployment",
    author="USGS EROS LCMAP",
    author_email="",
    license="Unlicense",
    packages=find_packages(),
    install_requires=["requests",],
    extras_require={
        "tests": ["pytest", "pytest-cov",],
        "docs": ["sphinx", "sphinx-autobuild", "sphinx_rtd_theme"],
        "deploy": ["twine"],
    },
    entry_points={"console_scripts": ["app-deploy = app_deploy.__main__:main"]},
    python_requires=">=3.6",
    include_package_data=True,
)
