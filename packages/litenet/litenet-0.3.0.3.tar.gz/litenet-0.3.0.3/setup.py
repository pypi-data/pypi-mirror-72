from setuptools import setup

setup(
    name='litenet',
    version='0.3.0.3',
    packages=['litenet'],
    url='https://github.com/GrandMoff100/LiteNet',
    license='MIT LIcence',
    author='',
    author_email='',
    description='A socket-based client messaging service.',
    install_requires=["click", "keyboard"],
    entry_points={
        "console_scripts":["litenet=litenet.cli:cli"]
    }
)
