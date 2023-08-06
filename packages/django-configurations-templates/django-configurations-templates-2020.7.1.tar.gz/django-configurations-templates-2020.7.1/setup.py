import setuptools

setuptools.setup(
    name='django-configurations-templates',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
