import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
    site: "https://tasuren.jp",
    prefetch: true,
    integrations: [sitemap(), mdx(), tailwind()],
});
