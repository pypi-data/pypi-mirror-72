# Flask Autoversion

Automatically version static file paths. When actively developing a web 
application, you may experience issues with browsers caching your static 
content. With this extension you can easily use the function in your 
templates that will update the query added on to the file path to bust 
the browser cache.

# Installation

Install the extension:

`pip install Flask-Autoversion`


# Set Up

A typical setup:

```python
from flask import Flask, render_template
from flaskext.autoversion import Autoversion

app = Flask(__name__)
app.autoversion = True
Autoversion(app)

@app.route('/')
def hello_world():
    return render_template("home.html")
```

Setting app.autoversion to True will append a query string with the file 
last-modified timestamp as the value.

# Versioning Static Files in Jinja

```html
<link rel="stylesheet" type="text/css" href="{{ static_autoversion('app.css') }}">
```