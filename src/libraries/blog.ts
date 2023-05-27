// tasuren's website - Blog API

import { MicroCMSQueries } from "microcms-js-sdk";

import { client } from "./cms";
import { sleep } from "./utils";


/* 型 */
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
export type Articles = {
  totalCount: number;
  offset: number;
  limit: number;
  contents: Article[];
};

export type EnumOfArticles = {[tag: string]: Article[]};


/* 一般 */
export async function* getArticles(
  endpoint: string, queries: MicroCMSQueries,
  interval: number = 1
): AsyncIterableIterator<Article[]> {
  console.log("記事の読み込み中...")
  var offset = 0;
  while (true) {
    // 記事を取得する。
    let articles = await client.get<Articles>({endpoint, queries: {offset, ...queries}});
    console.log(`microCMSの${endpoint}から${articles.contents.length}個の記事を取得。クエリ:`, queries);
    if (!articles.contents.length) { break; };
    yield articles.contents;
    offset = articles.limit;
    await sleep(interval);
  };
};


export const SAMPLE_ARTICLE_ENUM_DATA: EnumOfArticles =
  import.meta.env.SAMPLE_ARTICLE_ENUM_DATA
    ? JSON.parse(import.meta.env.SAMPLE_ARTICLE_ENUM_DATA) : {};
export const SAMPLE_ARTICLE_CONTENT_DATA: Article = 
  import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA ? JSON.parse(
    import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA
  ) : {};