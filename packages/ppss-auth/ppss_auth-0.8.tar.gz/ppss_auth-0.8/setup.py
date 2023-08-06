from setuptools import setup,find_packages


import os
here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.md'), 'r').read()
changelog = open(os.path.join(here, 'README.md'), 'r').read()

setup(name='ppss_auth',
  version='0.8',
  description='simple auth scheme for pyramid, based on Mako template and sqlalchemy backend',
  long_description=readme + "\n\n\n" + changelog,
  long_description_content_type="text/markdown",
  author='pdepmcp',
  author_email='d.cariboni@pingpongstars.it',
  license='MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Framework :: Pyramid',
    'Topic :: Internet :: WWW/HTTP :: Session',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
  ],
  keywords="pyramid module authentication accelerator",
  python_requires='>=2.7',
  url='http://www.pingpongstars.it',
  install_requires=['pyramid_mako','pyramid_beaker','pyramid_jinja2' ],
  #packages=['src/test1'],
  packages=find_packages(),
  include_package_data=True,
  entry_points={
    'console_scripts': [
            'initialize_ppss_auth_db=ppss_auth.scripts.initialize_db:main',
            'ppss_auth_upgrade_db=ppss_auth.scripts.upgrade_db:main',
            'sayauth=ppss_auth.scripts.sayauth:sayitnow',
    ],
  }

)


