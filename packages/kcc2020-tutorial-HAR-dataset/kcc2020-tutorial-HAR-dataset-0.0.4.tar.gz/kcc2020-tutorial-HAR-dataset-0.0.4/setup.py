import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kcc2020-tutorial-HAR-dataset',
    version='0.0.4',
    author='Auk Kim',
    author_email='kimauk@kaist.ac.kr',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas'
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ]
)
