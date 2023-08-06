import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clp", # Replace with your own username
    version="0.0.0",
    author="Rehan Guha",
    py_modules=["clp"],
    license='mit',
    author_email="rehanguha29@gmail.com",
    description="Container Loading Problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rehanguha/Container-Loading-Problem",
    package_dir={'': 'clp'},
    packages=setuptools.find_packages(),
    keywords = ['container loading problem', 'bin packing problem', 'packing', 'loading'],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Scientific/Engineering",
        'Intended Audience :: Developers',
    ],
    python_requires='>=2.7',
    install_requires=['numpy'],
)
