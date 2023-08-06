from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="rstdepassuredtchnq",
    version="0.0.1",
    description="A Demo Dummy package to check for pypi upload",
    long_description="This is a Long Description - A Demo Dummy package to check for pypi upload.",
    long_description_content_type="text/markdown",
    url="https://google.com",
    author="Deepika",
    author_email="deepirms2619@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rstdepassuredtchnq",
              "rstdepassuredtchnq.core",
              "rstdepassuredtchnq.core.base",
              "rstdepassuredtchnq.core.base.apihelpers",
              "rstdepassuredtchnq.core.base.config",
              "rstdepassuredtchnq.core.base.core",
              "rstdepassuredtchnq.core.base.endpoints",
              "rstdepassuredtchnq.core.base.format",
              "rstdepassuredtchnq.core.base.log",
              "rstdepassuredtchnq.core.base.utils",
              "rstdepassuredtchnq.core.mock"],
    include_package_data=True,
    install_requires=["pytest",
                      "pytest-html",
                      "requests",
                      "Flask",
                      "jsonpath",
                      "oauth2",
                      "bs4",
                      "mock",
                      "selenium",
                      "slack",
                      "slackclient",
                      "twine"]
)
