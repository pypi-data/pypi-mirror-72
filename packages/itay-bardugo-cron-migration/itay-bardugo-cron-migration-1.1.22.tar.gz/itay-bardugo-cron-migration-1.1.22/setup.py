import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

cur_directory_path = os.path.abspath(os.path.dirname(__file__))
main_path = os.path.dirname(os.path.realpath(__file__))
requirements_file = main_path + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_file):
    with open(requirements_file) as f:
        while (line := f.readline()):
            if not line.startswith("-"):
                install_requires.append(line.strip())

setuptools.setup(
    name="itay-bardugo-cron-migration", # Replace with your own username
    version="1.1.22",
    author="Itay Bardugo",
    author_email="itaybardugo91@gmail.com",
    description="manage your cron jobs with python and a revision system(CLI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itay-bardugo/python-cron-migration",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"templates": ["*"]},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            'cronmig=cron_migration.cli.commands:cronmig',
            'cronmig-revision=cron_migration.cli.commands:revision',
        ]
    },
    python_requires='>=3.8.3',
)
