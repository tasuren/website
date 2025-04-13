import { file } from "astro/loaders";
import { defineCollection, z } from "astro:content";
import { parse } from "toml";

const products = defineCollection({
    loader: file("src/content/products.toml", {
        parser: (text) => parse(text).products,
    }),
    schema: z.object({
        id: z.string(),
        title: z.string(),
        description: z.string(),
        skills: z.array(z.string()),
        link: z.string().url(),
    }),
});

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

export const collections = { products, sns };
