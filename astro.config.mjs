import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "astro/config";

export default defineConfig({
    site: "https://tasuren.jp",
    prefetch: true,
    integrations: [sitemap(), mdx()],
    vite: {
        plugins: [tailwindcss()],
    },
});
