// tasuren's Website - CMS

import { createClient, MicroCMSQueries } from "microcms-js-sdk";

import { SERVICE_DOMAIN } from "./constants";
import { sleep } from "./utils";


export const API_KEY = process.env.NO_MICROCMS ? "" : import.meta.env.MICROCMS_API_KEY;
console.log(SERVICE_DOMAIN);
export const client = createClient({
  serviceDomain: SERVICE_DOMAIN,
  apiKey: API_KEY,
});


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


export const getArticles = async (
  endpoint: string, queries?: MicroCMSQueries
) => await client.get<Articles>({endpoint: endpoint, queries});

export const getArticleDetail = async (
  endpoint: string, id: string,
  queries?: MicroCMSQueries
) => {
  return await client.getListDetail<Article>({
    endpoint: endpoint,
    contentId: id, queries,
  });
};


export async function* getAllArticles(
  endpoint: string, queries: MicroCMSQueries,
  interval: number = 0.04
): AsyncIterableIterator<Article[]> {
  queries.offset = 0;
  while (true) {
    // 記事を取得する。
    let articles = await getArticles(endpoint, queries);
    if (!articles.contents) { break; };
    yield articles.contents;
    queries.offset = articles.limit;
    await sleep(interval);
  };
};