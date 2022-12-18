// tasuren.xyz Articles - List

import { makeTagsText, setHashTagList } from "./common.js";


const url = new URL(window.location.href);
let tag = url.searchParams.get("tag") || "all";
let page = url.searchParams.get("page") || "0";


function makePageLink(newPage) {
  return `index.html?page=${newPage}${tag != "all" ? `&tag=${tag}` : ""}`;
};
window.makePageLink = makePageLink;
window.page = page;

function addPageLinks(mode, element) {
  var newPage;
  for (let i = 1; i < 5; i++) {
    newPage = mode == "minus" ? page - i : page + i;
    if (newPage < 0) break;
    element.innerHTML += ` <a href="${makePageLink(newPage)}">${newPage}</a> `;
  };
};


window.addEventListener("load", (_) => {
  if (tag != "all")
    document.getElementsByTagName("h1")[0].innerText += ` #${tag}`;

  // 記事一覧の取得を行う。
  fetch(`tags/${tag}/${page}.json`)
    .then((response) => {
      // 存在しないページの場合はブラウザバックする。
      if (response.status == 404) {
        alert("ここには何もないのでブラウザバックします。(*'-')b");
        history.back();
      } else return response.json();
    })
    .then((data) => {
      // 記事のリンクを作っていく。
      let main = document.getElementById("main");
      for (let article of data)
        main.innerHTML += `<li>
          <a href="${article.id}.html?tag=${tag}&page=${page}">${article.title}</a>
        </li>`;
    });

    fetch(`tags/index.json`)
      .then((response) => response.json())
      .then((data) => setHashTagList(data));

  // ページング用のリンクや入力ボックスを作る。
  let sub = document.getElementById("sub");
  sub.innerText = "ページ："
  addPageLinks("minus", sub);
  // ジャンプ用のボタンを作る。
  // TODO: なぜかここを`createElement`でやるとクリックしても動かなくなる。誰か対処法教えて。
  sub.innerHTML += '<input type="button" value="指定" onclick="location.href = makePageLink(prompt(\'ページ番号を入力してください。\', page));" />';
  addPageLinks("plus", sub);
});