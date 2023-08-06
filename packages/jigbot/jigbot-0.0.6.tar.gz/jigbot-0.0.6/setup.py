from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='jigbot',
  version='0.0.6',
  description='Install essential Libraries to create Chatbot',
  url='',  
  author='Jiganesh Patil',
  author_email='jiganeshpatil01071999@gmail.com',
  long_description='Install essential Libraries to create Chatbot and get user data',
  license='MIT', 
  classifiers=classifiers,
  keywords='chatbot',
  packages=find_packages(),
  install_requires=['nltk', 'wikipedia', 'validate_email', 'chatterbot_corpus', 'sklearn', 'numpy']
)
