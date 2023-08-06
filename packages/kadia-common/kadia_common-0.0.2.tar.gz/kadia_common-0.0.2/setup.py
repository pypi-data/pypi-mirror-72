from distutils.core import setup

setup(name='kadia_common',
      version='0.0.2',
      description='The common code for Kadia voice assistant',
      author='Andrew Ishutin',
      author_email='hazmozavr@gmail.com',
      url='https://github.com/kadia-iva/kadia',
      packages=['kadia_common'],
      install_requires=[
        'pydantic'
      ]
     )
