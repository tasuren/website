// tasuren.xyz Articles - Common


const HASHTAG_ELEMENT = '<a class="hashtag" ';


/** 渡されたタグのリストのタグを全てハッシュタグにして連結しHTMLにします。 */
export function makeTagsText(tags) {
  if (tags) return tags.map((tag) => `${
    HASHTAG_ELEMENT}href="./index.html?tag=${tag
    }" class="hashtag">#${tag}</a>`).join("");
  else return "";
};


/** ハッシュタグのリストの文字列をHTMLに設置します。 */
export function setHashTagList(tags) {
  let hashtags = document.getElementById("hashtags");
  hashtags.innerHTML += makeTagsText(tags).replace("#all", "#全部");
};