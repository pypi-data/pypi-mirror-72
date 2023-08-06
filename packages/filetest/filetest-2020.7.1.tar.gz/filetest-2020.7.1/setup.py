import setuptools

setuptools.setup(
    name='filetest',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
