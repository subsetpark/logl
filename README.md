logl (לאָגל)
======

Logl is a framework modelled on the well-known framework for Python, [Flask][]. It is a WSGI application that implements much of what you'd expect from a simple framework:

- routes
- db access
- html templating
- GET and POST parsing

[flask]: flask.pocoo.org

## Usage

To build a web application with logl, simply start a new project and import the logl module. Logl has a structure very similar to Flask. At the top of your application you should instantiate a new application object:

```python
from logl import Logl, Response

app = Logl()
```

This application will be your main point of interaction for your web app. Then proceed to define functions for the endpoints of your app, using a decorator to denote the url.

```python
@app.add_route('/')
def index():
    """
    Display the requested path.
    """
    app.add_replace('query', app.request.query)
    response = app.response(template="index.html")
    return response
```

In the above example, we are also passing a variable to the application's "context", which is where it stores data for the templating engine to access.

```
{{extends base.html}}
{{block name}}
If page
{{endblock}}
{{block content}}
<h2>This page demonstrates conditionals.</h2>
<form method="post" action="/if">
    <p>
        <input type="checkbox" name="ifs" value="first">
        <input type="checkbox" name="ifs" value="second">
        <input type="submit" value="Submit">
    </p>
</form>
<p>
{{if first}}
This is a basic if.
{{endif}}
{{if second}}
This is an if with an else.
{{else}}
This is an else.
{{endif}}
{{endblock}}
```

Logl's templating engine supports basic jinja-style features including conditionals, block extension, and variable substitution.

 