import setuptools

setuptools.setup(
    name='refork',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/refork']
)
