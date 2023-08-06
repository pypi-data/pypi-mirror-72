from setuptools import setup


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='prayikta',
      version='0.3',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['prayikta'],
      author = 'Manish Soni',
      author_email = 'manish.soni8403@gmail.com',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)
