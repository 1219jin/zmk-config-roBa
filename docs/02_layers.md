# レイヤー構成

> 2026-06-07 の大改修を反映した最新版。GitHub の live keymap が唯一の正。

## レイヤー一覧

| Layer | 名前 | 説明 |
|---|---|---|
| 0 | default_win | Windows用メイン（電源投入時のデフォルト） |
| 1 | window_win | Win固有：ウィンドウ/タブ/ブラウザ操作・F5・Alt+F4・絵文字 |
| 2 | default_mac | Mac/iPad用オーバーレイ（差分のみ明示・残り&trans透過） |
| 3 | window_mac | Mac固有：ウィンドウ/タブ/ブラウザ操作・更新(⌘R)・5方向スナップ・絵文字 |
| 4 | mouse | マウスクリック（AML自動移行・定数固定） |
| 5 | scroll | スクロール操作（定数固定） |
| 6 | bluetooth | BT切替・bootloader・OS切替 |
| 7 | num_sym | 記号(左手)＋数値・電卓(右手) |
| 8 | nav | 矢印・Home/End・PgUp/PgDn(右手)＋F6-F10/F2/F4(左手) |

> **命名規則：** スネークケース（小文字）。`window_win`/`window_mac` は大文字を含まない。
> **Layer 4・5は定数固定：** `#define MOUSE 4` / `scroll-layers = <5>` で参照。番号変更不可。

## レイヤー移動トリガー（★2026-06-07改）

| レイヤー | 移動方法 |
|---|---|
| num_sym (7) | **Spaceホールド（左親指）/ Slashホールド（右手）** |
| window (1/3) | **変換ホールド / 無変換ホールド**（OS別：Win→window_win(1)、Mac→window_mac(3)） |
| nav (8) | TABホールド |
| scroll (5) | Kホールド |
| bluetooth (6) | **3キー同時押し（key-positions 37 38 39）** ※B単独ホールドは廃止 |
| mouse (4) | トラックボール操作で自動移行（AML） |

> **設計思想：** window を親指ホールドにしたことで両手が空き、右手のスナップ・ブラウザ操作が使える。
> num_sym は Space＝右手で数字 / Slash＝左手で記号、と相手手で押せる配置。
> 変換/無変換はPC側（Google日本語入力でMac流の英/かな）にリマップ済み。**tap=IME切替 / hold=windowレイヤー**。

## レイヤースタック（定義順＝優先度・低→高）

```
Layer 0: default_win   ← 全キーの土台
Layer 1: window_win    ← Winでのみ到達
Layer 2: default_mac   ← Mac差分オーバーレイ（&trans透過）
Layer 3: window_mac    ← Macでのみ到達
Layer 4: mouse         ← 共通（固定・AML）
Layer 5: scroll        ← 共通（固定）
Layer 6: bluetooth     ← 共通
Layer 7: num_sym       ← 共通
Layer 8: nav           ← 共通
```

## Layer 0 vs Layer 2 の差分

| キー位置 | Win (Layer 0) | Mac (Layer 2) |
|---|---|---|
| 左小指最左端前段 | LCTRL | LEFT_GUI（Cmd） |
| 無変換位置 | window_win(1)ホールド / tap=INT_MUHENKAN | window_mac(3)ホールド / tap=LANG2（英数） |
| 変換位置 | window_win(1)ホールド / tap=INT_HENKAN | window_mac(3)ホールド / tap=LANG1（かな） |
| Slash | num_sym(7)ホールド | num_sym(7)ホールド（共通） |
| スクリーンショット | LS(LG(S))（Win+Shift+S） | LG(LC(LS(NUMBER_4)))（Cmd+Ctrl+Shift+4） |
| Layer 2の残り全キー | — | &trans（Layer 0に透過） |

## window_win vs window_mac の差分

| 操作 | window_win（Win） | window_mac（Mac） |
|---|---|---|
| ウィンドウ最大化 | LG(UP) | LC(LA(UP)) |
| 左/右スナップ | LG(LEFT) / LG(RIGHT) | LC(LA(LEFT)) / LC(LA(RIGHT)) |
| 復元・下 | LG(DOWN) | LC(LA(DOWN)) |
| 仮想デスクトップ/Spaces 左右 | LG(LC(LEFT)) / LC(LG(RIGHT)) | LC(LEFT) / LC(RIGHT) |
| タスクビュー / Mission Control | LG(TAB) | LC(UP) |
| 前/次タブ | LS(LC(TAB)) / LC(TAB) | LS(LC(TAB)) / LC(TAB) |
| 新規タブ | LC(T) | LG(T) |
| ブラウザ戻る/進む | LA(LEFT) / LA(RIGHT) | LG(LEFT_BRACKET) / LG(RIGHT_BRACKET) |
| 更新 | F5 | LG(R) |
| ウィンドウを閉じる | LA(F4) | （close_macコンボ Cmd+W で対応） |
| 絵文字 | LG(DOT) | LC(LG(SPACE)) |
| 5方向スナップ（1/3・2/3） | 未配置 | LC(LA(NUMBER_1..5))（右手下段） |

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
 =  *  4  5  6  ＋     ← = は内側キー(LS(MINUS))、* は H(LS(SINGLE_QUOTE))
 0  1  2  3  ．
```
> `&` は `amp` コンボ（layer 7限定）で入力。`=` = `LS(MINUS)`、`*` = `LS(SINGLE_QUOTE)`。
> 記号は keymap-editor 互換のため **直接キーコード**で記述（`JP_*` define は不使用）。

## nav レイアウト

- 右手：矢印（↑↓←→）、Home/End、PgUp/PgDn（エンコーダ回転でも PgUp/PgDn）
- 左手：F6-F10（中段）、F2 / F4

## コンボ一覧

| コンボ名 | キー位置 | 動作 | 備考 |
|---|---|---|---|
| tab | 11+12 | TAB | |
| shift_tab | 12+13 | Shift+TAB | |
| Alt_Left | 17+18 | マウスボタン4（戻る） | |
| Ctrl_Shift_1 | 29+30 | Ctrl+Shift+1 | |
| escape | 18+19 | ESC | |
| amp | 2+3 | `&`（Shift+6） | **layer 7限定**（通常打鍵で誤爆しない） |
| close_win | 30+32 | Ctrl+W | layers 0,1・timeout 35ms |
| close_mac | 30+32 | Cmd+W | layers 2,3・timeout 35ms |
| Bluetooth | 37+38+39 | bluetoothレイヤー（ホールド） | |

## OS切り替え方法

### Bluetooth接続（bluetoothレイヤー経由）
bluetoothレイヤー（3キー同時押し）→ 右手上段
- Y（sw_winマクロ）→ BT0接続 + Layer 0（Windows）
- U（sw_macマクロ）→ BT1接続 + Layer 2（Mac）
- I（sw_ipadマクロ）→ BT2接続 + Layer 2（Mac兼用）

### USB有線接続（bluetoothレイヤー経由）
bluetoothレイヤー → 右手中段
- H → Layer 0（Windowsモード）
- J → Layer 2（Macモード）
