"""
Usage:
1. put this file to the directory that you want to use in `path_deploy()`
2. change the app name if needed
3. run this file.
"""
import os
from os import path

from tornado import template

from pywebio.output import *
from pywebio.platform.path_deploy import filename_ok
from pywebio.session import *

#Change the name of the multipage app
app_name = 'A multipage app'


BASE_DIR = path.dirname(path.abspath(__file__))

TPL = """
<style>
    body {
        padding: 0 200px;
    }
    .sidebar {
        padding-left: 20px;
        position: fixed;
        left: 0;
        width: 250px;
        top: 0;
        bottom: 0;
        background-color: #f2f2f2;
        z-index: 999;
        padding-bottom: 60px;
    }
    iframe {
        display: none;
        position: fixed;
        width: calc(100% - 200px);
        height: 100%;
        left: 200px;
        top: 0;
        right: 0;
        bottom: 0;
        z-index: 10;
    }
    .sidebar > .tree{
        height: 100%;
        overflow-y: auto;
    }
</style>
<div class="sidebar">
    <h3>Navigator</h3>
    <div class="tree">
        <ul>
            {% for name, url in apps %}
            <li><a href="javascript:iframe_open('{{url}}')">{{name}}</a></li>
            {% end %}
            {% for name, url in dirs %}
            <li><a href="javascript:dir_open('{{url}}')">{{name}}\</a></li>
            {% end %}
        </ul>
    </div>
</div>
<iframe src="#" frameborder="0"></iframe>
<script>
    $('.footer').remove();
    function iframe_open(url) {
        $('iframe').show().attr('src', url);
        $('.alert-info').hide();
    }
    function dir_open(url) {
        window.location.hash = '#' + url;
        window.location.reload();
    }
</script>
"""


def main():
    target_path = eval_js("window.location.hash")[1:].lstrip('/') or ''
    if '.' in target_path:
        target_path = ''

    p = path.join(BASE_DIR, target_path)

    apps = []
    dirs = []

    try:
        files = os.listdir(p)
    except Exception:
        put_error("URL error")
        return

    for f in files:
        if not filename_ok(f):
            continue
        full_path = path.join(p, f)

        if os.path.isfile(full_path):
            if 'main()' not in open(full_path).read():
                continue
            if f.endswith('.py') and f != 'index.py':
                apps.append((f[:-3], path.join(target_path, f[:-3])))
        else:
            dirs.append((f, path.join(target_path, f)))

    if target_path:
        dirs.append(['..', path.dirname(target_path)])

    tpl = template.Template(TPL)

    html = tpl.generate(apps=apps, dirs=dirs).decode('utf8')
    put_html(html)
    put_info("%s" %app_name)


if __name__ == '__main__':
    from pywebio.platform.path_deploy import path_deploy
    path_deploy(BASE_DIR, port=8089, debug=True, cdn=False)