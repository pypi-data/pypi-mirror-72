from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Natural Language :: Portuguese (Brazilian)',
  'Topic :: Software Development :: Libraries'
]

setup(
  name='FMOARPG',
  version='0.0.6',
  description='Biblioteca para integrar Forge e Power BI',
  long_description='Esta biblioteca foi desenvolvida para integrar as APIs da plataforma Forge com o Power BI de maneira direta e simplificada',
  url='https://github.com/Jpornelas/MAPyForg/tree/master/MAPyForg',
  author='John Martins',
  author_email='jpornelas@poli.ufrj.br',
  license='MIT',
  classifiers=classifiers,
  keywords='Forge',
  packages=find_packages(),
  install_requires=['']
)