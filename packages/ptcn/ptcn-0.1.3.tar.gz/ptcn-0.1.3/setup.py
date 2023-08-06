# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptcn']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-addons>=0.10.0,<0.11.0', 'tensorflow>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'ptcn',
    'version': '0.1.3',
    'description': 'TF2 implementation of a Temporal Convolutional Network with a probabilistic twist',
    'long_description': '# ptcn\n\nTensorflow (2.x) implementation of a Temporal Convolutional Network architecture, with a probabilistic twist.\n\nThis project indulges a couple of curiosities:\n\n1. Working with convolutional sequence-to-sequence models a la [An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling](https://arxiv.org/abs/1803.01271)\n2. Adding a bayesian twist to the network a la [Bayesian Segnet: Model Uncertainty in Deep Convolutional Encoder-Decoder Architectures for Scene Understanding](https://arxiv.org/abs/1511.02680)\n\nThis implementation has been inspired by other projects, including:\n- https://github.com/locuslab/TCN\n- https://github.com/Baichenjia/Tensorflow-TCN\n- https://github.com/philipperemy/keras-tcn\n',
    'author': 'UpstatePedro',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UpstatePedro/ptcn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
