# tasuren.xyz

from __future__ import annotations

from typing import TypedDict, Any
from collections.abc import Sequence

from time import time, sleep

from os import environ, mkdir
from os.path import isdir
from pathlib import PurePath

from itertools import chain

from nisshi import Manager, Bundle

import requests
from ciso8601 import parse_datetime
from orjson import loads, dumps


API_BASE_URL = "https://tasuren.microcms.io/api/v1/"
API_KEY = environ.get("MICROCMS_API_KEY")
API_KEY_HEADER = "X-MICROCMS-API-KEY"
ENDPOINTS = ("articles", "services")
TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"


class MiniArticleData(TypedDict):
    "最低限の記事データの型です。"

    published_at: float
    revised_at: float
    title: str
    tags: Sequence[str]
    id: str


class TagMetaData:
    "タグのメタデータを入れるためのクラスです。"

    def __init__(self, output: PurePath) -> None:
        self.count, self.output = 0, output
        if not isdir(self.output):
            mkdir(self.output)


class TagMainData:
    "タグのメインデータを格納したりするためのクラスです。"

    def __init__(self) -> None:
        self.length, self.data = 0, list[MiniArticleData]()


class TagData:
    "タグのデータを格納するためのクラスです。"

    def __init__(self, output: PurePath) -> None:
        self.meta = TagMetaData(output)
        self.init_main()

    def init_main(self) -> None:
        "`.main`を初期化します。"
        self.main = TagMainData()

    def write(self) -> None:
        "タグのデータを書き込みます。"
        if self.meta.output is None:
            raise RuntimeError("まだ書き込みの準備が整っていません。")
        with open(self.meta.output.joinpath(f"{self.meta.count}.json"), "wb") as f:
            f.write(dumps(self.main.data))
        self.meta.count += 1

    def close(self) -> None:
        "タグのデータのファイルが何個あるかを示すためのメタデータファイルを作ります。"
        with open(self.meta.output.joinpath("index.txt"), "w") as f:
            f.write(str(self.meta.count))


class MicroCMSArticlesBundle(Bundle):
    "MicroCMSの記事を書き出す処理を実装したバンドルです。"

    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def request_cms(self, method: str, uri: str, *args: Any, **kwargs: Any) -> requests.Response:
        "MicroCMSのAPIにリクエストを行います。"
        if API_KEY_HEADER not in (headers := kwargs.get("headers", {})):
            headers.setdefault(API_KEY_HEADER, API_KEY)
            kwargs["headers"] = headers
        self.manager.console.log("Request to MicroCMS: %s %s(%s, %s)" % (uri, method, args, kwargs))
        return getattr(requests, method)(f"{API_BASE_URL}{uri}", *args, **kwargs)

    @Bundle.listen()
    def on_before_build_all(self) -> None:
        if not API_KEY:
            return

        root_output = PurePath(self.manager.config.include_folder)
        for endpoint in ENDPOINTS:
            self.manager.console.log(f"[bold blue]Buiding articles[/bold blue] {endpoint}...")

            tags = dict[str, TagData]()
            tags_output = (endpoint_output := 
                root_output.joinpath(endpoint)).joinpath("tags")
            if not isdir(endpoint_output):
                mkdir(endpoint_output)
            if not isdir(tags_output):
                mkdir(tags_output)

            tags["all"] = TagData(tags_output.joinpath("all"))

            # 記事データを全て読み込んでまとめる。
            while data := loads(self.request_cms("get", endpoint, params=(
                ("offset", 10 * tags["all"].meta.count),
            )).content)["contents"]:
                self.manager.console.log(f"Writing metadata {tags['all'].meta.count}...")

                for article in data:
                    # タグデータをまとめる。
                    for tag in chain(article["tags"], ("all",)):
                        if tag not in tags:
                            tags[tag] = TagData(tags_output.joinpath(tag))

                        article["publishedAt"] = parse_datetime(article["publishedAt"]) \
                            .strftime(TIME_FORMAT)
                        article["revisedAt"] = parse_datetime(article["revisedAt"]) \
                            .strftime(TIME_FORMAT)
                        tags[tag].main.data.append(MiniArticleData(
                            published_at=article["publishedAt"],
                            revised_at=article["revisedAt"],
                            title=article["title"],
                            tags=article["tags"],
                            id=article["id"]
                        ))

                        tags[tag].main.length += 1
                        if tags[tag].main.length == 10:
                            tags[tag].write()
                            tags[tag].init_main()

                    # 記事を書き出す。
                    output = endpoint_output.joinpath(f"{article['id']}.html")
                    self.manager.console.log("Rendering...\t", output)

                    page = ExtendedPage(self.manager, output)

                    page.ctx.title = article["title"]
                    page.ctx.published_at = article["publishedAt"]
                    page.ctx.revised_at = article["revisedAt"]
                    page.ctx.tags = article["tags"]
                    page.ctx.page = tags["all"].meta.count
                    page.ctx.is_article = True

                    page.content = article["content"]
                    with open(output, "w") as f:
                        f.write(self.manager.tempylate.render_from_file(
                            self.manager.config.default_layout,
                            __self__=page
                        ))

                sleep(0.5)

                for tag in tags:
                    if tags[tag].main.length != 0:
                        tags[tag].write()
                    tags[tag].close()

                with open(tags_output.joinpath("index.json"), "wb") as f:
                    f.write(dumps(tuple(tags.keys())))


def setup(manager: Manager):
    manager.add_bundle(MicroCMSArticlesBundle(manager))


class ExtendedPage(Manager.page_cls):
    "便利な機能を追加で実装したページクラスです。"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ctx.thumbnail = None
        self.ctx.published_at = None
        self.ctx.revised_at = None
        self.ctx.tags = ()
        self.ctx.page = 0
        self.ctx.is_article = False

    def make_article_list(self) -> None:
        "記事一覧を作るようにJSスクリプトを埋め込みます。(正確にはJSファイルを読み込むようにする。)"
        self.insert_head(
            '<script src="/assets/articles/list.js%s" type="module"></script>'
                % (self.last_updated,)
        )

    def insert_head(self, head: str) -> None:
        self.ctx.head = f"{self.ctx.head}{head}"

    @property
    def last_updated(self) -> str:
        return "?last_updated=%s" % time()

    @property
    def tags(self) -> str:
        return '\n<div id="hashtags">タグ：</div><br>\n'