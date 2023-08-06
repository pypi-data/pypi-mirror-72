import setuptools

from lmt_india_covid19_risk_assessment import __version__

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name=f"lmt-india-covid19-risk-assessment",
    version=__version__,
    author="IST Research",
    author_email="support@istresearch.com",
    description="LMT-India COVID-19 Risk Assessment",
    license="MIT License",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/istresearch/lmt-india-covid19-risk-assessment",
    packages=["lmt_india_covid19_risk_assessment"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "limesurvey-coconut>=1.0.1"
    ],
    include_package_data=True,
)
