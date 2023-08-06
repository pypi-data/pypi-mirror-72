# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swagger_render']

package_data = \
{'': ['*'],
 'swagger_render': ['static/swagger_render/*', 'templates/swagger_render/*']}

setup_kwargs = {
    'name': 'django-swagger-render',
    'version': '0.1.1',
    'description': 'Swagger documentation in Django',
    'long_description': "# Django Swagger Render\n\n## Getting Started\n\n### Prerequisites\n\n- python >= 3.5\n- Django >= 2.0\n\n### Installation\n\nInstall using pip\n\n```\npip install django-swagger-render\n```\n\nAdd 'swagger_render' to your INSTALLED_APPS setting.\n\n```\nINSTALLED_APPS = [\n    ...\n    'swagger_render',\n]\n```\n\nCreate the folder where you will store your documentation\n\n```\nmkdir docs\n```\n\nCreate the `index.yml` file with some `OPENAPI` or `Swagger` specifications\n\n```\ntouch docs/index.yml\n```\n\nServe your documentation files\n```\nurlpatterns += static('/docs/', document_root='docs')\n```\n\nAdd `SWAGGER_YAML_FILENAME` setting to your `settings.py`\n\n```\nSWAGGER_YAML_FILENAME = '/docs/index.yml'\n```\n\nAdd the `SwaggerUIView` to your urls\n\n```\nfrom swagger_render.views import SwaggerUIView\n\n\nurlpatterns = [\n    ...\n    path('swagger/', SwaggerUIView.as_view()),\n]\n```\n\nVoila!\n",
    'author': 'Emir Amanbekov',
    'author_email': 'amanbekoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/progremir/django-swagger-render',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
