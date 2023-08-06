from setuptools import setup

setup(
  name='primeTester',
  version='0.1',
  description='Say hello!',
  py_modules=["aks", "fermat",  "millerRabin", "solovayStrassen", "trialDivision"],
  package_dir={'': 'src'},
  url='https://github.com/avrha/Prime-Tests',
  liscene="MIT",
  author="Joey Ferenchak",
  author_email="sjferenchak@gmail.com",
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
