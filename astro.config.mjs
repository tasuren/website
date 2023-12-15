import { defineConfig } from 'astro/config';
import sitemap from "@astrojs/sitemap";


const DEFAULT_LAYOUT = '/src/Layout.astro';
function setDefaultLayout() {
  return function (_, file) {
    const {
      frontmatter
    } = file.data.astro;
    if (!frontmatter.layout) frontmatter.layout = DEFAULT_LAYOUT;
  };
}
;


// https://astro.build/config
export default defineConfig({
  site: "https://tasuren.jp",
  base: "/",
  prefetch: true,
  markdown: {
    remarkPlugins: [setDefaultLayout]
  },
  integrations: [sitemap()]
});