from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='distributions_bc',
      version='0.1',
      author='Charles Gauthey',
      author_email='cjgauthey@gmail.com',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['distributions_bc'],
      classifiers=[
          "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False,
      python_requires='>=3.6'
      )
