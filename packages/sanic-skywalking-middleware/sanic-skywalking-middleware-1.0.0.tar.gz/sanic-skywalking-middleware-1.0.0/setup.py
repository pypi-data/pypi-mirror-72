from setuptools import setup

version = '1.0.0'
url = 'https://github.com/sungitly/wsgi-skywalking-middleware'
download_url = '{}/archive/v{}.tar.gz'.format(url, version)

INSTALL_REQUIRES = ['sanic>=20.6.1', 'apache-skywalking==0.1.0']

setup(
    name='sanic-skywalking-middleware',
    py_modules=['sanic_skywalking_middleware'],
    version=version,
    description='A SkyWalking Agent/Middleware for Sanic Framework.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Lei Sun',
    author_email='leix.sun@qq.com',
    url=url,
    download_url=download_url,
    license='MIT',
    keywords=['sanic', 'skywalking', 'middleware'],
    classifiers=[],
    install_requires=INSTALL_REQUIRES
)
