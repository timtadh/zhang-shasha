from distutils.core import setup

setup(name='zss',
      version='1.0',
      description='Tree edit distance using the Zhang Shasha algorithm',
      author='Tim Henderson',
      author_email='tim.tadh@gmail.com',
      url='https://www.github.com/timtadh/sleepytree',
      packages=['zss'],
      requires=['editdist']
)
