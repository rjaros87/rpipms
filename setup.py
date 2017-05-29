from setuptools import setup

setup(name='rpipms',
      version='0.1.0',
      description='',
      url='https://github.com/rjaros87/rpipms',
      author='Radoslaw Jaros',
      author_email='',
      license='Apache-2.0',
      packages=['rpipms'],
      install_requires=[
          "pyyaml>=3.12",
          "pyserial>=3",
          "luma.core>=0.9.1",
          "luma.oled>=2.2.10"
      ],
      zip_safe=False)