import setuptools

setuptools.setup(
    name="pso-solver",
    version="0.2.1",
    author="Nikhil Kumar",
    author_email="nikhilkmr300@gmail.com",
    description="A package that implements the particle swarm optimization algorithm and provides visualizations.",
    long_description="Refer https://github.com/nikhilkmr300/pso_solver/blob/master/README.md for description.",
    url="https://github.com/nikhilkmr300/pso_solver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'numpy>=1.18',
      'matplotlib>=3.2',
      'tqdm>=4.46'
    ],
    python_requires='>=3.6',
)
