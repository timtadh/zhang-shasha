from distutils.core import setup

setup(name='foo',
      version='1.0',
      description='Tree edit distance using the Zhang Shasha algorithm',
      author='Steve Johnson',
      author_email='steve.johnson.public@gmail.com',
      url='https://www.github.com/irskep/sleepytree',
      packages=['sleepytree'],
      requires=['editdist']
      )