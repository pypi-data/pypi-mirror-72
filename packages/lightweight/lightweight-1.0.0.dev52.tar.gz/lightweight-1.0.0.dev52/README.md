# lightweight: a static site generator 
[![PyPI](https://img.shields.io/pypi/v/lightweight)][pypi]
[![Build Status](https://img.shields.io/azure-devops/build/misha-drachuk/lightweight/8)](https://dev.azure.com/misha-drachuk/lightweight/_build/latest?definitionId=8&branchName=master)
[![Test Coverage](https://img.shields.io/coveralls/github/mdrachuk/lightweight/master)](https://coveralls.io/github/mdrachuk/lightweight)
[![Supported Python](https://img.shields.io/pypi/pyversions/lightweight)][pypi]

Code over configuration.

[Documentation][docs]

[Examples](https://github.com/mdrachuk/lightweight-examples)



## Features
- [x] Jinja2 templates
- [x] Markdown rendering with YAML frontmatter
- [x] Sass/SCSS rendering
- [x] Dev server
- [x] Template project
- [x] Clean extensible API 
- [x] Fast Enough
- [x] Fails Fast

## Installation
Available from [PyPI][pypi]:
```shell
pip install lightweight
```

## Quick Example
```python
from lightweight import Site, SiteCli, markdown, paths, jinja, template, sass


def blog_posts(source):
    post_template = template('_templates_/blog/post.html')
    # Use globs to select files. # source = 'posts/**.md'
    return (markdown(path, post_template) for path in paths(source))

def example(url):
    site = Site(url)
    
    # Render an index page from Jinja2 template.
    site.add('index.html', jinja('index.html'))
    
    # Render markdown blog posts.
    [site.add(f'blog/{post.source_path.stem}.html', post) for post in blog_posts('posts/**.md')]
    site.add('blog.html', jinja('posts.html'))
    
    # Render SASS to CSS.
    site.add('css/global.css', sass('styles/main.scss'))
    
    # Include a copy of a directory.
    site.add('img')
    site.add('fonts')
    site.add('js')
    
    return site   

def generate_prod():
    example(url='https://example.org/').generate(out='out')


if __name__ == '__main__':
    # Run CLI with `build` and `serve` commands. 
    SiteCli(build=example).run()

```

## Create a new project

Initialize a new project using `init` command:
```bash
lw init --url https://example.org example
```

It accepts multiple optional arguments:
```
lw init -h
usage: lw init [-h] [--title TITLE] location

Generate Lightweight skeleton application

positional arguments:
  location       the directory to initialize site generator in

optional arguments:
  -h, --help     show this help message and exit
  --title TITLE  the title of of the generated site
```

## Dev Server

Lightweight includes a simple static web server with live reload serving at `localhost:8080`:
```bash
python -m website serve
```
Here `website` is a Python module 

Host and port can be changed via:
```bash
python -m website serve --host 0.0.0.0 --port 80
```

The live reload can be disabled with `--no-live-reload` flag:
```bash
python -m website serve --no-live-reload
```
Otherwise every served HTML file will be injected with a javascript that polls `/__live_reload_id__`.
The script triggers page reload when the value at that location changes.
The `/__live_reload_id__` is changed after regenerating the site upon change in `--source` directory.

To stop the server press `Ctrl+C` in terminal.


[pypi]: https://pypi.org/project/lightweight/
[docs]: https://lightweight.readthedocs.io/en/latest/ 
