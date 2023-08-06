from distutils.core import setup
setup(
  name = 'aiohttp-swagger-fix',         
  packages = ['aiohttp_swagger'],   
  version = '1.0.15',
  license='MIT',        
  description = 'Fix of aiothttp-swagger',   
  author = 'Daan Klijn',                   
  author_email = 'daanklijn0@gmail.com',      
  url = 'https://github.com/daanklijn/aiohttp-swagger',   
  download_url = 'https://github.com/daanklijn/aiohttp-swagger/archive/1.0.15.tar.gz',    
  keywords = ['aiohttp', 'swagger'],   
  install_requires=[            
	'pyYAML>=5.1',
	'jinja2~=2.8',
	'aiohttp>=2.3.10'
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
