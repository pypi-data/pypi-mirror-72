from distutils.core import setup
from pathlib import Path
# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'freshlybuiltimagebol',         
  packages = ['freshlybuiltimagebol'],   
  version = '0.0.2.1',     
  license='MIT',        
  description = 'Photo Bhi Bol Uthega',
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'Vishal Sharma',                   
  author_email = 'vishalsharma.gbpecdelhi@gmail.com',      
  url = 'https://github.com/FreshlyBuilt/freshlybuiltimagebol',   
  download_url = 'https://github.com/FreshlyBuilt/freshlybuiltimagebol/archive/v0.0.2.1.tar.gz',  
  keywords = ['Image', 'Audio', 'Text'],   
  install_requires=[            
          'hyper',
          'googletrans',
          'gTTS',
          'Pillow',
          'pytesseract',
          'opencv-python',
          'numpy',
          'matplotlib',
          'imutils'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
