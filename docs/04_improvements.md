# キーマップ改善リスト

## 実装済み ✅

| 日付 | 内容 | コミット |
|---|---|---|
| 2026/05/04 | ZMK v0.3-branchへのバージョン固定 | 複数 |
| 2026/05/04 | Mac/iPadレイヤー追加（Layer 7） | ae4e67d |
| 2026/05/04 | ARROW_MACレイヤー追加（Layer 8、BetterSnapTool対応） | ae4e67d |
| 2026/05/04 | BT+レイヤー同時切り替えマクロ（sw_win/sw_mac/sw_ipad） | ae4e67d |
| 2026/05/04 | USB有線接続時の手動レイヤー切り替え（BTレイヤーQ/W） | ae4e67d |
| 2026/05/04 | INTERNATIONAL_2 → INT_HENKAN修正 | 複数 |
| 2026/05/04 | LEFT_ALT追加（5605bb5相当） | 781c74d |
| 2026/05/04 | KP_NUMBER_0変更 | 781c74d |
| 2026/05/06 | require-prior-idle-ms追加（&mt / lt_to_layer_0 / mt_exit_AML_on_tap） | 852f871 |
| 2026/05/06 | quick-tap-ms 0→150ms修正（②） | 852f871 |
| 2026/05/06 | MacレイヤーをLayer 7から&trans透過方式に変更（SYMBOL/NUM/MOUSE使用可能に） | 565bc73 |
| 2026/05/06 | Macレイヤー（Layer 2）にControl・Optionキー追加 | ユーザー自身 |
| 2026/05/06 | BTレイヤーを右手操作に集約（Y=sw_win/U=sw_mac/I=sw_ipad/H=有線Win/J=有線Mac） | 9952d4f |
| 2026/05/06 | Macスクリーンショット Cmd+Ctrl+Shift+4（Layer 2で上書き） | 9952d4f |
| 2026/05/06 | レイヤー番号・名称の再構成（スネークケース統一、Win/Mac隣接配置） | 9952d4f |
| 2026/05/06 | JP_ defineを直接JISキーコードに置換・TILDE/GRAVE修正 | 94a5882 |
| 2026/06/04 | arrow_winにタブ移動(前/次)・PageUp/Down・ブラウザ戻る/進む/新規タブを追加、タブ移動をWin標準(Ctrl系)に修正（⑤一部・LiNEA40「次のタブ」実装） | 83cc2a8 |
| 2026/06/04 | AML誤起動対策：CONFIG_PMW3610_MOVEMENT_THRESHOLD 0→5（roBa_R.conf） | 5ec03f1 |
| 2026/06/04 | arrow_macにMac用タブ/ブラウザ操作を反映（前/次タブ=Ctrl系、戻る/進む=Cmd+[ / Cmd+]、新規タブ=Cmd+T、PageUp/Down）（⑬実装） | 35df8ff |

---

## 未実装・優先度高 🔴

### ⑤ ARROWレイヤー下段を活用（**arrow_win / arrow_mac とも一部実装済み**）
**効果：** ARROWレイヤー中に使える操作が増え作業効率向上。
**現状（2026/06/04）：** arrow_win / arrow_mac の下段にブラウザ操作を実装済み。
- arrow_win：X=戻る LA(LEFT) / C=新規タブ LC(T) / V=進む LA(RIGHT)
- arrow_mac：X=戻る LG(LEFT_BRACKET) / C=新規タブ LG(T) / V=進む LG(RIGHT_BRACKET)
**残課題：**
- 両レイヤーとも下段の残りキー・親指は未使用（&trans）。
**追加候補（未実装分）：**
- LC(Z) = Undo / LC(Y) = Redo / LC(A) = 全選択 / LC(S) = 保存 / LC(F) = 検索

### ⑦ Caps Wordの追加
**効果：** スネークケース・大文字定数入力が楽になる。
**内容：** `&caps_word` をsymbolレイヤーの空きキーに配置。
次の単語だけ大文字で入力でき、スペース・Enter等で自動解除。

### ⑨ ESCコンボの追加
**効果：** ESCがホームポジションから即アクセス可能になる。現状はarrow_winレイヤー移動が必要。
**候補：** J+K同時押し（key-positions: 18 19）
```c
escape {
    bindings = <&kp ESCAPE>;
    key-positions = <18 19>;
    timeout-ms = <50>;
};
```

### ⑲ 閉じたタブを再度開く（arrowレイヤーに追加）
**効果：** 誤ってタブを閉じたとき即座に復元できる。
**現状（2026/06/04）：** 新規タブ（Win=LC(T) / Mac=LG(T)）は実装済み。
「閉じたタブ再開」（Win=LC(LS(T)) / Mac=LG(LS(T))）はまだ別キーに未配置。
**実装：** arrow_win / arrow_mac の空きキー位置に配置する。

