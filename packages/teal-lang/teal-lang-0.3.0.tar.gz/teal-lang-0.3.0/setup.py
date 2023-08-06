# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teal_lang',
 'teal_lang.cli',
 'teal_lang.cloud',
 'teal_lang.controllers',
 'teal_lang.examples',
 'teal_lang.executors',
 'teal_lang.machine',
 'teal_lang.run',
 'teal_lang.teal_compiler',
 'teal_lang.teal_parser']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=14.0,<15.0',
 'colorful>=0.5.4,<0.6.0',
 'deterministic_zip>=0.1,<0.2',
 'docopt',
 'graphviz>=0.13.2,<0.14.0',
 'parsy>=1.3.0,<2.0.0',
 'pydot>=1.4.1,<2.0.0',
 'pynamodb',
 'pyyaml>=5.3.1,<6.0.0',
 'schema>=0.7.2,<0.8.0',
 'sly>=0.4,<0.5',
 'toml>=0.10.1,<0.11.0',
 'yaspin>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['teal = teal_lang.cli.main:main']}

setup_kwargs = {
    'name': 'teal-lang',
    'version': '0.3.0',
    'description': 'The Teal Programming Language',
    'long_description': '# The Teal Programming Language\n\n![Tests](https://github.com/condense9/teal-lang/workflows/Build/badge.svg?branch=master) [![PyPI](https://badge.fury.io/py/teal-lang.svg)](https://pypi.org/project/teal-lang) [![Gitter](https://badges.gitter.im/Teal-Lang/community.svg)](https://gitter.im/Teal-Lang/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n\nTeal is designed for passing data between Python functions running in the cloud\nwith very little infrastructure. It\'s like having a cluster, without having to\nmanage a cluster.\n\n```javascript\n// service.tl\nimport(read_items,     :python src.data_lib)\nimport(transform_item, :python src.data_lib)\nimport(get_metadata,   :python src.data_lib)\nimport(save_item,      :python src.data_lib)\nimport(aggregate,      :python src.data_lib)\n\nfn handle(item) {\n  // Get the metadata and do the transform in parallel\n  metadata = async get_metadata(item)\n  transformed = async transform_item(item)\n  save_item(await metadata, await transformed)\n}\n\nfn main(items_csv) {\n  items = read_items(items_csv)\n  results = map(items, async handle)\n  aggregate(map(results, await)) // wait for all handling to finish\n  "done"\n}\n```\n\nRun it locally:\n\n```\n$ teal service.tl test_items.csv\n```\n\nAnd deploy it to the cloud:\n\n```shell\n$ teal deploy\nTeal: {"version": "0.2.1"}\nDone (52s elapsed).\n\n$ aws s3 cp test_items.csv s3://your-bucket teal\n...\n\n$ invoke -f main test_items.csv\n```\n\n---\n\n## Introduction\n\nTeal threads run in parallel on separate compute resource, and Teal handles data\ntransfer and synchronisation.\n\n**Data in**: You can invoke Teal like any Lambda function (AWS cli, S3 trigger,\nAPI gateway, etc).\n\n**Data out**: Use the Python libraries you already have for database access.\nTeal just connects them together.\n\n**Testing**: There is a local runtime too, so you can thoroughly test Teal\nprograms before deployment (using minio and localstack for any additional\ninfrastructure that your code uses).\n\n| Teal is like...                     | But...                                                                                                   |\n|-------------------------------------|----------------------------------------------------------------------------------------------------------|\n| AWS Step Functions                  | Teal programs can be tested locally, and aren\'t bound to AWS.                                            |\n| Orchestrators (Apache Airflow, etc) | You don\'t have to manage infrastructure, or think in terms of DAGs, and you can test everything locally. |\n| Task runners (Celery, etc)          | You don\'t have to manage infrastructure.                                                                 |\n| Azure Durable Functions             | While powerful, Durable Functions (subjectively) feel complex - their behaviour isn\'t always obvious.    |\n\n[Read more...](#why-teal)\n\nTeal functions are like coroutines - they can be paused and resumed at any\npoint. Each horizontal bar in this plot is a separate Lambda invocation. Try\nimplementing that in Python. [Read more...](#faq)\n\n![Concurrency](doc/functions.png)\n\n\n## Getting started\n\n```shell\n$ pip install teal-lang\n```\n\nThis gives you the `teal` executable - try `teal -h`.\n\nDocumentation is coming soon! For now, check out the [the Fractal\nexample](examples/fractals) or the\n[Playground](https://www.teal-lang.org/playground).\n\n[Create an issue](https://github.com/condense9/teal-lang/issues) if none of this\nmakes sense, or you\'d like help getting started.\n\n\n### Teal May Not Be For You!\n\nTeal *is* for you if:\n- you use Python for long-running tasks.\n- you have an AWS account.\n- you have a repository of data processing scripts, and want to run them\n  together in the cloud.\n- You don\'t have time (or inclination) to deploy and manage a full-blown task\n  platform (Airflow, Celery, etc).\n- You don\'t want to use AWS Step Functions .\n\nCore principles guiding Teal design:\n- Do the heavy-lifting in Python.\n- Keep business logic out of infrastructure (no more hard-to-test logic defined\n  in IaC, please).\n- Workflows must be fully tested locally before deployment.\n\n\n## Why Teal?\n\nTeal is like AWS Step Functions, but is cheaper (pay only for the Lambda\ninvocations and process data), and way easier to program and test. The tradeoff\nis you don\'t get tight integration with the AWS ecosystem (e.g. Teal doesn\'t\nnatively support timed triggers).\n\nTeal is like Azure Durable Functions -- it lets you pause and resume workflows,\nbut it\'s (subjectively) nicer to write. The syntax feels natural. Also it\'s not\nbound to Azure.\n\nTeal is like a task runner (Celery, Apache Airflow, etc), but you don\'t have to\nmanage any infrastructure.\n\nTeal is **not** Kubernetes, because it\'s not trying to let you easily scale\nDockerised services.\n\nTeal is **not** a general-purpose programming language, because that would be\nneedlessly reinventing the wheel.\n\nTeal is a simple compiled language with only a few constructs:\n\n1. named variables\n2. `async` & `await` concurrency primitives \n3. Python (>=3.8) interoperability (FFI)\n4. A few basic types (strings, numbers, lists)\n5. first-class functions (proper closures coming soon)\n\nTwo interpreters have been implemented so far -- local and AWS Lambda, but\nthere\'s no reason Teal couldn\'t run on top of (for example) Kubernetes. [Issue\n#8](https://github.com/condense9/teal-lang/issues/8)\n\n**Concurrency**: When you do `y = async f(x)`, `f(x)` is started on a new Lambda\ninstance. And then when you do `await y`, the current Lambda function\nterminates, and automatically continues when `y` is finished being computed.\n\nThe compiler is basic at the moment, but does feature tail-call optimisation for\nrecursive functions. Compile-time correctness checks (e.g. bound names, types,\netc) are coming soon.\n\n\n## FAQ\n\n**Why is this not a library/DSL in Python?**\n\nWhen Teal threads wait on a Future, they stop completely. The Lambda function\nsaves the machine state and then terminates. When the Future resolves, the\nresolving thread restarts any waiting threads by invoking new Lambdas to pick up\nexecution.\n\nTo achieve the same thing in Python, the framework would need to dump the entire\nPython VM state to disk, and then reload it at a later point -- I don\'t know\nPython internals well enough to do this, and it felt like a huge task.\n\n**How is Teal like Go?**\n\nGoroutines are very lightweight, while Teal `async` functions are pretty heavy --\nthey involve creating a new Lambda (or process, when running locally).\n\nTeal\'s concurrency model is similar to Go\'s, but channels are not fully\nimplemented so data can only be sent to/from a thread at call/return points.\n\n**Is this an infrastructure-as-code tool?**\n\nNo, Teal does not do general-purpose infrastructure management. There are\nalready great tools to do that ([Terraform](https://www.terraform.io/),\n[Pulumi](https://www.pulumi.com/), [Serverless\nFramework](https://www.serverless.com/), etc).\n\nInstead, Teal reduces the amount of infrastructure you need. Instead of a\ndistinct Lambda function for every piece of application logic, you only need the\ncore Teal interpreter (purely serverless) infrastructure.\n\nTeal will happily manage that infrastructure for you (through `teal deploy` and\n`teal destroy`), or you can set it up with your in-house custom system.\n\n\n## Current Limitations and Roadmap\n\nTeal is alpha quality, which means that it\'s not thoroughly tested, and lots of\nbreaking changes are planned. This is a non-exhaustive list.\n\n### Libraries\n\nOnly one Teal program file is supported, but a module/package system is\n[planned](https://github.com/condense9/teal-lang/issues/9).\n\n### Error Handling\n\nThere\'s no error handling - if your function fails, you\'ll have to restart the\nwhole process manually. An exception handling system is\n[planned](https://github.com/condense9/teal-lang/issues/1).\n\n### Typing\n\nFunction inputs and outputs aren\'t typed. This is a limitation, and will be\nfixed soon, probably using\n[ProtoBufs](https://developers.google.com/protocol-buffers/) as the interface\ndefinition language.\n\n### Calling Arbitrary Services\n\nCurrently you can only call Teal or Python functions -- arbitrary microservices\ncan\'t be called. Before Teal v1.0 is released, this will be possible. You will\nbe able to call a long-running third party service (e.g. an AWS ML service) as a\nnormal Teal function and `await` on the result.\n\n### Dictionary (associative map) primitives\n\nTeal really should be able to natively manipulate JSON objects. This may happen\nbefore v1.0.\n\n---\n\n\n## Contributing\n\nContributions of any form are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)\n\nMinimum requirements to develop:\n- Docker (to run local DynamoDB instance)\n- Poetry (deps)\n\nUse `scripts/run_dynamodb_local.sh` to start the database and web UI. Export the\nenvironment variables it gives you - these are required by the Teal runtime.\n\n\n## About\n\nTeal is maintained by [Condense9 Ltd.](https://www.condense9.com/). Get in touch\nwith [ric@condense9.com](ric@condense9.com) for bespoke data engineering and\nother cloud software services.\n\nTeal started because we couldn\'t find any data engineering tools that were\nproductive and *felt* like software engineering. As an industry, we\'ve spent\ndecades growing a wealth of computer science knowledge, but building data\npipelines in $IaC, or manually crafting workflow DAGs with $AutomationTool,\n*just isn\'t software*.\n\n\n## License\n\nApache License (Version 2.0). See [LICENSE](LICENSE) for details.\n',
    'author': 'Ric da Silva',
    'author_email': 'ric@condense9.com',
    'maintainer': 'Ric da Silva',
    'maintainer_email': 'ric@condense9.com',
    'url': 'https://www.condense9.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
