#  #!/usr/bin/env python
  
# from distutils.core import setup,Extension
from setuptools import setup

setup(name="thorsky",
        version="1.0",
        description="Python based skycalc GUI",
        url="http://www.dartmouth.edu",
        author = "John Thorstensen",
        author_email = "John.Thorstensen@dartmouth.edu",
        packages=['thorsky'],
        scripts=['bin/pyskycalc3.py'],
        include_package_data=True)
#        scripts = ['pyskycalc3.py'],
#        py_modules=['thorskyclasses3','thorskyutil'],
#        data_files=[('/usr/local/share/skycalc',['observatories_rev.dat','cartesian_bright.dat'])])

