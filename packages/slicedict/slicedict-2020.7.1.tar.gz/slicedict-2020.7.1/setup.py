import setuptools

setuptools.setup(
    name='slicedict',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
