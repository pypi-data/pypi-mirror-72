import setuptools

setuptools.setup(
    name='django-site-local-middleware',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
