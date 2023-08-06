# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['bingads==13.0.2']

setup_kwargs = {
    'name': 'arcane-bing',
    'version': '0.1.4',
    'description': 'Helpers to request bing API',
    'long_description': '# Arcane bing\n\nThis package is based on [bingads](https://docs.microsoft.com/en-us/advertising/guides/request-download-report?view=bingads-13).\n\n## Get Started\n\n```sh\npip install arcane-bing\n```\n\n## Example Usage\n\n```python\nbing_client = Client(\n    credentials=Config.BING_ADS_CREDENTIALS,\n    secrets_bucket=Config.SECRETS_BUCKET,\n    refresh_token_location=Config.BING_ADS_REFRESH_TOKEN,\n    storage_client=storage_client\n)\n\nreporting_service_manager, reporting_service = bing_client.get_bing_ads_api_client()\n\nreport_request = build_campaigns_report(reporting_service, bing_account_id)\n\nresult_file_path = bing_client.submit_and_download(report_request, reporting_service_manager)\n```\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
