# Description

Gobits is a very small module, which acts as a metadata carrier for pub/sub messages. It automatically adds fields that may be useful downstream to determine the origin of a pub/sub message.

# Usage

Cloud function with http trigger:

```python
from gobits import Gobits


def handler(request):

    bits = Gobits(request=request)

    message = {
      'gobits': bits,
      'data': 'message-to-send'
    }

```

Cloud function with storage trigger:

```python
from gobits import Gobits


def handler(data, context):

    bits = Gobits(context=context)

    message = {
      'gobits': bits,
      'data': 'message-to-send'
    }

```
