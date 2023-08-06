import setuptools

setuptools.setup(
    name='ini2dict',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
