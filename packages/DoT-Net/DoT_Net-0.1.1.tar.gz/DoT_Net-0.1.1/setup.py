import setuptools
import wtforms

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DoT_Net",
    version="0.1.1",
    author="Sai Kosaraju",
    author_email="kosaraju@unlv.nevada.edu",
    description="Document Extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datax-lab/DoTNet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
