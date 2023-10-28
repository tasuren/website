// date-fnsの初期化をします。

import { setDefaultOptions } from "date-fns";
import jaLocale from "date-fns/locale/ja";


// デフォルトのdate-fnsの言語設定を日本語にする。 
setDefaultOptions({
  locale: jaLocale
});