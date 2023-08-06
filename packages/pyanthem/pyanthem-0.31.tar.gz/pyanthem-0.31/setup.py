import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
    name="pyanthem",
    version="0.31",
    author="Nic Thibodeaux",
    author_email="dnt2111@columbia.edu",
    description="py-anthem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicthib/neuroauvi",
    packages=setuptools.find_packages(),
    setup_requires=['numpy'],
    install_requires=['scipy',
        'soundfile',
        'midiutil',
        'GitPython',
        'matplotlib',
        'pygame',
        'opencv-python',
        'sklearn',
      ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# For MANIFEST:
# recursive-include pyanthem/AE *.ogg
# recursive-include pyanthem/AE/scaledata.csv
# recursive-include pyanthem/AE *.txt

