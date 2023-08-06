from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pySTLtools",
    version="0.0.1",
    description="A Python package for mathematical tools like in STL of C++",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rkat7/pySTL",
    author="Rohith Kattamuri",
    author_email="skrishrkat7@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    py_modules=["pySTLtools"],
    package_dir={'':'src'},
    setup_requires=['wheel'],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    #packages=["pySTL"],
    
)