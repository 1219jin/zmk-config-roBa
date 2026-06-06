# レイヤー構成

## レイヤー一覧

| Layer | 名前 | 説明 |
|---|---|---|
| 0 | default_win | Windows用メイン（電源投入時のデフォルト） |
| 1 | arrow_win | カーソル・ウィンドウ・タブ操作（Windows用） |
| 2 | default_mac | Mac/iPad用オーバーレイ（差分のみ明示、残り&trans透過） |
| 3 | arrow_mac | カーソル・ウィンドウ・タブ操作（Mac/BetterSnapTool用） |
| 4 | mouse | マウスクリック（AML自動移行・定数固定） |
| 5 | scroll | スクロール操作（定数固定） |
| 6 | bluetooth | BT切り替え・bootloader |
| 7 | symbol | 記号入力（JIS対応） |
| 8 | num | 数字・ファンクションキー |

> **命名規則：** スネークケース（小文字）に統一
> **Layer 4・5は定数固定：** `#define MOUSE 4` / `scroll-layers = <5>` で参照されるため番号変更不可
> **空レイヤー：** keymap末尾に `layer_9`〜`layer_20`（全&trans）がkeymap-editorにより自動生成されているが機能に影響なし。

## レイヤースタック（優先度）

```
高  Layer 8: num        ← 共通
    Layer 7: symbol     ← 共通
    Layer 6: bluetooth  ← 共通
    Layer 5: scroll     ← 共通（固定）
    Layer 4: mouse      ← 共通（固定・AML）
    Layer 3: arrow_mac  ← Macでのみ到達
    Layer 2: default_mac← Mac差分オーバーレイ（&trans透過）
    Layer 1: arrow_win  ← Winでのみ到達
低  Layer 0: default_win← 全キーの土台
```

## レイヤー移動トリガー

| レイヤー | 移動方法 |
|---|---|
| symbol (7) | スペースホールド / スラッシュホールド |
| num (8) | 変換ホールド / 無変換ホールド |
| arrow_win (1) | TABホールド（Layer 0から） |
| mouse (4) | トラックボール操作で自動移行（AML） |
| scroll (5) | Kホールド |
| bluetooth (6) | Bホールド / 3キー同時押し（key-positions: 37 38 39） |
| arrow_mac (3) | TABホールド（Layer 2から） |

## Layer 0 vs Layer 2 の差分

| キー位置 | Win (Layer 0) | Mac (Layer 2) |
|---|---|---|
| 左小指最左端前段 | LCTRL | LEFT_GUI（Cmd） |
| 左親指（無変換） | INT_MUHENKAN | LANG2（英数） |
| 右親指（変換） | INT_HENKAN | LANG1（かな） |
| TABホールド先 | Layer 1（arrow_win） | Layer 3（arrow_mac） |
| スクリーンショット | LS(LG(S))（Win+Shift+S） | LG(LC(LS(NUMBER_4)))（Cmd+Ctrl+Shift+4） |
| Layer 2の残り全キー | — | &trans（Layer 0に透過） |

## arrow_win vs arrow_mac の差分（ウィンドウ操作）

| 操作 | arrow_win（Windows） | arrow_mac（Mac/BetterSnapTool） |
|---|---|---|
| ウィンドウ最大化 | LG(UP) | LC(LA(UP)) |
| 左半分スナップ | LG(LEFT) | LC(LA(LEFT)) |
| 右半分スナップ | LG(RIGHT) | LC(LA(RIGHT)) |
| 元に戻す | LG(DOWN) | LC(LA(DOWN)) |
| 左のデスクトップ | LG(LC(LEFT)) | LC(LEFT) |
| 右のデスクトップ | LC(LG(RIGHT)) | LC(RIGHT) |

## arrow_win / arrow_mac のタブ・ブラウザ操作（2026/06/04 実装）

arrow_win（83cc2a8・ユーザー実装）と arrow_mac（35df8ff）に、同じ物理位置で
OSごとのキーを配置。**前/次タブはブラウザ共通の Ctrl 系**（Mac でも Cmd+Tab は
アプリ切替になるため Ctrl 系を使用）、戻る/進む・新規タブは OS 固有キー。

| 操作 | 物理位置 | arrow_win（Win） | arrow_mac（Mac） |
|---|---|---|---|
| 前のタブへ | 左手上段2列目（W） | LS(LC(TAB)) | LS(LC(TAB)) |
| 次のタブへ | 左手上段4列目（R） | LC(TAB) | LC(TAB) |
| PageUp | 右手上段2列目（U） | PAGE_UP | PAGE_UP |
| PageDown | 右手上段4列目（O） | PAGE_DOWN | PAGE_DOWN |
| ブラウザ戻る | 左手下段2列目（X） | LA(LEFT) | LG(LEFT_BRACKET)（⌘[） |
| 新規タブ | 左手下段3列目（C） | LC(T) | LG(T)（⌘T） |
| ブラウザ進む | 左手下段4列目（V） | LA(RIGHT) | LG(RIGHT_BRACKET)（⌘]） |

> 「閉じたタブを再開」（Win=LC(LS(T)) / Mac=LG(LS(T))）は未配置（improvements ⑲）。

## OS切り替え方法

### Bluetooth接続（bluetoothレイヤー経由）
bluetoothレイヤー（3キー同時押しまたはBホールド）→ 右手キー
- Y（sw_winマクロ）→ BT0接続 + Layer 0（Windows）
- U（sw_macマクロ）→ BT1接続 + Layer 2（Mac）
- I（sw_ipadマクロ）→ BT2接続 + Layer 2（Mac兼用）

### USB有線接続（bluetoothレイヤー経由）
bluetoothレイヤー → 右手中段
- H → Layer 0（Windowsモード）
- J → Layer 2（Macモード）

## コンボ一覧

| コンボ名 | キー位置 | 動作 |
|---|---|---|
| tab | 11+12 | TAB |
| shift_tab | 12+13 | Shift+TAB |
| Ctrl_w | 5+6 | Ctrl+W |
| Alt_Left | 17+18 | マウスボタン4（戻る） |
| Ctrl_Shift_1 | 29+30 | Ctrl+Shift+1 |
| Bluetooth | 37+38+39 | bluetoothレイヤー（ホールド） |
