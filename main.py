# tasuren's website main program

PROGRAM_NAME = "tasuren.website"
HOST = "0.0.0.0"
PORT = 800
TEMPLATE_ENGINE_EXTS = ("html", "tmp", "tpl")
BASE_PATH = "root"
NORMAL_CONTENT_FILES = ("menu.html", "googlebad1ca1c18db0f38.html")


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
    if path[-1] == "/":
        path = path[:-1]
    if "." not in path:
        path = path + "/index.html"
    true_path = BASE_PATH + "/" + path
    file_split = path.rfind("/")
    if file_split == -1:
        file_split = 0
    file_name = path[file_split:]
    if file_name[0] == "/":
        file_name = file_name[1:]
    true_main_page = path[:file_split] + "/_" + file_name
    if true_main_page[0] != "/":
        true_main_page = "/" + true_main_page
    true_main_page = BASE_PATH + true_main_page
    menu_right_mode = exists(true_main_page)
    if exists(true_path) or menu_right_mode:
        if path.endswith(TEMPLATE_ENGINE_EXTS):
            # titleを取得する。
            titles = data["titles"].get(path, {})
            if titles == {}:
                json_path = ((BASE_PATH + "/" if file_split != 0 else BASE_PATH)
                             + path[:file_split] + "/titles.json")
                if exists(json_path):
                    async with async_open(json_path, "r") as f:
                        data["titles"][path] = loads(await f.read())
                else:
                    data["titles"][path] = {}
                titles = data["titles"][path]
            title = titles.get(file_name, file_name[:file_name.rfind(".")])
            # ファイルを返す。
            if menu_right_mode:
                new_path = "index.html"
            else:
                new_path = path
                file_name = ""
            print(path)
            return await template(
                new_path, ext_js_name=data["ext_js"].get(path, "/none.js"),
                title=title, file_name="/" + true_main_page[len(BASE_PATH) + 1:])
        else:
            # 普通にファイルを返す場合。
            return await file(true_path)
    else:
        return abort(404)


app.run(host=HOST, port=PORT)
