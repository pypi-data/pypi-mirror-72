
import setuptools

with open("README.md", "r") as fh:
    README = fh.read()

setuptools.setup(
    name='sideex-webservice-client', # Replace with your own username
    version='0.9.0',
    author='SideeX Team',
    author_email='feedback@sideex.io',
    description='SideeX WebService Client API for Python handles the transfer of test suites to a self-hosted SideeX WebService server and returns the test reports.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SideeX/sideex-webservice-client-api-python",
    packages=setuptools.find_packages(),
    classifiers=[  # Optional
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      # Pick your license as you wish
      'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3',
)