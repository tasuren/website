// 投稿について。

import { Article } from "./cms";


export interface PageMetadata {
  title: string, description?: string
}

export interface Frontmatter extends PageMetadata {
  draft?: boolean, layout?: string
}

export type EnumOfArticles = {[name: string]: Article[]};