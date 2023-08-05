# August - a html-to-text converter

August is an html to text converter specifically intended for producing
text versions of HTML emails. The main code is all written in Rust,
this packages is includes python bindings.


## Getting Started

Install using PIP

```shell
$ pip3 install august
```

Then, import it and run convert

```python
import august

html = '<p>I\'m <em>so</em> excited to try this</p>'
print(august.convert(html, width=20))
```

which prints

```text
I'm /so/ excited to
try this
```


## Alternatives

* [html2text](https://pypi.org/project/html2text/):
  Coverts HTML into markdown, and supports a bazillion options.
  It's a great project if you want to produce markdown; but markdown, because
  it's designed to be turned into HTML, has a little more noise than is
  strictly necessary, and the header formatting is pretty unclear.
* [html-to-text](https://www.npmjs.com/package/html-to-text):
  Converts HTML to text. Javascript/node project.
