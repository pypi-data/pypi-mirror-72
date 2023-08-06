import setuptools

setuptools.setup(
    name="cloudflow",
    version="0.0.1",
    author="Victor Martins",
    author_email="victor.martins.dpaula@gmail.com",
    description="AWS DAGs utility",
    url="https://github.com/victormpa/cloudflow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
