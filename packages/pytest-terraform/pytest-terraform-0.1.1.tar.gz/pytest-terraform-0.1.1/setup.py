# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_terraform']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=0.9.5,<0.10.0', 'portalocker>=1.7.0,<2.0.0', 'pytest>=5.3.5,<5.4.0']

entry_points = \
{'pytest11': ['terraform = pytest_terraform.plugin']}

setup_kwargs = {
    'name': 'pytest-terraform',
    'version': '0.1.1',
    'description': 'A pytest plugin for using terraform fixtures',
    'long_description': '# Introduction\n\n[![CI](https://github.com/cloud-custodian/pytest-terraform/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/cloud-custodian/pytest-terraform/actions?query=branch%3Amaster)\n[![codecov](https://codecov.io/gh/cloud-custodian/pytest-terraform/branch/master/graph/badge.svg)](https://codecov.io/gh/cloud-custodian/pytest-terraform)\n\npytest_terraform is a pytest plugin that enables executing terraform\nto provision infrastructure in a unit/functional test as a fixture.\n\nThis plugin features uses a fixture factory pattern to enable paramterized\nconstruction of fixtures via decorators.\n\n## Usage\n\n```python\nfrom boto3 import Session\nfrom pytest_terraform import terraform\n\n\n# We use the terraform decorator to create a fixture with the name of\n# the terraform module.\n#\n# The test function will be invoked after the terraform module is provisioned\n# with the results of the provisioning.\n#\n# The module `aws_sqs` will be searched for in several directories, the test\n# file directory, a sub directory `terraform`.\n#\n# This fixture specifies a session scope and will be run once per test run.\n#\n@terraform(\'aws_sqs\', scope=\'session\')\ndef test_sqs(aws_sqs):\n    # A test is passed a terraform resources class containing content from\n    # the terraform state file.\n    #\n    # Note the state file contents may vary across terraform versions.\n    #\n    # We can access nested datastructures with a jmespath expression.\n    assert aws_sqs["aws_sqs_queue.test_queue.tags"] == {\n        "Environment": "production"\n    }\n   queue_url = aws_sqs[\'test_queue.queue_url\']\n   print(queue_url)\n\n\ndef test_sqs_deliver(aws_sqs):\n   # Once a fixture has been defined with a decorator\n   # it can be reused in the same module by name, with provisioning\n   # respecting scopes.\n   #\n   boto3.Session().client(\'sqs\')\n   sqs.send_message(\n       QueueUrl=aws_sqs[\'test_queue.queue_url\'],\n       MessageBody=b"123")\n\n@terraform(\'aws_sqs\')\ndef test_sqs_dlq(aws_sqs):\n   # the fixture can also referenced again via decorator, if redefined\n   # with decorator the fixture parameters much match (ie same session scope).\n\n   # Module outputs are available as a separate mapping.\n   aws_sqs.outputs[\'QueueUrl\']\n```\n\n*Note* the fixture name should match the terraform module name\n\n*Note* The terraform state file is considered an internal\nimplementation detail of terraform, not per se a stable public interface\nacross versions.\n\n## Options\n\nYou can provide the path to the terraform binary else its auto discovered\n```shell\n--tf-binary=$HOME/bin/terraform\n```\n\nTo avoid repeated downloading of plugins a plugin cache dir is utilized\nby default this is `.tfcache` in the current working directory.\n```shell\n--tf-plugin-dir=$HOME/.cache/tfcache\n```\n\nTerraform modules referenced by fixtures are looked up in a few different\nlocations, directly in the same directory as the test module, in a subdir\nnamed terraform, and in a sibling directory named terraform. An explicit\ndirectory can be given which will be looked at first for all modules.\n\n```shell\n--tf-mod-dir=terraform\n```\n\nThis plugin also supports flight recording (see next section)\n```shell\n--tf-replay=[record|replay|disable]\n```\n\n## Flight Recording\n\nThe usage/philosophy of this plugin is based on using flight recording\nfor unit tests against cloud infrastructure. In flight recording rather\nthan mocking or stubbing infrastructure, actual resources are created\nand interacted with with responses recorded, with those responses\nsubsequently replayed for fast test execution. Beyond the fidelity\noffered, this also enables these tests to be executed/re-recorded against\nlive infrastructure for additional functional/release testing.\n\n### Replay Support\n\nBy default fixtures will save a `tf_resources.json` back to the module\ndirectory, that will be used when in replay mode.\n\n### Recording\n\nTODO ~\n\n## XDist Compatibility\n\npytest_terraform supports pytest-xdist in multi-process (not distributed)\nmode.\n\nWhen run with python-xdist, pytest_terraform treats all non functional\nscopes as per test run fixtures across all workers, honoring their\noriginal scope lifecycle but with global semantics, instead of once\nper worker (xdist default).\n\nTo enable this the plugin does multi-process coodination using lock\nfiles, a test execution log, and a dependency mapping of fixtures\nto tests. Any worker can execute a module teardown when its done executing\nthe last test that depends on a given fixture. All provisioning and\nteardown are guarded by atomic file locks in the pytest execution\'s temp\ndirectory.\n\n### Root module references\n\n`terraform_remote_state` can be used to introduce a dependency between\na scoped root modules on an individual test, note we are not\nattempting to support same scope inter fixture dependencies as that\nimposes additional scheduling constraints outside of pytest native\ncapabilities. The higher scoped root module (ie session or module scoped)\nwill need to have output variables to enable this consumption.\n',
    'author': 'Kapil Thangavelu',
    'author_email': 'kapilt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cloud-custodian/pytest-terraform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
