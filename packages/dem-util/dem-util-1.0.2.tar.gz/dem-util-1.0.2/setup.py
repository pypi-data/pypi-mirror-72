from setuptools import setup, find_packages


setup(
    name='dem-util',
    version='1.0.2',
    url="https://github.com/BetaS/pydemutil",
    author="BetaS",
    author_email="thou1999@gmail.com",
    description="DEM slope modeling and imaging with trilinear interpolation",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pyproj',
        'shapely',
        'cairocffi',
        'scour'
    ],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
            "License :: OSI Approved :: MIT License"
    ]
)