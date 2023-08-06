import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swea",
    version="0.0.1",
    author="John Kang",
    auther_email="john@hphk.kr",
    description="SWEA Problem Set Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hp-hk/swea.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'swea=swea.scripts:main'
        ]
    }
)