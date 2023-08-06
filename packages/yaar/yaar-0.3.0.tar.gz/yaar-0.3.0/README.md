Yet Another Asyncio Requests

Install and usage are as expected. To install:

```sh
$ pip install yaar
```

And then the usage:

```python
import yaar

response = await yaar.get(url)
print(response.status, response.text)
print(response.json())


# send a json in the request body
response = await yaar.post(url, json={"some": "json"})
print(response.status)
```

To send headers in your request use:

```python
response = await yaar.get(url, headers={'Authentication': 'bearer} XYZ')
```

Here you have all usual the methods like ``put``, ``delete``, etc..

In case you need a custom session you can use:

```python
session = aiohttp.ClientSession(loop=loop)
response = await yaar.get(url, session=session)
```
