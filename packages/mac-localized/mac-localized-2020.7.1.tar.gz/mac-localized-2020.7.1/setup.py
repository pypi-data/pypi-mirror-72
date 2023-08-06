import setuptools

setuptools.setup(
    name='mac-localized',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
