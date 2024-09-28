import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
    site: "https://tasuren.jp",
    base: "/",
    prefetch: true,
    integrations: [sitemap()],
});
