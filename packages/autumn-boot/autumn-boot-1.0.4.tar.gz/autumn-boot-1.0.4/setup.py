import setuptools

setuptools.setup(
    name='autumn-boot',
    version='1.0.4',
    author='Ferencz Albert',
    author_email='split@aferencz.xyz',
    description='A framework to build event-driven backend solutions',
    long_description='',
    url='https://bitbucket.org/AlphaSpliT/autumn',
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.6',
    install_requires=[
        'asyncio',
        'websockets',
        'python-dotenv',
        'click',
        'pymongo',
    ],
    setup_requires=['wheel']
)
