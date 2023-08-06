import setuptools

setuptools.setup(
    name='mac-headphones',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/headphones']
)
