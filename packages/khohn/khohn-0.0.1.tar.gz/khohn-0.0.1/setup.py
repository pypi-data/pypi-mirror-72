import distutils.core
import distutils.ccompiler
import os
from khohn.version import KHOHN_PROJ, KHOHN_VERSION_STRING

                                         
_destination_vers_dir = lambda folder: "/".join([KHOHN_PROJ, KHOHN_VERSION_STRING, folder])
  
KHOHN_C_SOURCE_DIR = "src"
KHOHN_C_HEADER_DIR = "include"

def _get_files_under_dir(local_dir):
    flist = os.listdir(os.path.join(os.path.dirname(__file__), local_dir))
    return [os.path.join(local_dir, file) for file in flist]
    
def _generate_install_files(dir_pairs):
    return [(k, _get_files_under_dir(v)) for k, v in dir_pairs.items()]
    

FILES_TO_PACKAGE = _generate_install_files({
     "khohn/0.0.1/csrc":KHOHN_C_SOURCE_DIR,
     "khohn/0.0.1/cinclude":KHOHN_C_HEADER_DIR
})
          
          
keyword_list = [
    'thai',
    'thailand',
    'thai language',
    'thai nlp',
    'thai search',
    'big data',
    'full text',
    'text search',
    'data science'
]

classifers_list = [
    'Development Status :: 2 - Pre-Alpha',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Natural Language :: Thai',
    'License :: OSI Approved :: MIT License'
]

macro_defs = []

if os.name == 'nt':
  macro_defs.append(('_CRT_SECURE_NO_WARNINGS', '1'))

# This goes under the main khohn package
# Will be linked with the C library later on 
core_module = distutils.core.Extension('khohn.core',
                    define_macros = macro_defs,
                    include_dirs = ['include'],
                    sources = ['pyext/pymain.c'])

distutils.core.setup(name='khohn',
      version=KHOHN_VERSION_STRING,
      description='A library for searching and analyzing Thai data',
      author='Joshua Weinstein',
      author_email='jweinst1@berkeley.edu',
      url='https://github.com/jweinst1/khohn',
      download_url='https://github.com/jweinst1/khohn/archive/master.zip',
      license = 'MIT',
      keywords = keyword_list,
      classifiers = classifers_list,
      long_description = open('README.md').read(),
      packages=['khohn'],
      py_modules=['khohn.version'],
      ext_modules=[core_module],
      data_files=FILES_TO_PACKAGE,
     )