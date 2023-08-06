import setuptools

setuptools.setup(
    name='dir-exec',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/dir-exec']
)
