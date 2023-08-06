import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='psssodls',
      version='0.3',
      description='Generate PSSSODLS in Minion 3 format.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      url='https://gitlab.com/MHenderson1/psssodls-generator',
      author='Matthew Henderson',
      author_email='matthew.james.henderson@gmail.com',
      license='MIT',
      scripts=['bin/psssodls'],
      zip_safe=False)
