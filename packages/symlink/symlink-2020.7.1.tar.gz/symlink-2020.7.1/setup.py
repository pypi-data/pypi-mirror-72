import setuptools

setuptools.setup(
    name='symlink',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
