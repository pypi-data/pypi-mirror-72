import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pj_robotnotifier",
    version="0.0.1",
    description="Send notifications to Slack or Mattermost using Robot Framework Listener..",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    author="PJ Gevana",
    author_email="patdroidz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pj_robotnotifier"],
    include_package_data=True,
    # install_requires=["requests"],
)
