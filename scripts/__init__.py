# tasuren.f5.si - Script

from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime

from pathlib import PurePath, Path
from os.path import exists

from nisshi import Page
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


index: PurePath | None = None
def setup(manager: Manager) -> None:
    manager.extend_page(NewPage)

    # 新しい記事または記事が更新されるたびに記事一覧のページを更新するようにする。
    def rebuild_index():
        assert index is not None
        manager.build(index, True)

    def check(path: PurePath) -> None:
        global index
        if index is None and path.stem != "index" \
                and exists((path := path.parent.joinpath("index.md"))):
            index = path
            if not manager.is_building_all:
                rebuild_index()

    @manager.listen()
    def on_after_build_page(page: NewPage) -> None:
        check(page.input_path)

    @manager.listen()
    def on_after_build_directory(path: PurePath) -> None:
        if index is not None and path.name == index.parent.name:
            rebuild_index()

    @manager.listen()
    def on_clean(input_path: PurePath | None, output_path: PurePath, is_directory: bool) -> None:
        if not is_directory:
            check(output_path)