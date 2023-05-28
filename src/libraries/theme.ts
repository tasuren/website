// tasuren's Website - テーマ


// 実験ができるようにウィンドウを拡張。
interface MyWindow extends Window { resetTheme(): void; };
/** @ts-ignore */
declare var window: MyWindow;


// 色々準備。
export type Theme = "dark" | "light";
export type Setting = Theme | "auto";
export const EMOJIS: {[theme: string]: string} = {
  auto: "🌓", dark: "🌙", light: "☀️"
};


// highlight.jsのスタイルデータの取り扱いのためのAPI。
export let styleLinks = null;
export function updateHighlightStyle(theme: Theme) {
  if (styleLinks == null) {
    let element = document.getElementById("highlight-style-links");
    if (element) styleLinks = JSON.parse(element.innerText);
    else styleLinks = {};
  };
  if (theme in styleLinks) {
    var link = document.getElementById("highlight-style") as HTMLLinkElement | null;
    if (!link) {
      link = document.createElement("link");
      link.rel = "stylesheet";
      link.id = "highlight-style";
      document.head.append(link);
    };
    link.href = styleLinks[theme];
    link.setAttribute("data-theme", theme);
  };
};


// 設定変更用のAPI。
export function get(): Setting {
  return localStorage.getItem("theme") as Setting || "auto"
};
export function set(setting: Setting): Setting {
  localStorage.setItem("theme", setting); return setting;
};
export function reset() { return localStorage.removeItem("theme"); };
window.resetTheme = reset;

export function roll(setting: Setting): Setting {
  if (setting == "auto") setting = "dark";
  else if (setting == "dark") setting = "light";
  else setting = "auto";
  return setting;
}

export var emoji = EMOJIS.dark;
export function updateEmoji(setting: Setting) {
  emoji = EMOJIS[setting];
  dispatchEvent(new CustomEvent("updateemoji", { detail: EMOJIS[setting] }));
};
export function effect(
  setting?: Setting, theme?: Theme,
  enableUpdateHighlightStyle: boolean = false
) {
  if (theme) document.documentElement
    .setAttribute("data-theme", theme);
  if (setting) updateEmoji(setting);
  if (enableUpdateHighlightStyle) updateHighlightStyle(theme);
};
export function detectTheme(setting: Setting): Theme {
  if (setting == "auto")
    return window.matchMedia
      ("(prefers-color-scheme: dark)")
        .matches ? "dark" : "light";
  else return setting;
};


export function initialize() {
  // 前の設定を引き継ぐ。
  let setting = get();
  // 初期化する。
  let theme = detectTheme(setting);
  if (theme == "light") effect(setting, "light");
  else if (setting == "auto") effect(setting);
  updateHighlightStyle(theme);
};