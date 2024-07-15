from setuptools import setup, find_packages

setup(name='amanzi',
      version='0.1.2',
      description='Back-end of SLIMM Designer',
      url='https://github.com/Vitens/amanzi',
      author='Abel Heinsbroek',
      author_email='abel.heinsbroek@vitens.nl',
      license='GNU Lesser General Public License v3 (LGPLv3)',
      packages=find_packages('.'),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy',
          'phreeqpython',
          'pandas',
          'scipy',
      ])
