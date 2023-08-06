from setuptools import setup

setup(name='simple_prob_distributions',
      version='1.1.3',
      author = 'Haard Shah',
      author_email = 'haard2013@gmail.com',
      description='Normal (Gaussian) and Binomial distributions',
      packages=['simple_prob_distributions'],
      url = 'http://pypi.org/pypi/simple-prob-distributions',
      license = 'license.txt',
      zip_safe=False,
      install_requires = [
          'matplotlib>=2.1.0'
      ]
     )
