from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup (
    name="MutationChecker", 
    version="0.0.1",
    description="Package for the computation of distances from a residue to the catalytic active residues.",
    py_modules=["MutationChecker"],
    package_dir={"":"src"},
    requirements = [
        "biopython", 
        "requests"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
exit()
