
from distutils.core import setup
setup(
  name = 'z43_styles',
  packages = ['z43_styles'],
  version = '0.2',
  license='MIT',
  description = 'Z43 plotly templates',
  author = 'Odei Maiz',
  author_email = 'maiz@itis.swiss',
  url = 'https://github.com/odeimaiz/z43_plot_styles',
  download_url = 'https://github.com/odeimaiz/z43_plot_styles/archive/v_01.tar.gz',
  keywords = ['PLOTLY', 'TEMPLATES', 'Z43'],
  install_requires=[
    'plotly',
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
