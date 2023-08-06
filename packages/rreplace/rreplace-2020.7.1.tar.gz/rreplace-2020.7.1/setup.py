import setuptools

setuptools.setup(
    name='rreplace',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
