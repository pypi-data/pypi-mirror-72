import setuptools

with open("irLib/README.md", "r") as f:
    long_description = f.read()

dependencies = []
with open("irLib/requirements.txt", "r") as r:
    for line in r.readlines():
        dependencies.append(line.split("==")[0])

setuptools.setup(
    name="interestRateInstrumentsLib",
    version="0.4.0",
    author="Neo Yung",
    author_email="reverie211@gmail.com",
    description="Interest rate instruments library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neoyung/irLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=dependencies
)

