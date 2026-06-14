# レイヤー構成

> ver 2.0 系（2026-06-08 OS隣接11層＋iPad専用層）を反映。**GitHub の live keymap が唯一の正。**
> バージョンの変遷は `07_version_history.md` を参照。

## レイヤー一覧（11層）

| Layer | 名前 | 区分 | 説明 |
|---|---|---|---|
| 0 | default_win | ベース | Windows用メイン（電源投入時のデフォルト） |
| 1 | window_win | ウィンドウ | Win固有：ウィンドウ/タブ/ブラウザ操作・F5・Del・絵文字 |
| 2 | default_mac | ベース | Mac用オーバーレイ（差分のみ・残り&trans透過） |
| 3 | window_mac | ウィンドウ | Mac固有：ウィンドウ/タブ/ブラウザ・⌘R・5方向スナップ・Del |
| 4 | default_ipad | ベース | iPad用オーバーレイ（差分のみ・残り&trans透過） |
| 5 | window_ipad | ウィンドウ | iPad固有：Globeベース操作・Del |
| 6 | num_sym | 共通 | 記号(左手)＋数値・電卓(右手) |
| 7 | nav | 共通 | 矢印・Home/End・PgUp/PgDn(右手)＋F6-F10/F2/F4(左手) |
| 8 | mouse | 共通 | マウスクリック（AML自動移行・定数固定） |
| 9 | scroll | 共通 | スクロール操作（定数固定） |
| 10 | bluetooth | 共通 | BT切替・bootloader・OS切替 |

> **設計：** ベース3種（win/mac/ipad）と対応するウィンドウ操作3種を **OS単位でペア隣接**（0-1, 2-3, 4-5）。
> **命名規則：** スネークケース（小文字）。
> **定数固定：** `#define MOUSE 8` / `scroll-layers = <9>` で参照。番号変更時は要追従。

## レイヤー移動トリガー

| レイヤー | 移動方法 |
|---|---|
| window_win (1) | Win時：変換／無変換ホールド |
| window_mac (3) | Mac時：かな／英数ホールド（LANG1/LANG2） |
| window_ipad (5) | iPad時：かな／英数ホールド（LANG1/LANG2） |
| num_sym (6) | Spaceホールド（左親指）／ Slashホールド（右手） |
| nav (7) | TABホールド |
| mouse (8) | トラックボール操作で自動移行（AML） |
| scroll (9) | Kホールド |
| bluetooth (10) | 3キー同時押し（key-positions 37 38 39） |

> window は各ベース層からそのOSのウィンドウ層へ向く（win→1 / mac→3 / ipad→5）。
> 変換/無変換・かな/英数は **tap=IME切替 / hold=windowレイヤー**。親指ホールドで両手が空く。

## レイヤースタック（定義順＝優先度・低→高）
```
0 default_win   ← 全キーの土台
1 window_win    ← Winでのみ到達
2 default_mac   ← Mac差分オーバーレイ（&trans透過）
3 window_mac    ← Macでのみ到達
4 default_ipad  ← iPad差分オーバーレイ（&trans透過）
5 window_ipad   ← iPadでのみ到達
6 num_sym       ← 共通
7 nav           ← 共通
8 mouse         ← 共通（固定・AML）
9 scroll        ← 共通（固定）
10 bluetooth    ← 共通
```

## ベース層の差分（Win=0 / Mac=2 / iPad=4）

| キー位置 | Win (0) | Mac (2) | iPad (4) |
|---|---|---|---|
| 左小指最左端前段 | LCTRL | LEFT_GUI（Cmd） | LEFT_GUI（Cmd） |
| 無変換位置 | window_win(1)hold / tap=INT_MUHENKAN | window_mac(3)hold / tap=LANG2（英数） | window_ipad(5)hold / tap=LANG2 |
| 変換位置 | window_win(1)hold / tap=INT_HENKAN | window_mac(3)hold / tap=LANG1（かな） | window_ipad(5)hold / tap=LANG1 |
| Space | num_sym(6)hold | num_sym(6)hold | num_sym(6)hold |
| Slash | num_sym(6)hold | num_sym(6)hold | num_sym(6)hold |
| TAB | nav(7)hold | nav(7)hold | nav(7)hold |
| スクリーンショット | LS(LG(S))（Win+Shift+S） | LG(LC(LS(NUMBER_4))) | &trans（未設定） |
| 残り全キー | （土台） | &trans（0に透過） | &trans（0に透過） |

## ウィンドウ層の差分（window_win=1 / window_mac=3 / window_ipad=5）

