# Sanic Skywalking

This package help you integrate Skywalking APM in Sanic applications easily through Skywalking Python Agent. 

If you'd like to explore more about Apache Skywalking and Python agent, you can visit 

[Apache Skywalking Github](https://github.com/apache/skywalking/)

[Apache Skywalking Python Agent](https://github.com/apache/skywalking-python)

## Installation

Run the following command:

```shell
$ pip install sanic-skywalking-middleware
```

### Usage
Simple initilize a SanicSkywalingMiddleware with a Sanic instance and Skywalking collector address. 

```python
from sanic_skywalking_middleware import SanicSkywalingMiddleware

SanicSkywalingMiddleware(app, service='Sanic Skywalking Demo Service', collector='127.0.0.1:11800')
```

## Examples

See [Examples](example.py) to view and run an example of Sanic applications with Skywalking integrated.
