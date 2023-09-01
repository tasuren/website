import { NO_MICROCMS, getArticles } from "./cms";


export type Article = {
  id: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
  revisedAt: string;
  title: string;
  content: string;
  tags: string[];
};

export type EnumOfArticles<T=Article> = {[tag: string]: T[]};


/** 記事の内容のサンプルデータ。 */
export const SAMPLE_ARTICLE_CONTENT_DATA: EnumOfArticles =
  import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA
    ? JSON.parse(import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA) : {
      "id":"81011451445451919nna-",
      "createdAt":"2023-02-14T23:57:31.148Z",
      "updatedAt":"2023-02-17T07:25:04.182Z",
      "publishedAt":"2023-02-15T23:16:33.847Z",
      "revisedAt":"2023-02-17T07:25:04.182Z",
      "title":"Astroプロジェクトのテストケースのタイトルでありますよ。",
      "content":"<p>これはテストです。そうテストケース。</p><h1>見出し1</h1><p>wow</p><pre><code class=\"language-python\">from random import randint\nprint(randint(1, 6))</code></pre>",
      "tags":["cort_corporation","yjsnpi","tono"]
    };
export const QUERIES = Object.freeze({fields: [
  "id", "tags", "title", "content", "publishedAt", "revisedAt"
], limit: 128});

/** microCMSから記事の内容を全て少しづつ取得します。 */
export async function* getContents(): AsyncIterableIterator<Iterable<Article>> {
  if (NO_MICROCMS) {
    var tempArticle;
    for (let articles of Object.values(SAMPLE_ARTICLE_ENUM_DATA))
      yield articles.map(article => {
        tempArticle = {...SAMPLE_ARTICLE_CONTENT_DATA};
        tempArticle.id = article.id;
        return tempArticle;
      });
  } else
    for await (let articles of getArticles<Article>("blog", QUERIES))
      yield articles;
};


/** 記事の小さい形でのメタデータのサンプル。 */
export const SAMPLE_ARTICLE_SMALL_METADATA = {
  "id": "5bopmct4enkv",
  "title": "Darkmode.jsを使ってPythonドキュメントを簡単にダークモード対応してみた。",
  "publishedAt": "2022-01-14T15:30:00.000Z",
  "tags": ["Python", "JavaScript"],
};
/** 記事をタグ別でまとめた際のサンプルデータ。 */
export const SAMPLE_ARTICLE_ENUM_DATA: EnumOfArticles = 
  import.meta.env.SAMPLE_ARTICLE_ENUM_DATA ? JSON.parse(
    import.meta.env.SAMPLE_ARTICLE_ENUM_DATA
  ) : {
    "all": [SAMPLE_ARTICLE_SMALL_METADATA],
    "Python": [SAMPLE_ARTICLE_SMALL_METADATA],
    "JavaScript": [SAMPLE_ARTICLE_SMALL_METADATA]
  };


export interface Context { allTags: string[] }
export interface ArticleForEnum extends Article { ctx: Context };

/** 一覧ページ用の記事データを取得します。 */
export async function getEnum(): Promise<EnumOfArticles<ArticleForEnum>> {
  let allArticles: {[tag: string]: ArticleForEnum[]} = {"all": []};
  // Astroの`paginate`した後でも、全てのタグに参照できるようにする。
  // そのために、この配列を全ての記事データに同梱させる。そして、最後に中身を張る。
  let allTags: string[] = [];

  if (NO_MICROCMS) {
    // もし`API_KEY`が設定されていない場合は、サンプルデータを使用する。`
    Object.assign(allArticles, SAMPLE_ARTICLE_ENUM_DATA);
    for (let articles of Object.values(allArticles))
      for (let index in articles) articles[index].ctx = {allTags: allTags};
  } else {
    // 取得して整理する。
    for await (let articles of getArticles<Article>(
      "blog", {limit: 183, fields: ["id", "title", "tags", "publishedAt"]}
    ))
      for (var article of articles.map(article => article as ArticleForEnum)) {
        article.ctx = {allTags: allTags};
        allArticles["all"].push(article);

        for (let tag of article.tags) {
          if (!(tag in allArticles)) allArticles[tag] = [];
          if (tag == "all") console.warn(`IDが${article.id}の記事が予約済みのタグを使っています。`);
          allArticles[tag].push(article);
        };
      };
    // テスト用：console.log(JSON.stringify(allArticles));
  };

  // 全てのタグをまとめる。
  allTags.push(...Object.keys(allArticles));
  return allArticles;
};