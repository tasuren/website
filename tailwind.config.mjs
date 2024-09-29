/** @type {import('tailwindcss').Config} */
export default {
    content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
    theme: {
        extend: {
            colors: {
                link: "#539af8",
                "link-visited": "#9268de",
            },
            typography: ({ theme }) => ({
                tasuren: {
                    css: {
                        "--tw-prose-headings": theme("colors.zinc[800]"),
                        "--tw-prose-invert-headings": theme("colors.zinc[300]"),
                        "--tw-prose-links": theme("colors.link"),
                        "--tw-prose-invert-links": theme("colors.link"),
                    },
                },
            }),
        },
    },
    plugins: [require("@tailwindcss/typography")],
    corePlugins: {
        preflight: false,
    },
};
