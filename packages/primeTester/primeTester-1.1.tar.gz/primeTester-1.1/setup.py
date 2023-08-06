from setuptools import setup

with open("README.md", "r") as fh:
      long_description = fh.read()
setup(
    name='primeTester',
  version='1.1',
  description='A collection of Python modules consisting different primality tests.',
  py_modules=["aks", "fermat",  "millerRabin", "solovayStrassen", "trialDivision"],
  package_dir={'': 'src'},
  url='https://github.com/avrha/Prime-Tests',
  liscene="MIT",
  author="Joey Ferenchak",
  author_email="sjferenchak@gmail.com",
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
