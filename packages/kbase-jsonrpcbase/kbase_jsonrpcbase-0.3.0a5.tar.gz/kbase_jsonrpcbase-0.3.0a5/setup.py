# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpcbase']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'kbase-jsonrpcbase',
    'version': '0.3.0a5',
    'description': 'Simple JSON-RPC service without transport layer',
    'long_description': '# JSONRPCBase\n\n> NOTE: This is a fork of [level12/jsonrpcbase](https://github.com/level12/jsonrpcbase/) with changes maintained by KBase\n\nSimple JSON-RPC service without transport layer\n\nThis library is intended as an auxiliary library for easy an implementation of JSON-RPC services with Unix/TCP socket\nlike transport protocols that do not have complex special requirements. You need to utilize some suitable transport\nprotocol with this library to actually provide a working JSON-RPC service.\n\n## Features\n\n- Easy to use, small size, well tested.\n- Supports JSON-RPC v2.0. Compatible with v1.x style calls with the exception of v1.0 class-hinting.\n- Optional argument type validation that significantly eases development of jsonrpc method_data.\n\n## Example\n\nExample usage:\n\n```py\nimport jsonrpcbase\n\nchat_service = jsonrpcbase.JSONRPCService()\n\ndef login(username, password, timelimit=0):\n    # (...)\n    return True\n\ndef receive_message(**kwargs):\n    # (...)\n    return chat_message\n\ndef send_message(msg):\n    # (...)\n    pass\n\nif __name__ == \'__main__\':\n\n    # Adds the method login to the service as a \'login\'.\n    chat_service.add(login, types=[basestring, basestring, int])\n\n    # Adds the method receive_message to the service as a \'recv_msg\'.\n    chat_service.add(receive_message, name=\'recv_msg\', types={"msg": basestring, "id": int})\n\n    # Adds the method send_message as a \'send_msg\' to the service.\n    chat_service.add(send_message, \'send_msg\')\n\n    # Receive a JSON-RPC call.\n    jsonmsg = my_socket.recv()\n\n    # Process the JSON-RPC call.\n    result = chat_service.call(jsonmsg)\n\n    # Send back results.\n    my_socket.send(result)\n```\n\n## Development\n\nInstall [poetry](https://python-poetry.org/) and run `poetry install`.\n\nRun tests with `make test`.\n\nDeploy with `poetry build` and `poetry publish`.\n\n## Credits\n\nThis project was originally developed by Juhani Åhman.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kbaseIncubator/jsonrpcbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
