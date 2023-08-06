from setuptools import find_packages, setup


setup(name='pyzpipe',
      version='0.1',
      description='Concurrent and parallel pipeline framework using ZMQ',
      url='https://github.com/jheo4/zpipe',
      author='jheo4',
      author_email='993jin@gmail.com',
      license='MIT',
      zip_safe=False,
      python_requires="<=3.6",
      packages=find_packages(exclude=["examples"]),
      install_requires=[
          'numpy>=1.19.0',
          'pyzmq>=19.0.1',
          ],
      extras_require={
          "pyopencv": ['opencv-python==3.4.2', 'opencv-contrib-python==3.4.2'],
          "vidgear": ['vidgear>=0.1.8'],
          "dev": ["flake8==3.7.9", "black==19.10b0", "pytest==5.4.1"],
          },
      )
