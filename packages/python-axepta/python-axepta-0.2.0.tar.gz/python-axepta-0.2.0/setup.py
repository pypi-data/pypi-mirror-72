from setuptools import setup

setup(name='python-axepta',
      version='0.2.0',
      description='Axepta BNP Paribas SOAP Client',
      url='https://bitbucket.org/metadonors/python-axepta',
      author='Metadonors S.r.l.',
      author_email='edoardo.nodari@metadonors.it',
      license='MIT',
      packages=['pyaxepta'],
      install_requires=[
          'zeep',
      ],
      zip_safe=False)
