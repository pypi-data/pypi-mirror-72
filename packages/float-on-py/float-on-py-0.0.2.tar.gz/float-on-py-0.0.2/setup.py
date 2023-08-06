import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="float-on-py",
    version="0.0.2",
    author="Stephen Dowsland",
    author_email="stephen.dowsland@newcastle.ac.uk",
    description="Python Wrapper for Float API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NICD-UK/float-on-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'requests',
      ],
)
