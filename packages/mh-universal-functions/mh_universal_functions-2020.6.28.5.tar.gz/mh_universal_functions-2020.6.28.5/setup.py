import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("mh_universal_functions/_version.py").read())

setuptools.setup(
      name='mh_universal_functions',
      version=__version__,
      author='MH',
      author_email='ibhmduu1721nhg11.11@o2mail.de',
      description='General functions library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://pypi.org/project/mh-universal-functions',
      packages=setuptools.find_packages(),
      license='MIT',
      python_requires='>=3.7',
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False
)

# Source:
# https://martin-thoma.com/python-package-versions
