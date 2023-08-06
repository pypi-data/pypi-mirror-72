import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(name="thad-roberts-model",
      version = '0.1.5.2',
      description = "Thad Roberts Model Library",
      long_description = long_description,
      long_description_content_type = "text/markdown",
      url = 'https://github.com/lukaszp/thad-roberts-model.git',
      author = 'Lukasz Paszke',
      author_email = 'lukasz.paszke@gmail.com',
      license = 'MIT',
      packages = setuptools.find_packages(),
      install_requires = [],
      extras_require = {'dev': ['twine']},
      classifiers = ["Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent"],
      python_requires = '>=3.8')