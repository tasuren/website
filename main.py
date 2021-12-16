# tasuren's website main program

from typing import List

from urllib.parse import unquote
from aiofiles.os import wrap
from os.path import exists
from ujson import load

from sanic.response import HTTPResponse, file as rfile, html, text
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
env.filters.setdefault(
    "markdown", Misaka(autolink=True, fenced_code=True, wrap=True).render
)


# Jinja2テンプレートエンジンを使用してHTMLを返すためのコルーチン関数。
async def template(tpl: str, **kwargs) -> HTTPResponse:
    return html(
        (await env.get_template(tpl).render_async(kwargs))
    )


def get_metas(path: str, paths: List[str]) -> dict:
    d = data["metas"]
    for key in (paths := path.split("/")):
        if key:
            if not (d := d.get(key, {})):
                break
    if "title" not in d:
        d["title"] = paths[-1] if paths else "Untitled"
    before = ('/'.join(paths[:-1]) + "/") if paths[:-1] else ""
    d["src"] = f"{before}{paths[-1][:paths[-1].rfind('.')+1] if paths else 'index.'}j2"
    return d


# MAIN
@app.middleware("request")
async def on_request(request: Request):
    # Pathの調整をする。
    path = unquote(request.path[1:])
    if path.endswith("/"):
        path = path[:-1]
    if not any(paths := path.split("/")) or "." not in paths[-1]:
        path = f"{path}/index.html"
    if not path.startswith("/"):
        path = f"/{path}"
    # ファイルを返す。
    real_path = f"{data['jinja2']['folder']}{path}"
    if "." in path and path.endswith(tuple(data["jinja2"]["exts"])):
        if await exists(real_path):
            return await template(path)
        elif await exists(f"{data['jinja2']['folder']}{path[:path.rfind('.')+1]}j2"):
            return await template(
                data['jinja2']['base'], **get_metas(path, paths)
            )
    if await exists(real_path):
        return await rfile(real_path)


@app.route("/ping")
async def ping(_: Request):
    return text("pong")


app.run(**data["app"])
