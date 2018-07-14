from setuptools import setup

setup(name='buildStatusSignClient',
      version='0.1',
      description='',
      url='http://github.com/papertrailio/buildStatusSignClient',
      author='robwalkerco',
      author_email='rob@papertrail.io',
      license='MIT',
      packages=['buildStatusSignClient'],
      install_requires=[
          'RPi.GPIO',
          'requests',
          'python-firebase',
      ],
      zip_safe=False)
