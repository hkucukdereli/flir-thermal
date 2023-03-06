import os
import sys
import warnings
from setuptools import setup, find_packages

# directory = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f .read()

setup(
    name="flir_thermal",
    author="Hakan Kucukdereli",
    author_email="hkucukdereli@gmail.com",
    maintainer="Hakan Kucukdereli",
    maintainer_email="hkucukdereli@gmail.com",
    description="Wrapper functions for handling FLIR .seq file format. Depends on Science File SDK.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    license="",
    url="",
    version="0.2",
    download_url="",
    install_requires=[
        "numpy",
        "tqdm",
        "opencv-python",
        "ffmpeg-python",
    ],
    packages=find_packages(),
    zip_safe=True,
)
