import setuptools

setuptools.setup(
    name="divHretention",
    version="0.1",
    author="Remi Delaporte-Mathurin",
    author_email="rdelaportemathurin@gmail.com",
    description="Tool to estimate H retention in tokamak divertors",
    url="https://github.com/IRFM/divHretention",
    packages=setuptools.find_packages(),
    package_dir={"divHretention": "main"},
    data_files=[("", ["LICENSE.txt"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'scipy',
        'inference-tools',
        'matplotlib',
    ],
    zip_safe=True,
)