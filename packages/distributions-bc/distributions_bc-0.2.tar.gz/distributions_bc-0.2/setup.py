from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(name='distributions_bc',
      version='0.2',
      author='Charles Gauthey',
      author_email='cjgauthey@gmail.com',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      classifiers=[
          "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False,
      python_requires='>=3.6'
      )
