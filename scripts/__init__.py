# tasuren.f5.si - Script

from os import listdir

from nisshi.ext.articles import Manager


class NewPage(Manager.page_cls):
    def process_blog_list_metadata(self) -> None:
        "ブログの記事一覧のページのメタデータを設定したり、ブログの一覧のマークダウンを作ってそれを返したりします。"
        self.ctx.make_back_link = True
        self.ctx.title = f"{self.input_path.parent.name}年のtasurenのブログ記事一覧"
        self.ctx.description = f"{self.input_path.parent.name}年にtasurenが書いた記事の一覧があるウェブページです。"
        return f"# {self.input_path.parent.name}年のtasurenの記事一覧\n{self.format_articles()}"

    def make_blog_year_list(self) -> str:
        "ブログの年別一覧を表示する。"
        return "\n".join(
            f"- [{file_name}年]({file_name})"
            for file_name in sorted(filter(
                lambda n: len(n) == 4 and "." not in n,
                listdir(self.input_path.parent)
            ), key=int, reverse=True)
        )