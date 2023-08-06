from setuptools import setup

with open('pyprob_distributions/README.md') as f:
    long_description = f.read()

setup(name='pyprob_distributions',
      version='0.2',
      description='Gaussian and Binominal distributions',
      packages=['pyprob_distributions'],
      author = 'Adithya Yelloju',
      author_email = 'adithyayelloju@gmail.com',
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/AdithyaYelloju/pyprob-distributions',
      zip_safe=False)
