from setuptools import setup

setup(name='svautil',
      version='0.0.3',
      description='Converts CSV files from Sigilent Vector Spectrum Analyzers to a Scikit RF network.',
      url='https://github.com/norsk-datateknikk/SVA-Utility',
      author='Erik Buer',
      author_email='erik.buer@norskdatateknikk.no',
      license='GPL',
      packages=['svautil'],
      zip_safe=False,
      install_requires = [ 'numpy', 'rf-tool', 'scikit-rf'])