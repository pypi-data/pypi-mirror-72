import setuptools

setuptools.setup(
    name='popd',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
