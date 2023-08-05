<img src="https://www.zoomconnect.com/assets/logo.png">

# ZoomConnect Python SDK 

This Python package provides a wrapper for the [ZoomConnect API](https://www.zoomconnect.com/api).

### Installation

```
pip install zoomconnect-sdk
```

### Authentication

Please visit the [signup](https://www.zoomconnect.com/app/account/signup) page
to create an account and generate an API key.

### Example usage

```python
from zoomconnect_sdk.client import Client

c = Client(api_token='xxx-xxx-xxx-xxx', account_email='xxxx@xxx.co.za')
try:
    res = c.send_sms("0000000000", "Welcome to ZoomConnect")
except Exception as e:
    print(e)
else:
    print(res)
```

### Requirements
Python 3.6+

### License

[MIT](https://github.com/Lambrie/zoomconnect_sdk/blob/master/LICENSE)
