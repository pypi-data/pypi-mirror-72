import re

from pkg_resources import get_distribution, DistributionNotFound
import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

# Take from https://github.com/aleju/imgaug
INSTALL_REQUIRES = [
    "numpy",
    "pymupdf",
    "opencv-python-headless"
]

ALT_INSTALL_REQUIRES = {
    "opencv-python-headless": ["opencv-python", "opencv-contrib-python", "opencv-contrib-python-headless"],
}


def check_alternative_installation(install_require, alternative_install_requires):
    """If some version version of alternative requirement installed, return alternative,
    else return main.
    """
    for alternative_install_require in alternative_install_requires:
        try:
            alternative_pkg_name = re.split(r"[!<>=]", alternative_install_require)[0]
            get_distribution(alternative_pkg_name)
            return str(alternative_install_require)
        except DistributionNotFound:
            continue

    return str(install_require)


def get_install_requirements(main_requires, alternative_requires):
    """Iterates over all install requires
    If an install require has an alternative option, check if this option is installed
    If that is the case, replace the install require by the alternative to not install dual package"""
    install_requires = []
    for main_require in main_requires:
        if main_require in alternative_requires:
            main_require = check_alternative_installation(main_require, alternative_requires.get(main_require))
        install_requires.append(main_require)

    return install_requires


INSTALL_REQUIRES = get_install_requirements(INSTALL_REQUIRES, ALT_INSTALL_REQUIRES)

setuptools.setup(
    name="split_qr_exam",
    version="0.1.1",
    author="Christoph Stahl",
    author_email="christoph.stahl@tu-dortmund.de",
    description="Splits a pdf consisting of multiple exams identified by a QR code on the cover page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christofsteel/split_qr_exam.git",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['split_qr_exam=split_qr_exam.main:main'],
    }

)
