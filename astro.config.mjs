import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import icon from "astro-icon";
import { defineConfig } from "astro/config";

export default defineConfig({
    site: "https://tasuren.jp",
    prefetch: true,
    integrations: [sitemap(), mdx(), icon()],
    vite: {
        plugins: [tailwindcss()],
    },
});
