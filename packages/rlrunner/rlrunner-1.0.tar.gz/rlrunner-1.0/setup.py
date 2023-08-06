import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rlrunner",
    version="1.0",
    author="Miguel Martins",
    author_email="mfmartins1996@gmail.com",
    description="A framework for Reinforcement Learning experimentation and run simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PriestTheBeast/RLRunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
          'numpy',
          'gym',
          'matplotlib'
    ],
    python_requires='>=3.6',
)