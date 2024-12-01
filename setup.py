from setuptools import find_packages, setup

setup(
    name="sports_betting_pipeline",
    packages=find_packages(exclude=["sports_betting_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
