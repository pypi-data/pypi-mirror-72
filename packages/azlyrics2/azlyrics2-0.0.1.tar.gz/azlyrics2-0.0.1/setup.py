import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="azlyrics2",
      version="0.0.1",
      url="https://github.com/bngom/azlyrics",
      author="Barthelemy NGOM",
      author_email="barthe.ngom@gmail.com",
      description=" Extends azlyrics 'API' and CLI program to fetch lyrics from azlyrics",
      install_requires=["azlyrics"],
      packages=setuptools.find_packages(),
      license="MIT",
      classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
      ],
      entry_points = {
          'console_scripts': [
              'azlyrics2 = azlyrics2:run'
          ]
      })