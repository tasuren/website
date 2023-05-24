// tasuren's Website - CMS

import { createClient, MicroCMSQueries } from "microcms-js-sdk";

import { SERVICE_DOMAIN, BLOG_ENDPOINT as ENDPOINT } from "./constants";


export const API_KEY = import.meta.env.MICROCMS_API_KEY;
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
  queries?: MicroCMSQueries
) => await client.get<Articles>({endpoint: ENDPOINT, queries});

export const getArticleDetail = async (
  contentId: string,
  queries?: MicroCMSQueries
) => {
  return await client.getListDetail<Article>({
    endpoint: ENDPOINT,
    contentId, queries,
  });
};