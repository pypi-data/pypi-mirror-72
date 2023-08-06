import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='EZlogR',
    version='0.2.0.dev6',
    author='Jeremy Gillespie',
    author_email='jeremy@kodeslingr.com',
    url='http://www.ezlogr.com',
    license='MIT',
    description='This is a simple logging tool to help devs focus on writing code instead of writing logs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    package_dir = {"": "src"},
    packages=setuptools.find_namespace_packages(where="src")
)
