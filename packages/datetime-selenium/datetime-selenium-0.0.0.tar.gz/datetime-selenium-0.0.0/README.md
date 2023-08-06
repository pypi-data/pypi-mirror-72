Datetime-Selenium allows you to send/retrieve `datetime.datetime` objects to/from web forms using [Selenium](https://selenium-python.readthedocs.io/).

## Installation

```
$ pip install datetime-selenium
```

## Quickstart

First, clone an example file from the Datetime-Selenium repo.

```bash
$ curl https://raw.githubusercontent.com/dsbowen/datetime-selenium/master/form.html --output form.html
```

Let's send the current date and time to all input in the form.

```python
from datetime_selenium import send_datetime

from selenium.webdriver import Chrome

from datetime import datetime

driver = Chrome()
driver.get('data:text/html,'+open('form.html').read())

datetime_ = datetime.utcnow()

css_selectors = (
    'input[type=date]',
    'input[type=datetime-local]',
    'input[type=month]',
    'input[type=time]',
    'input[type=week]'
)
for selector in css_selectors:
    input_ = driver.find_element_by_css_selector(selector)
    send_datetime(input_, datetime_)
```

You'll see the form filled in in your selenium browser.

## Citation

```
@software{bowen2020datetime-selenium,
  author = {Dillon Bowen},
  title = {Datetime-Selenium},
  url = {https://dsbowen.github.io/datetime-selenium/},
  date = {2020-06-29},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/datetime-selenium/blob/master/LICENSE).