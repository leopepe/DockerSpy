from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name='dockerspy',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/leopepe/DockerSpy',
    license='Simplified BSD',
    author='Leonardo Pepe',
    author_email='lpepefreitas@gmail.com',
    description='Spy docker API and add nginx configuration upon docker starts and stops events',
    zip_safe=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['dockerspy = dockerspy.__main__:main'],
        'setuptools.installation': ['eggsecutable = dockerspy.__main__:main'],
    }
)
