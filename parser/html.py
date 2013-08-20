# -*- coding: utf-8 -*-
import re

class Html:
    def __init__(self):
        self.plain_regex = re.compile(r'^\s+|\s*<[^<]+>', re.I|re.M)

    def to_plain(self, html):
        """ HTMLをプレインテキストに変換する
        """
        plain_strings = [self.plain_regex.sub('', s) for s in html.split("\n")]
        return "".join([s + "\n" for s in plain_strings if s])

    def get_attrs(self, html, tag, attr_name):
        """ {html}中の{tag}から{attr_name}を抽出する
        """
        return [m.group(1) for m in
                re.finditer('%s(?:\s*)%s(?:\s*)=(?:\s*)"([^"]+)"' % (tag, attr_name), html)]


class _TestTarget:
    def pytest_funcarg__target(request):
        return Html()


class Test_to_plain(_TestTarget):
    def test_empty(self, target):
        assert target.to_plain('') == ''

    def test_plain(self, target):
        html = """\
<html>
  <body>
    <p>This is p</p>
    <div id="yeah"><span class="hogehoge">This is span</span></div>
    body text
  </body>
</html>
"""

        plain = """\
This is p
This is span
body text
"""
        assert target.to_plain(html) == plain


class Test_get_attrs(_TestTarget):
    def test_empty(self, target):
        assert target.get_attrs('', 'a', 'href') == []

    def test_has_not_attrs(self, target):
        assert target.get_attrs('<a>hoge</a>', 'a', 'href') == []

    def test_has_attrs(self, target):
        html = """\
<div class="booo">
  <a class="foo">text</a>
  <a class ="bar">text</a>
  <a  class=  "baz">text</a>
  <div class="outer"><div class="inner">aaa</div></div>
</div>
"""
        assert target.get_attrs(html, 'a', 'class') == ['foo', 'bar', 'baz']
        assert target.get_attrs(html, 'div', 'class') == ['booo', 'outer', 'inner']
