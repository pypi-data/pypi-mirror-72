import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorgrab", # Replace with your own username
    version="0.0.1",
    author="xepha",
    author_email="magneticrex@gmail.com",
    description="gets a pixel from your screen and spits out the hex value (e.g #0A0EFE)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julianPescobar/colorgrab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
