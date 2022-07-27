# tasuren.f5.si - Script

from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime

from pathlib import PurePath, Path
from os.path import exists

from nisshi import Bundle, Page
from nisshi.tools import enum

if TYPE_CHECKING:
    from nisshi import Manager


# TODO: 以下にあるものは記事をまとめるためのものと、それを`index.md`に書き込むものとなっている。
#   これを拡張として別で用意したいと思っている。例：`nisshi.ext.articles`


class NewPage(Page):
    @property
    def articles(self) -> str:
        return "\n".join(
            "- *{}* : [{}](/{})".format(
                datetime.fromtimestamp(t.st_ctime).strftime("%Y年%m月%d日 %H時%M分%S秒"),
                path.stem, self.manager.exchange_extension(
                    PurePath().joinpath(*path.parts[1:]),
                    self.manager.config.output_ext
                )
            )
            for path, t in sorted(map(
                lambda p: (p, p.stat()),
                enum(Path(self.input_path.parent))
            ), key=lambda x: x[1].st_ctime)
            if path.stem != "index"
        )


class SimpleArticleSystem(Bundle):
    "新しい記事または記事が更新されるたびに記事一覧のページを更新するようにするためのバンドルです。"

    def __init__(self, manager: Manager):
        self.manager = manager
        self.nisshi: PurePath | None = None

    def rebuild_index(self) -> None:
        assert self.index is not None
        self.manager.build(self.index, True)

    def process(self, path: PurePath) -> None:
        if self.index is None and path.stem != "index" \
                and exists((path := path.parent.joinpath("index.md"))):
            self.index = path
            if not self.manager.is_building_all:
                self.rebuild_index()

    @Bundle.listen()
    def on_after_build_page(self, page: NewPage) -> None:
        self.process(page.input_path)

    @Bundle.listen()
    def on_after_build_directory(self, path: PurePath) -> None:
        if self.index is not None and path.name == self.index.parent.name:
            self.rebuild_index()

    @Bundle.listen()
    def on_clean(self, _, output_path: PurePath, is_directory: bool) -> None:
        if not is_directory:
            self.check(output_path)


def setup(manager: Manager) -> None:
    manager.extend_page(NewPage)
    manager.add_bundle(SimpleArticleSystem(manager))