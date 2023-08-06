import setuptools

# *---------------------------------------------------------------------------*
# * Including ReadMe Markdown File in the setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
# *---------------------------------------------------------------------------*
setuptools.setup(
    name="gitlas",  
    version=" 0.1.02",
    author="Abhi-1U",
    author_email="PerricoQ@outlook.com",
    description="A minimalist git log Statistics library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abhi-1U/gitlas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
# *---------------------------------------------------------------------------*
