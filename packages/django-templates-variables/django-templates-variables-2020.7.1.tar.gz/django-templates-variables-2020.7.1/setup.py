import setuptools

setuptools.setup(
    name='django-templates-variables',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
