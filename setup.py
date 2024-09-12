import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "versatile-audio-upscaler"
DESCRIPTION = "Versatile AI-driven audio upscaler to enhance the quality of any audio."
URL = "https://github.com/IAHispano/Audio-Upscaler"
EMAIL = "blaise@applio.org"
AUTHOR = "Pascal Aznar"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.2"

REQUIRED = [
    "torch>=1.13.0",
    "torchaudio>=0.13.0",
    "torchvision>=0.14.0",
    "tqdm",
    "pyyaml",
    "einops",
    "chardet",
    "numpy<=1.23.5",
    "soundfile",
    "librosa==0.9.2",
    "scipy",
    "pandas",
    "tokenizers>=0.14.1",
    "unidecode",
    "phonemizer",
    "torchlibrosa>=0.0.9",
    "transformers",
    "wget",
    "progressbar",
    "ftfy",
    "timm",
    "matplotlib",
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # packages=find_packages(exclude=[]),
    # If your package is a single module, use this instead of 'packages':
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    packages=find_packages(),
    package_data={
        "audio_upscaler": [
            "*/*.py",
            "*/*/*.py",
            "*/*/*/*.py",
            "*/*/*/*/*.py",
            "*/*.npy",
            "*/*/*.npy",
            "*/*.gz",
            "*/*/*.gz",
            "*/*.json",
            "*/*/*.json",
            "*/*/*/*.json",
        ]
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
