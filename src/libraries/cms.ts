// tasuren's Website - CMS

import { MicroCMSQueries, createClient } from "microcms-js-sdk";

import { sleep } from "./utils";


export const API_KEY = (process.env.NO_MICROCMS
  ? null : import.meta.env.MICROCMS_API_KEY) || "...";
export const SERVICE_DOMAIN = (process.env.NO_MICROCMS
  ? null : import.meta.env.MICROCMS_SERVICE_DOMAIN) || "...";

export const NO_MICROCMS = process.env.NO_MICROCMS
  || API_KEY == "..." || SERVICE_DOMAIN == "...";
if (NO_MICROCMS) console.info(
  "現在、microCMSを使わないモードですので、microCMSのライブラリは使用不可です。"
);

export const client = createClient({
  serviceDomain: SERVICE_DOMAIN,
  apiKey: API_KEY,
});


export type Block<T> = {
  totalCount: number;
  offset: number;
  limit: number;
  contents: T[];
};


/**
 * 低レイヤーなmicroCMSのブログAPIのラッパ。
 * 抽象度が高いことからサンプルデータが用意されていませんので、microCMSが使えない状況ではエラーが発生します。
 */
export async function* getArticles<T>(
  endpoint: string, queries: MicroCMSQueries,
  interval: number = 1
): AsyncIterableIterator<T[]> {
  console.log("記事の読み込み中...")
  var offset = 0;
  while (true) {
    // 記事を取得する。
    let articles = await client.get<Block<T>>({endpoint, queries: {offset, ...queries}});
    console.log(`microCMSの${endpoint}から${articles.contents.length}個の記事を取得。クエリ:`, queries);
    if (!articles.contents.length) { break; };
    yield articles.contents;
    offset = articles.limit;
    await sleep(interval);
  };
};