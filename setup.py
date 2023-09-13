import os
import re

from distutils.core import setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = [
  'kubernetes>=27.2.0,<28.0.0'
],

def get_version():
    init = open(os.path.join(ROOT, 'python_kubernetes_tools', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)
  
setup(name='python-pulumi-helm',
      version=get_version(),
      description='Python Kubernetes tools',
      url='https://github.com/luismiguelsaez/python-kubernetes-tools',
      install_requires=requires
)
