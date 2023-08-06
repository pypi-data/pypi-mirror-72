""" Unit bootstrap tool
--------------------------
The tool that helps configure and sign Aos services.
"""

from setuptools import setup, find_packages
from aos_signer import __version__


def get_required_packages():
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    return required


setup(
    name="aos-signer",
    version=__version__,
    license="Apache License 2.0",
    author="EPAM Systems",
    author_email="support@aoscloud.io",
    description="Aos service manager",
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=get_required_packages(),
    platforms="any",
    entry_points={
        'console_scripts': [
            'aos-signer=aos_signer.main:main'
        ]
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ]
)
