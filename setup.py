import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspectra", # Replace with your own username
    version="0.0.1.2",
    author="Oscar Ureña",
    author_email="oscar.enrique.urena@gmail.com",
    description="A  python package designed to work with spectroscopy data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OEUM/PySpectra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy','pandas','spc_spectra','scipy'],
    keywords=['spectroscopy', 'nir', 'ftir', 'raman', 'spc','dx','foss','viavi','grams']
)