from distutils.core import setup

import zss

setup(name='zss',
      version=zss.__version__,
      description='Tree edit distance using the Zhang Shasha algorithm',
      author='Tim Henderson',
      author_email='tim.tadh@gmail.com',
      url='https://www.github.com/timtadh/zss',
      packages=['zss'],
      requires=['editdist', 'numpy']
)
