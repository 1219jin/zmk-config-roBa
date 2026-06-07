# キーマップ改善リスト

## 実装済み ✅

### 2026-06-07 大改修（レイヤー再設計）
バックアップ：ブランチ `backup/20260607-before-redesign`（commit `1c8e5de`）／凍結ファイル `roBa_keymap_20260607_baseline.keymap`

| 内容 | コミット |
|---|---|
| SYMBOL＋NUM を `num_sym`（左手記号・右手電卓）に統合 | 大改修一括 |
| ARROW/ARROW_MAC を `nav`（矢印・F）＋ `window_win`/`window_mac`（ウィンドウ・タブ・ブラウザ）に再編 | 大改修一括 |
| レイヤー番号/名称を整理（0:win 1:window_win 2:default_mac 3:window_mac 4:mouse 5:scroll 6:bluetooth 7:num_sym 8:nav） | 大改修一括 |
| トリガー再割り当て（num_sym←Space/Slash、window←変換/無変換、nav←TAB） | keymap-editor調整 |
| `escape` コンボ追加（key-positions 18+19）＝改善⑨ | 大改修一括 |
| `close_win`/`close_mac` コンボ（Ctrl+W / Cmd+W、レイヤー限定・短timeout）で誤爆対策＝改善⑯対応 | 大改修一括 |
| window_mac に BetterSnapTool 5方向スナップ（1/3・2/3、LC(LA(NUMBER_1..5))）＝改善⑳ | 467f40a |
| num_sym `=` バグ修正（`LS(EQUAL)`はJISで`~`が出る → `LS(MINUS)`が正） | 467f40a |
| num_sym に `*`（`LS(SINGLE_QUOTE)`）を復活（物理5列に収まらず一旦欠落していた） | 467f40a |
| num_sym 左手記号を再キュレーション（上段JIS Shift順 `! " # $ %`、`' ( ) _ @`、`[ ] { } :` を直接キー化） | 467f40a |
| `&` を `amp` コンボ（layer 7限定、Shift+6）に移動 | 467f40a |
| B単独ホールド廃止（bluetoothは3キー同時押しのみ）／CapsLock追加 | keymap-editor調整 |

### それ以前（〜2026-06-04）
| 日付 | 内容 | コミット |
|---|---|---|
| 2026/05/04 | ZMK v0.3-branch へのバージョン固定 | 複数 |
| 2026/05/04 | Mac/iPad対応・BT＋レイヤー同時切替マクロ（sw_win/sw_mac/sw_ipad）・有線手動切替 | ae4e67d 他 |
| 2026/05/06 | require-prior-idle-ms / quick-tap-ms 調整、Mac透過方式化、レイヤー再構成 | 852f871 / 565bc73 / 9952d4f |
| 2026/06/04 | AML誤起動対策：`CONFIG_PMW3610_MOVEMENT_THRESHOLD` 0→5（roBa_R.conf） | 5ec03f1 |

---

## 未実装・優先度高 🔴

### ⑦ Caps Word の検討
**現状：** 大改修で `CAPSLOCK`（トグル）を追加済み。`caps_word`（次の単語だけ大文字・自動解除）とは別物。
**残：** snake_case／定数入力に `caps_word` の方が向く場面があれば、CapsLockと使い分けるか置換を検討。

---

## 未実装・優先度中 🟡

### ⑤ window/nav 下段の追加活用
**候補：** Undo/Redo/保存/検索/全選択（`LC(Z)`/`LC(Y)`/`LC(S)`/`LC(F)`/`LC(A)`）。
**注意：** これらは「文書編集」であり**ウィンドウ操作とは別コンセプト**。windowには入れず、nav側か別レイヤーに置くのが筋。

### ⑩ default_mac の Mac固有キー拡充
**候補：** `LG(SPACE)`（Spotlight）/ `LC(SPACE)`（入力ソース切替）。

### ⑪ mouse レイヤーに MB4/MB5
**現状：** MB1/MB2/MB3 のみ（MB4は Alt_Left コンボにあり）。MB5（進む）未配置。

### ㉑ 比較演算子クラスタ `< = >`
**現状：** `=` は num_sym 右手にあるが `< >` は未配置。Fish配列由来の改善候補。

---

## 未実装・優先度低 ⚪

### ⑱ window_mac の右親指キー見直し
**候補：** `RIGHT_ALT`（Right Option）等。

---

## 見送り決定 ❌

### ⑥ hold-trigger-key-positions
**理由：** 左手Shift（Z位置のみ）の使い方と相容れない。設定すると左手大文字が打てなくなる。

### ⑲ 閉じたタブを再開
**決定（2026-06-07）：** 普段使わないため**課題から削除**。新規タブ（Win=LC(T)/Mac=LG(T)）は実装済み。

---

## 補足：keymap-editor 経由の編集について
- 大改修後の微調整は keymap-editor で実施（トリガー再割り当て・CapsLock追加等）。
- 記号は **直接キーコード**で統一（`JP_*` define を使わない）。`=` のように生コードを誤ると JIS で別記号が出るため、JIS対応表（05）で必ず確認すること。
