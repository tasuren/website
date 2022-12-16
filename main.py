# tasuren.xyz - Backend

from collections.abc import Iterator

from shutil import rmtree, copy
from os import listdir, mkdir, remove, walk
from os.path import exists, isdir
from pathlib import PurePath

from tempylate import Manager
from mizu import parse_ext

from rich import get_console


MARKDOWN_EXTENSIONS = ("md",)
MARKDOWN_EXTENSIONS_AFTER_RENDER = ".html"
TEMPLATE_EXTENSIONS = ("html", "htm") + MARKDOWN_EXTENSIONS
DEFAULT_LAYOUT_FILE = "layout.html"
INPUT_PATH = PurePath("input")
OUTPUT_PATH = PurePath("output")


console = get_console()


console.print("Preparing...")
# 必要なフォルダを用意する。
if exists(OUTPUT_PATH):
    console.log("Removing output files...")
    for path in map(OUTPUT_PATH.joinpath, listdir(OUTPUT_PATH)):
        if isdir(path):
            rmtree(path)
        else:
            remove(path)
else:
    console.log("Creating output directory...")
    mkdir(OUTPUT_PATH)


class ExtendedManager(Manager):
    "便利な関数を追加で実装した`.Manager`です。"

    def format_link(self, link: str) -> str:
        return f"- []"

    def get_file_names(self, path: str | PurePath) -> Iterator[str]:
        "指定されたパスにあるファイルなどの名前を返します。"
        for name in listdir(path):
            yield name


manager = ExtendedManager()


class Context:
    "ファイルの設定等を保管するためのクラスです。"

    template: str | None = DEFAULT_LAYOUT_FILE
    title = "..."
    description = ""
    head = ""
    content = ""


if exists(INPUT_PATH):
    console.print("Processing files...")

    for root, directories, files in walk(INPUT_PATH):
        root = PurePath(root)
        for path in map(root.joinpath, files):
            output = OUTPUT_PATH.joinpath(*path.parts[1:])

            # まだ存在していないフォルダは作る。
            if isdir(path.parent) and not exists(output.parent):
                console.log("Creating new direcotry...\t", output.parent)
                mkdir(output.parent)

            if path.suffix[1:] not in TEMPLATE_EXTENSIONS:
                # コピーするだけで良い場合。
                console.log("Copying...\t", path)
                copy(path, output)
                continue

            console.log("Rendering...\t", path)
            ctx = Context()
            with open(path, "r") as f:
                ctx.content = f.read()

            # レンダリングする。
            ctx.content = manager.render(ctx.content, str(path), ctx=ctx)
            for ext in MARKDOWN_EXTENSIONS:
                if path.suffix[1:] == ext:
                    ctx.content = parse_ext(ctx.content, tables=True)
                    output = output.with_suffix(MARKDOWN_EXTENSIONS_AFTER_RENDER)
                    break
            # テンプレートが指定されている場合は、そのテンプレートで継承を行う.
            if ctx.template is not None:
                ctx.content = manager.render_from_file(ctx.template, ctx=ctx)

            with open(output, "w") as f:
                f.write(ctx.content)