# selenium-fetch

A simple module that lets you access the `fetch` API with selenium!

> _Why do I make this? just annoyed with cloudflare. It works best with [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)._

## Installation

```
pip install selenium-fetch undetected-chromedriver
```

## Example

```python
from undetected_chromedriver import Chrome
from selenium_fetch import fetch, Options, get_browser_user_agent

LOGIN_PAGE_URL = "https://smekdong.com/login"
LOGIN_API_URL = "https://smekdong.com/api/login"
driver = Chrome(headless=False)
driver.get(LOGIN_PAGE_URL)
post_data = {
    'username': 'blaabla',
    'password': 'xxxx'
}
headers = {
    "user-agent": get_browser_user_agent(driver),
    'origin': 'https://smekdong.com',
    'referer': 'https://smekdong.com/',
}
options = Options(method="POST", headers=headers, body=post_data)
response = fetch(driver, LOGIN_API_URL, options)
print("Response:", response)
```
