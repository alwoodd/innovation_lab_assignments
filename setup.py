from setuptools import setup
setup(
    name='innovation_lab_assignments',
    version='2.1.0',
    author='Dan Alwood',
    author_email='dalwood@yahoo.com',
    description='Generate innovation lab sheets from Google Forms data',
    package_dir={'':'src'},
    packages=["innovation_lab_assignments",
              "config_editor",
              "innovation_lab_assignments_ui"],
    include_package_data=True,  # Allows MANIFEST.in to control included files
    install_requires=["my_utilities >= 1.0.0"]
)