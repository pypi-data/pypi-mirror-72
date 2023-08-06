import setuptools

setuptools.setup(
    name='django-celery-task-queue',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
