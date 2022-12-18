// tasuren.xyz Articles - Page

import { setHashTagList } from "./common.js";


// 全てのハッシュタグを表示する。
window.addEventListener("load", (_) => setHashTagList(
  document.getElementById("tags").getAttribute("data-tags").split(",")
));