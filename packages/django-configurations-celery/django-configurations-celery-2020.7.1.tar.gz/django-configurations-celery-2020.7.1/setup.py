import setuptools

setuptools.setup(
    name='django-configurations-celery',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
