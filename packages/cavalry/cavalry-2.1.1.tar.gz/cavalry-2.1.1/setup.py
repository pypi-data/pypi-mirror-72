import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cavalry",
    version="2.1.1",
    author="Sean Christians",
    author_email="seanchristians.scc@gmail.com",
    description="Secrets manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanchristians/cavalry",
    packages=["cavalry"],
    package_dir={"cavalry": "src"},
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
    ],
    scripts=["src/cav"],
    python_requires=">=3.8",
)
