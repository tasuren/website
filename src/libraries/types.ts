// 投稿について。

export interface Article {
  title: string, description?: string
}

export interface Frontmatter extends Article {
  draft?: boolean, layout?: string
}