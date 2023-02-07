from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='energy',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/decarlof/energy',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    scripts=['src/energy/energycli.py'],  
    entry_points={'console_scripts':['energy = energycli:main'],},
    description='ops',
    zip_safe=False,
)
