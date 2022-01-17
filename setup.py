from setuptools import setup, find_packages

setup(
    name="minimizer",
    description="Locate bugs in your program",
    author="Lucas Galery Käser",
    author_email="lucas.galerykaeser@gmail.com",
    url="https://github.com/aibasel/minimizer",
    license="GPL3+",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "slurm-template": ["minimizer/grid/slurm-array-job.template"],
    },
    install_requires=[
        "simplejson",  # optional, speeds up reading properties files
    ]
)
