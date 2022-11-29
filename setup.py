from setuptools import setup

setup(
    name="dqfit",
    package_dir={"": "src"},
    package_data={"": ["data/weights/*.csv"]},
    author="Parker Holcomb",
    author_email="parker.holcomb@gmail.com",
)