| 操作 | window_win | window_mac | window_ipad |
|---|---|---|---|
| 最大化/全画面 | LG(UP) | LC(LA(UP)) | globe_f（Globe+F） |
| 左/右スナップ・タイル | LG(LEFT)/LG(RIGHT) | LC(LA(LEFT))/LC(LA(RIGHT)) | globe_ctrl_left/right（Globe+Ctrl+←→） |
| 復元・下 | LG(DOWN) | LC(LA(DOWN)) | — |
| デスクトップ/Spaces/アプリ切替 | LG(LC(LEFT))/LC(LG(RIGHT)) | LC(LEFT)/LC(RIGHT) | globe_left/right（前/次アプリ） |
| タスクビュー/Exposé | LG(TAB) | LC(UP) | globe_up（App Switcher） |
| 全ウィンドウ表示 | — | — | globe_down（Globe+↓） |
| 前/次タブ | LS(LC(TAB))/LC(TAB) | LS(LC(TAB))/LC(TAB) | LS(LC(TAB))/LC(TAB) |
| 新規タブ | LC(T) | LG(T) | LG(T) |
| ブラウザ戻る/進む | LA(LEFT)/LA(RIGHT) | LG(LEFT_BRACKET)/LG(RIGHT_BRACKET) | LG(LEFT_BRACKET)/LG(RIGHT_BRACKET) |
| 更新 | F5 | LG(R) | LG(R) |
| ホーム/最小化 | — | — | LG(H)／LG(M) |
| Dock/通知/Spotlight | — | — | globe_a／globe_n／LG(SPACE) |
| 絵文字 | LG(DOT) | LC(LG(SPACE)) | GLOBE（単押し） |
| ウィンドウを閉じる | close_win（Ctrl+W） | close_mac（Cmd+W） | close_mac（Cmd+W） |
| Del | pos28（Backspace位置に Delete） | pos28（同左） | pos28（同左） |
| 5方向スナップ | 未配置 | LC(LA(NUMBER_1..5))右手下段 | — |
| Alt+F4 | alt_f4コンボ（X+C+V） | — | — |

> **Globeマクロ：** `macro_press GLOBE → macro_tap KEY → macro_release GLOBE`（v0.3-branchで利用可確認済み）。
> `globe_ctrl_left/right` は Globe+Ctrl+矢印の3要素マクロ。

## num_sym レイアウト

**左手＝記号**（上段はJIS Shift順）
```
! " # $ %     ← Shift+1〜5
' ( ) _ @
[ ] { } :
```
**右手＝電卓**
```
/  7  8  9  −
=  *  4  5  6  ＋     ← = は内側キー LS(MINUS)、* は H 位置 LS(SINGLE_QUOTE)
0  1  2  3  ．
```
> `&` は `amp` コンボ（layer 6限定）。`=`=`LS(MINUS)`、`*`=`LS(SINGLE_QUOTE)`。
> 記号は keymap-editor 互換のため **直接キーコード**で記述（`JP_*` define 不使用）。
> **Fキーはコンボ入力：** F7=R+T / F8=F+G / F9=Y+U / F10=H+J（既存）に加え、F2=Z+X（22+23）・F4=C+V（24+25）を左手下段に配置（Excel多用）。FキーはすべてF2〜F10がnum_sym層コンボで入力可能。
> **ESCコンボはベース6層(0-5)限定**（layers=<0 1 2 3 4 5>）：num_sym層以降での F10コンボ(H+J, 17+18)との誤爆を防ぐ。

## nav レイアウト

- 右手：矢印（↑↓←→）、Home/End、PgUp/PgDn（エンコーダ回転でも PgUp/PgDn）。
- 左手：F6-F10（中段・左詰め）、F2 / F4（下段）。
- F2/F4/F7-F10 は num_sym コンボからも入力可（nav層との重複配置）。

## コンボ一覧

| コンボ名 | キー位置 | 動作 | レイヤー | 備考 |
|---|---|---|---|---|
| tab | 11+12 | TAB | 全 | |
| shift_tab | 12+13 | Shift+TAB | 全 | |
| Alt_Left | 17+18 | MB4（戻る） | 0-5 | F10と競合回避のためbase+window限定 |
| Ctrl_Shift_1 | 29+30 | Ctrl+Shift+1 | 全 | |
| escape | 18+19 | ESC | 0-5 | num_sym以降でF10コンボとの誤爆防止 |
| Bluetooth | 37+38+39 | bluetooth層（&lt 10 SPACE） | 全 | |
| amp | 2+3 | `&`（Shift+6） | 6 | num_sym限定 |
| close_win | 30+32 | Ctrl+W | 0,1 | timeout35ms・idle150ms |
| close_mac | 30+32 | Cmd+W | 2,3,4,5 | Mac/iPad共通・timeout35ms |
| alt_f4 | 23+24+25 | Alt+F4 | 1 | window_win限定・timeout50ms |
| f7 | 3+4 | F7 | 6 | R+T |
| f8 | 13+14 | F8 | 6 | F+G |
| f9 | 5+6 | F9 | 6 | Y+U |
| f10 | 17+18 | F10 | 6 | H+J |
| f2 | 22+23 | F2 | 6 | Z+X（左手下段） |
| f4 | 24+25 | F4 | 6 | C+V（左手下段） |

> 誤爆対策：layer限定コンボは `require-prior-idle-ms=150` ＋短 timeout（35-50ms）。

## OS切り替え方法（bluetooth層）

### BT接続＋レイヤー同時切替（右手上段 Y/U/I）
- Y（sw_win）→ BT0接続 ＋ Layer 0（Windows）
- U（sw_mac）→ BT1接続 ＋ Layer 2（Mac）
- I（sw_ipad）→ BT2接続 ＋ Layer 4（iPad）

### 手動レイヤー切替フォールバック（右手中段 H/J/K）
- H → Layer 0（Win）／ J → Layer 2（Mac）／ K → Layer 4（iPad）
- 上段 Y/U/I と同じ Win/Mac/iPad 並び。BT接続はそのままで層だけ切り替えたい時／sw_*の層切替が効かなかった時の復帰用。
