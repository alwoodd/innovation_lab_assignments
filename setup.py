from setuptools import setup, find_packages
print(find_packages())
setup(
    name='innovation_lab_assignments',
    version='1.0.0',
    author='Dan Alwood',
    author_email='dalwood@yahoo.com',
    description='Generate innovation lab sheets from Google Forms data',
    package_dir={'':'src'},
    packages=["innovation_lab_assignments"],
    package_data={'':['*.json']},
    install_requires=[],                # Add any dependencies if necessary
)