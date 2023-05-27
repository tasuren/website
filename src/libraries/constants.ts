// tasuren's Website - Constants

import { Article } from "./cms";
import { EnumOfArticles } from "./types";


export const WEBSITE_TITLE = "tasurenのウェブサイト";


export const SAMPLE_ARTICLE_ENUM_DATA: EnumOfArticles =
  import.meta.env.SAMPLE_ARTICLE_ENUM_DATA
    ? JSON.parse(import.meta.env.SAMPLE_ARTICLE_ENUM_DATA) : {};
export const SAMPLE_ARTICLE_CONTENT_DATA: Article = 
  import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA ? JSON.parse(
    import.meta.env.SAMPLE_ARTICLE_CONTENT_DATA
  ) : {};