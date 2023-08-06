import setuptools

setuptools.setup(
    name='kill-child-processes',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/kill-child-processes']
)
