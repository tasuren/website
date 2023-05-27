// tasuren's Website - CMS

import { createClient } from "microcms-js-sdk";


export const NO_MICROCMS = process.env.NO_MICROCMS;
if (NO_MICROCMS) console.info(
  "現在、microCMSを使わないモードですので、microCMSのライブラリは使用不可です。"
);


export const API_KEY = process.env.NO_MICROCMS
  ? "..." : import.meta.env.MICROCMS_API_KEY;
export const SERVICE_DOMAIN = process.env.NO_MICROCMS
  ? "_test_mode" : import.meta.env.MICROCMS_SERVICE_DOMAIN;
export const client = createClient({
  serviceDomain: SERVICE_DOMAIN,
  apiKey: API_KEY,
});