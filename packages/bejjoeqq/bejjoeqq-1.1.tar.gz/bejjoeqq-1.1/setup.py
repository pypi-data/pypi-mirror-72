from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='bejjoeqq',
  version='v1.1',
  description='Trial Library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Aldhiya Rozak',
  author_email='Aldhiya.rozak@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='Indonesian Library',
  packages=find_packages(),
  install_requires=['']
)
