import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyTextMiner", # Replace with your own username
    version="1.1.1",
    author="Min Song",
    author_email="min.song@yonsei.ac.kr",
    description="A text mining tool for Korean and English",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinSong2/pyTextMiner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)