<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()
[![](https://img.shields.io/badge/language-Python-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/v/readme42.svg?maxAge=3600)](https://pypi.org/project/readme42/)
[![](https://img.shields.io/npm/v/readme42.svg?maxAge=3600)](https://www.npmjs.com/package/readme42)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/readme42.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/readme42.py/)

#### Installation
```bash
$ [sudo] npm i -g readme42
```
```bash
$ [sudo] pip install readme42
```

#### Scripts usage
command|`usage`
-|-
`readme42` |`usage: readme42 path`

#### Examples
https://readme42.com/templates/username/template
```html
{% if examples %}
### Examples
{{ examples }}
{% endif %}

{% if links %}
### Links
{{ links }}
{% endif %}
```

cli
```bash
$ export README42_TOKEN="XXX" # https://readme42.com/token/
$ export README42_TEMPLATE="username/template"
$ readme42 . > README42.md
```

python api:
```python
url = 'https://api.readme42.com/templates'
headers = {'Authorization': 'Token README42_TOKEN'}

data = dict(
    examples=open('examples.md').read(),
    links=open('links.md').read()
)
r = requests.post(url,headers=headers,data=data)

open('README.md','w').write(r.text)
```

#### Links
+   [readme42.com](https://readme42.com/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>