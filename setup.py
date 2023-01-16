from setuptools import setup, find_packages, find_namespace_packages

# setup(
#     name='dmm2bm',
#     version=open('VERSION').read().strip(),
#     #version=__version__,
#     author='Francesco De Carlo',
#     author_email='decarlof@gmail.com',
#     url='https://github.com/decarlof/dmm',
#     packages=find_namespace_packages(where="dmm2bm"),
#     package_dir={"": "dmm2bm"},
#     include_package_data = True,
#     scripts=['bin/dmm'],
#     description='ops',
#     zip_safe=False,
# )

setup(
    name='dmm2bm',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/decarlof/dmm',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/dmm'],
    description='ops',
    zip_safe=False,
)