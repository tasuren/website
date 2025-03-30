/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
const config = {
    trailingComma: "es5",
    tabWidth: 4,
    semi: true,
    plugins: ["prettier-plugin-astro"],
};

export default config;
