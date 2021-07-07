# tasuren's website main program

PROGRAM_NAME = "tasuren.website"
HOST = "0.0.0.0"
PORT = 80
TEMPLATE_ENGINE_EXTS = ("html", "tmp", "tpl")
BASE_PATH = "root"
NORMAL_CONTENT_FILES = ("menu.html")


from ujson import load, loads, dumps
from aiofiles import open as async_open
from os.path import exists

from sanic.response import file, html, redirect
from sanic.exceptions import abort, NotFound
from sanic import Sanic

from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask_misaka import Misaka


with open("data.json", "r", encoding="utf-8_sig") as f:
    data = load(f)


app = Sanic("RT-WebSite")


# Jinja2 テンプレートエンジンの定義。
env = Environment(loader=FileSystemLoader("./" + BASE_PATH),
                  autoescape=select_autoescape(TEMPLATE_ENGINE_EXTS),
                  enable_async=True)


# Jinja2テンプレートエンジンを使用してHTMLを返すためのコルーチン関数。
async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    content = await template.render_async(kwargs)
    return html(content)


# Flask-MisakaをJinja2にくっつける。
# マークダウンレンダリング用。
md = Misaka(
    autolink=True, wrap=True)
env.filters.setdefault("markdown", md.render)


# ===  MAIN ## === #
@app.route('/')
async def index(request):
    return redirect("/index.html")


@app.route('/<path:path>')
async def normal_two(request, path: str):
    if path.endswith(TEMPLATE_ENGINE_EXTS):
        file_name = path.split("/")
        if file_name:
            file_name = file_name[-1]
            if file_name == NORMAL_CONTENT_FILES or file_name.startswith("_"):
                return await template(path)
            else:
                main_file_name = "_" + file_name
                title = file_name[1:main_file_name.rfind(".")]
                return await template(
                    "index.html", file_name=main_file_name,
                    title=data["titles"].get(file_name, "notitle"))
        else:
            raise abort(404)
    else:
        return await file(BASE_PATH + "/" + path)


app.run(host=HOST, port=PORT)
