from distutils.core import setup

setup(name='zss',
      version='1.1.4',
      description='Tree edit distance using the Zhang Shasha algorithm',
      author='Tim Henderson',
      author_email='tim.tadh@gmail.com',
      url='https://www.github.com/timtadh/zss',
      packages=['zss'],
      install_requires=['six'],
      requires=['editdist', 'numpy', 'six'],
)
