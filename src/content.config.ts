import { file } from "astro/loaders";
import { defineCollection, z } from "astro:content";
import { parse } from "toml";

const sns = defineCollection({
    loader: file("src/content/sns.toml", {
        parser: (text) => parse(text).sns,
    }),
    schema: z.object({
        id: z.string(),
        link: z.string().url(),
        src: z.string().optional(),
    }),
});

export const collections = { sns };
