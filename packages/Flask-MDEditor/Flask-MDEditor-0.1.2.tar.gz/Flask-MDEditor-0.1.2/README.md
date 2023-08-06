# Flask-mdeditor
[![ENV](https://img.shields.io/badge/release-v0.1-blue.svg)](https://github.com/pylixm/django-mdeditor)
[![ENV](https://img.shields.io/badge/pypi-v0.1-blue.svg)](https://pypi.org/project/Flask-MDEditor/)
[![ENV](https://img.shields.io/badge/中文-v0.1-blue.svg)](./README_CN.md)
[![ENV](https://img.shields.io/badge/python-3.7x-green.svg)]()
[![ENV](https://img.shields.io/badge/flask-1.0+-green.svg)]()
[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

![](./flask_and_mdeditor.png)

**Flask-mdeditor** is Markdown Editor plugin application for [flask]() base on [Editor.md](https://github.com/pandao/editor.md).

**Flask-mdeditor** was inspired by great [django-mdeditor](https://github.com/pylixm/django-mdeditor), [flask-ckeditor](https://github.com/greyli/flask-ckeditor)

**Note:**
    
* For Markdown page rendering issues, backend rendering is recommended. you can use markdon render plugin such like [mistune](https://github.com/lepture/mistune) 

## Features
------------------------------
* Alomost Editor.md features
    * Support Standrad Markdown / CommonMark and GFM(GitHub Flavored Markdown); 
    * Full-featured: Real-time Preview, Image upload, Preformatted text/Code blocks/Tables insert, search replace, Themes, Multi-languages;
    * The MDEditorField is provided for the FlaskForm;


## Quick Start
------------------------------
### Installation
> `pip install flask-mdeditor`
### Initialization
This extension needs to be initialized in the usual way before it can be used, in order to be able to **save upload image** correctly, `MDEDITOR_FILE_UPLOADER` needed to be frist config, such like:
```python
from flask_mdeditor import MDEditor
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['MDEDITOR_FILE_UPLOADER'] = os.path.join(basedir, 'uploads') # this floder uesd to save your uploaded image
mdeditor = MDEditor(app)
```
### Working with Flask-WTF/WTForms
when using Flask-WTF/WTForms, you can import MDEditorField provided by FLASK-MDEDITOR and use it just like StringField:
```python
from flask_mdeditor import  MDEditorField
class PostForm(FlaskForm):
    content = MDEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

```
then you can use it in your template
```html
<form action="/xxx" method="POST">
        {{ form.csrf_token }}
        {{ form.content.label }} {{ form.content() }}
        {{ form.submit() }}
</form>
```
or , if you don't use the wtf, you can use the global jinja2 func `{{ mdeditor.load() }}` to load the editor, such as:
```html
<form action="/" method="POST">
    {{ mdeditor.load() }}
    <button type="submit">submit</button>
</form>
```

### Get the Data
* use the wtf
```python
@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        body = form.content.data
        ...
```
* else
Since the MDEditor textarea is just a normal `<textarea>` element, you can get the data from request.form by passing **mdeditor** as key:
```python
@app.route('/save', methods=['POST'])
def new_post():
    if request.method == 'POST':
        data = request.form.get('mdeditor')
    ...
```
------------------
## Tip
check the demo application at demo/flask_test

## Available Configuration
The more configuration options available are listed below:
|Name|Default Value| Info | Required | Option
|-|-|-|-|-|
|MDEDITOR_FILE_UPLOADER| path | the floder path used to save uploaded img  | √ | 
|MDEDITOR_HEIGHT|500px|Browser rendering editor height|×|
|MDEDITOR_WIDTH|100%|Browser rendering editor width|×|
|MDEDITOR_THEME|default|editor main theme|×|dark / default|
|MDEDITOR_PREVIEW_THEME|default|preview area theme|×| default / dark
|MDEDITOR_EDITOR_THEME|default|edit area theme|×| pastel-on-dark / default
|MDEDITOR_LANGUAGE|zh|editor language|×|zh / en

## TODO
* Unit Testing
* code optimization
* More Features
## License
The MIT License.

Copyright (c) 2020 Zisc