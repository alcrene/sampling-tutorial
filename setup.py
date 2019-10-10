
# >>>>> See https://github.com/pypa/sampleproject/blob/master/setup.py <<<<<<

from setuptools import setup

setup(
      name='sampling-tutorial',
      version='0.1',
      description="",

      author="Alexandre René",
      author_email="arene010@uottawa.ca",

      license='MIT',

      # >>>>>> See https://pypi.org/classifiers/ <<<<<<<<
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only'
      ],
      
      python_requires='>=3.6',
      
      packages=["sampling_tutorial"],

      install_requires=['numpy']
     )
