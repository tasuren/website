# tasuren's website main program

from typing import List

from aiofiles.os import wrap
from os.path import exists
from ujson import load

from sanic.response import HTTPResponse, file as rfile, html
from sanic.request import Request
from sanic import Sanic

from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask_misaka import Misaka


app = Sanic("RT-WebSite")
with open("data.json", "r", encoding="utf-8_sig") as f:
    app.ctx.data = data = load(f)
exists = wrap(exists)


# Jinja2 テンプレートエンジンの設定をする。
env = Environment(
    loader=FileSystemLoader("./" + data["jinja2"]["folder"]),
    autoescape=select_autoescape(data["jinja2"]["exts"]),
    enable_async=True
)
env.filters.setdefault("markdown", Misaka(autolink=True, wrap=True).render)


# Jinja2テンプレートエンジンを使用してHTMLを返すためのコルーチン関数。
async def template(tpl: str, **kwargs) -> HTTPResponse:
    return html(
        (await env.get_template(tpl).render_async(kwargs))
            .replace("<code>", "<pre><code>")
            .replace("</code>", "</code></pre>")
    )


def get_metas(path: str, paths: List[str]) -> dict:
    d = data["metas"]
    for key in (paths := path.split("/")):
        d = d.get(key, {})
    if "title" not in d:
        d["title"] = paths[-1] if paths else "Untitled"
    d["src"] = f"{paths[-1][paths[-1].rfind('.'):] if paths else 'index.'}j2"
    return d


# MAIN
@app.middleware("request")
async def on_request(request: Request):
    print(request.path)
    # Pathの調整をする。
    path = request.path
    if path.endswith("/"):
        path = path[:-1]
    if (paths := path.split()) and "." not in paths[-1]:
        path = path = f"{path}/index.html"
    # ファイルを返す。
    real_path = f"{data['jinja2']['folder']}/{path}"
    if "." in request.path and path.endswith(data["jinja2"]["exts"]):
        if await exists(real_path):
            return await template(request.path)
        elif await exists(f"{data['jinja2']['folder']}/{path[path.rfind('.'):]}j2"):
            return await template(
                f"{data['jinja2']['folder']}/{data['jinja2']['base']}",
                **get_metas(path, paths)
            )
    else:
        return await rfile(real_path)


app.run(**data["app"])
