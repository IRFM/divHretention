import setuptools

setuptools.setup(
    name="divHretention",
    version="0.1.3",
    author="Remi Delaporte-Mathurin",
    author_email="rdelaportemathurin@gmail.com",
    description="Tool to estimate H retention in tokamak divertors",
    url="https://github.com/IRFM/divHretention",
    packages=setuptools.find_packages(),
    package_dir={"divHretention": "divHretention"},
    data_files=[("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.19',
        'scipy>=1.5',
        'inference-tools==0.5.4',
        'matplotlib>=3.3',
    ],
    zip_safe=True,
    include_package_data=True,
)
