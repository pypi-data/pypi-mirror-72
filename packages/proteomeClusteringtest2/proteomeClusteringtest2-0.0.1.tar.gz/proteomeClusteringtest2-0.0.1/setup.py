import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proteomeClusteringtest2", # Replace with your own username
    version="0.0.1",
    author="Tse-Ming Chen",
    author_email="benben5514@gmail.com",
    description="proteomeClustering test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zytyz/ProteomeClustering",
    project_urls={
            "Documentation": "https://pillow.readthedocs.io" },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