---

## 未実装・優先度中 🟡

### ⑩ default_macのLEFT_WINをMac固有キーに変更
**現状：** Layer 2に `LEFT_GUI` と `LEFT_WIN`（実質同じキー）が並んでいる。
**候補：** `LG(SPACE)` = Spotlight検索 / `LC(SPACE)` = 入力ソース切替

### ⑪ MOUSEレイヤーにMB4/MB5を追加
**効果：** マウス操作中にブラウザの前後移動ができる。
**現状：** MB1/MB2/MB3のみ。MB4（戻る）MB5（進む）が未設定。

### ⑫ SYMBOLレイヤーの重複解消
**現状：** `(`（LS(NUMBER_8)相当）と `)`（LS(NUMBER_9)相当）が左手上段・下段の2箇所ずつに重複。
**対処：** 一方を `<` `>` や `EQUAL` など別の記号に変更。

### ⑳ BetterSnapTool 5方向スナップ（arrow_macの右手に追加）
**効果：** 現状4方向（上下左右）のみのところ、右手に5つ追加することで細かいレイアウト操作が可能になる。
**候補キーコード（BetterSnapTool設定に合わせて調整要）：**
| キー | 動作候補 |
|---|---|
| `LC(LA(NUMBER_1))` | 左1/3 |
| `LC(LA(NUMBER_2))` | 中1/3 |
| `LC(LA(NUMBER_3))` | 右1/3 |
| `LC(LA(NUMBER_4))` | 左2/3 |
| `LC(LA(NUMBER_5))` | 右2/3 |

---

## 未実装・優先度低 ⚪

### ⑯ Ctrl_wコンボの位置見直し
**現状：** key-positions 5+6（TとYの隣接）→ 誤発動リスクがある。
**懸念：** Ctrl+Wはウィンドウ・タブを閉じる操作のため誤発動が致命的。
**対処：** より押しにくい位置か、レイヤー内キーへの移動を検討。

### ⑱ MacレイヤーのRCTRLをRight Optionに変更
**現状：** Layer 2の右端親指に `RCTRL`（Macではほぼ未使用）。
**候補：** `RIGHT_ALT`（Right Option） または `LG(SPACE)`（Spotlight）

---

## 見送り決定 ❌

### ⑥ hold-trigger-key-positions
**理由：** 左手Shiftの使い方と相容れない。
- じんさんはShiftが左手Z位置のみ
- 左手キーの大文字入力を日常的に使う
- 設定すると左手大文字が全部打てなくなる

---

## 参考：LiNEA40サンプル分析

> 参照動画：https://www.youtube.com/watch?v=DbFIhT8gaXo

### Mac/Win共通操作リスト（同じ物理キーで異なるキーコード）

| 操作 | Mac（arrow_mac） | Win（arrow_win） | roBa実装状況 |
|---|---|---|---|
| 閉じたタブを再開 | `LG(LS(T))` | `LC(LS(T))` | 未実装 → ⑲（新規タブは実装済み） |
| 前のタブへ | `LS(LC(TAB))` | `LS(LC(TAB))` | 実装済み ✅（両レイヤーCtrl系） |
| 次のタブへ | `LC(TAB)` | `LC(TAB)` | 実装済み ✅ |
| ブラウザ戻る | `LG(LEFT_BRACKET)`(⌘[) | `LA(LEFT)` | 実装済み ✅ |
| ブラウザ進む | `LG(RIGHT_BRACKET)`(⌘]) | `LA(RIGHT)` | 実装済み ✅ |
| 新規タブ | `LG(T)` | `LC(T)` | 実装済み ✅ |
| PageUp / PageDown | `PAGE_UP` / `PAGE_DOWN` | 同左（OS共通） | 実装済み ✅ |
| ウィンドウ最大化 | `LC(LA(UP))` | `LG(UP)` | 実装済み ✅ |
| 左/右スナップ | `LC(LA(LEFT/RIGHT))` | `LG(LEFT/RIGHT)` | 実装済み ✅ |
| 仮想デスクトップ左/右 | `LC(LEFT/RIGHT)` | `LC(LG(...))` | 実装済み ✅ |
| Mission Control / タスクビュー | `LC(UP)` | `LG(TAB)` | 未実装 |

**roBaとの設計上の違い：** LiNEA40はOS別に完全独立ベースレイヤー方式。
roBaは&trans透過方式（Winを土台にMac差分だけ上書き）で維持コストが低い。

---

## 補足：keymapの空レイヤースロット

keymap-editor経由の編集により、keymap末尾に `layer_9` 〜 `layer_20` の空レイヤー
（全キー&trans）が自動生成されている。機能には影響しないが、レイヤー設計上は無視してよい。
