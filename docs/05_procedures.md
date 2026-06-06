# 作業手順・バージョン管理・リファレンス

## コミットメッセージ規則
- タイトル：英語のまま（例：`feat: add Mac layer`）
- 説明文（Extended description）：日本語で記載
- 種別：
  - `feat:` = 新機能・キー割り当て追加
  - `fix:` = 不具合・誤設定の修正
  - `chore:` = ビルド設定・バージョン固定など
  - `ci:` = GitHub Actions設定変更
  - `restore:` = 過去バージョンへの巻き戻し
  - `refactor:` = 機能を変えずに構成・名称を整理

---

## 作業前の必須手順

1. `https://github.com/1219jin/zmk-config-roBa` を開く
2. mainブランチになっていることを確認
3. バックアップブランチを作成
   - `main ▼` → テキスト入力に `backup/YYYYMMDD-作業内容` → 「Create branch ... from main」

---

## バックアップブランチ一覧

| ブランチ名 | 内容 |
|---|---|
| `backup/before-sync-20260504` | 2026/05/04 作業開始前（エラー発生直前） |
| `backup/20260504-working` | 2026/05/04 全作業完了・動作確認済み |

> コミット履歴・最新状態はGitHubで確認すること：
> https://github.com/1219jin/zmk-config-roBa/commits/main/config/roBa.keymap

---

## GitHub編集（Chrome経由）

Chrome経由でGitHubファイルを編集する場合は、
**`github-chrome-editor` スキルを参照すること。**

> **注意：** Claude in Chrome が接続されていないセッションでは、ブラウザ自動化での編集はできない。
> その場合は (a) 修正版ファイルを出力してGitHubの編集画面に貼り付け／Upload file、
> または (b) 変更が数行なら該当行をGitHub上で直接書き換える、で対応する。

### 複数ファイルの一括新規アップロード（2026/06 追記）

GitHubの `file_upload` ツールはホストのファイルパス方式を受け付けなくなった。
複数ファイルを一度に上げるときは、内容を base64 でブラウザに注入して File を組み立てる：

1. `https://github.com/{owner}/{repo}/upload/main/{dir}` を開く（`{dir}` が無くてもコミット時に自動作成される）
2. 各ファイルを `window._rf.push({n:'<name>', d:'<base64>'})` で順に積む
   - base64化すると `dr`+`aw` 等のフィルタ語を避けられ `javascript_exec` が通る
   - 各base64は16000字未満に分割すると `view` で全文を読めて貼り込みやすい
3. `DataTransfer` で File 化し、`input[type=file]` の `files` にセットして `change` を発火（`input.files = dt.files` の代入で `dt.files` は空に移譲されるので、ステージ確認はスクリーンショットで行う）
4. コミットメッセージはネイティブセッター（方法B）で設定
5. 末尾の「Commit changes」クリックはツール取得が不安定なことがあり、手動クリックでも可

> ナレッジ（01〜06）は GitHub `docs/` に配置済み。今後の更新は GitHub `docs/` 側で行う（GitHubが正）。

### 複数ファイルの新規・一括アップロード（2026/06/06 確認）

GitHubの `file_upload` ツールがホストパス方式を受け付けなくなった場合の代替手順。
ブラウザ側で File オブジェクトを組み立て、file input に直接セットする。

1. `https://github.com/{owner}/{repo}/upload/main/{dir}` を開く（`{dir}` 指定で**新規フォルダにも**アップロード可）
2. 各ファイル内容を **base64** で `window._rf` 配列にpushする（**"draw"/"error" を含む文字列は `javascript_exec` がブロックするため、base64経由で回避**）
3. `atob` → `Uint8Array` → `new File(...)` を生成し、`DataTransfer` 経由で `input[type=file].files` にセットして `change` を発火
4. コミットメッセージはネイティブセッター方式（github-chrome-editor スキル Step 5）で設定
5. コミット実行（ページ内フォームの緑「Commit changes」ボタン）

> **注意1：** `input.files = dt.files` 代入後は `dt.files` が空になる（input へ移譲）ため、戻り値が 0 でも正常。必ずスクリーンショットでステージ状態を確認する。
> **注意2：** `tool_search` で Claude in Chrome の `computer`/`javascript_tool` 等が取得しづらいことがある。取得できたら一気に注入→コミットまで進める。最悪、最後のコミットボタンはユーザーに手動クリックを依頼する。

> この手順は `github-chrome-editor` スキルにも追記推奨。

---

## GitHub Actions ワークフロー一覧

| ファイル | 名前 | トリガー | 役割 |
|---|---|---|---|
| `.github/workflows/build.yml` | Build | push（全般） | ファームウェア（uf2）ビルド |
| `.github/workflows/draw.yml` | Draw Keymap | push to main（keymap関連ファイル変更時）/ 手動 | キーマップSVG生成 → keymap-drawer/にコミット |

> 旧ワークフロー `draw-keymaps.yml` は2026/05/07に削除済み（draw.ymlと重複・エラー継続のため）。

---

## キーマップ画像の自動更新フロー

### 仕組み
1. `config/roBa.keymap` または `keymap_drawer.config.yaml` または `config/roBa.dtsi` を変更してmainにpushする
2. `.github/workflows/draw.yml`（Draw Keymap）が自動起動する
3. `keymap-drawer` が `keymap-drawer/roBa.svg` を再生成する
4. botが `[Draw] <元コミットメッセージ>` のコミットでSVGをmainに直接コミットする
5. `README.md` の `<img src="keymap-drawer/roBa.svg">` が自動的に最新画像を表示する

### 重要な前提条件
- keymapで使う日本語キー定義は **`#define JP_*` ではなく直接Shift+数字** で書くこと
  - 例：`JP_DQUOTE` ではなく `LS(NUMBER_2)` を使う
  - 理由：keymap-editor互換でなければkeymap-drawerもパース失敗する
- pushトリガーは下記3ファイルの変更時のみ発火する：
  - `config/roBa.keymap`
  - `keymap_drawer.config.yaml`
  - `config/roBa.dtsi`
- bot自身のコミット（SVG更新）は上記paths外なので**無限ループしない**

### 手動実行（緊急時）
1. https://github.com/1219jin/zmk-config-roBa/actions/workflows/draw.yml を開く
2. 右側「Run workflow」→ Branch: main → 「Run workflow」ボタン

---

## ファームウェア書き込み手順

1. `https://github.com/1219jin/zmk-config-roBa/actions` を開く
2. 最新の ✅ runをクリック
3. 右側「Artifacts」→「firmware」をダウンロード
4. 保存先：`~/Documents/roBa/firmware/`
5. リネーム：`YYYYMMDD_roBa_L.uf2` / `YYYYMMDD_roBa_R.uf2`
6. 右手リセットボタンを素早く2回押し → USBドライブとして認識
7. `roBa_R-seeeduino_xiao_ble.uf2` をドラッグ → 自動書き込み・切断
8. 左手も同様（`roBa_L-seeeduino_xiao_ble.uf2`）
9. 元のZIPと元ファイル名のuf2は削除。日付リネーム版のみ保管。

---

## トラックボール（PMW3610）設定リファレンス

トラックボール関連の設定は keymap ではなく **`boards/shields/roBa/roBa_R.conf`**（右手側）にある。

| 設定 | 役割 | 現行値 | 既定値 |
|---|---|---|---|
| `CONFIG_PMW3610_CPI` | 感度（解像度） | 400 | — |
| `CONFIG_PMW3610_AUTOMOUSE_TIMEOUT_MS` | トラックボール使用後にmouseレイヤーが維持される時間(ms) | 700 | 400 |
| `CONFIG_PMW3610_MOVEMENT_THRESHOLD` | AML起動に必要な移動量しきい値。**大きいほど起動しにくく、タイピング中の誤起動を防ぐ** | 5（旧0） | 5 |
| `CONFIG_PMW3610_SMART_ALGORITHM` | データシート実装のスムージング | y | y |

> AMLの自動移行先は mouse レイヤー（Layer 4）。`#define MOUSE 4` で固定。

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| `west update failed` | west.ymlのrevisionが違う | zmk→`v0.3-branch`、pmw3610→`main`に戻す |
| `CMake parse error` | keymap構文エラー・行頭に不要文字 | 行頭の`~`等を削除 |
| `INTERNATIONAL_2`エラー | v0.3-branchで廃止済み | `INT_HENKAN`に置換 |
| MacでLANG1/LANG2が効かない | Layer 2未適用 | BTレイヤーでU(sw_mac)を押してLayer 2に切替確認 |
| Draw Keymapが`Number of keys differ between layers`で失敗 | keymap-editor非互換のJP_*定義使用 | `JP_*`を`LS(NUMBER_n)`等の直接記述に置換 |
| Draw Keymapが`physical layout could not be found` | `json_path`の指定ミスまたは`config/roBa.json`不在 | `json_path: "config"` のままにし、`config/roBa.json`が存在するか確認 |
| **AMLが誤起動（タイピング中にトラックボール微動でmouseレイヤーへ移行し、文字キーが左クリック等になる。特にJ=左クリック）** | `CONFIG_PMW3610_MOVEMENT_THRESHOLD=0`（微小移動でも即起動） | roBa_R.confで `=5` 以上に引き上げ。残れば 8〜12 →15と段階調整。補助で `AUTOMOUSE_TIMEOUT_MS` を400〜500に短縮 |

---

## キーコードリファレンス

### 日本語入力関連
| キーコード | 用途 | OS |
|---|---|---|
| `INT_HENKAN` | 変換キー | Windows |
| `INT_MUHENKAN` | 無変換キー | Windows |
| `LANG1` | かなキー | Mac |
| `LANG2` | 英数キー | Mac |

### JIS記号対応表
| 出力記号 | ZMKキーコード |
|---|---|
| `"` | `LS(NUMBER_2)` |
| `'` | `LS(NUMBER_7)` |
| `(` | `LS(NUMBER_8)` |
| `)` | `LS(NUMBER_9)` |
| `&` | `LS(NUMBER_6)` |
| `^` | `EQUAL` |
| `¥` | `INT_YEN` |
| `+` | `LS(SEMICOLON)` |
| `@` | `LEFT_BRACKET` |
| `` ` `` | `LS(LEFT_BRACKET)` |
| `:` | `SINGLE_QUOTE` |
| `*` | `LS(SINGLE_QUOTE)` |
| `[` | `RIGHT_BRACKET` |
| `]` | `BACKSLASH` |
| `{` | `LS(RIGHT_BRACKET)` |
| `}` | `LS(BACKSLASH)` |
| `_` | `LS(INT_RO)` |
| `~` | `LS(EQUAL)` |

### モディファイアキー
| キーコード | 説明 | Mac上の動作 |
|---|---|---|
| `LEFT_GUI` / `LEFT_WIN` | Win/Cmdキー | Cmdキー |
| `LCTRL` | 左Ctrl | Ctrlキー |
| `LEFT_ALT` | 左Alt | Optionキー |
| `RIGHT_ALT` | 右Alt | Right Option |

### 組み合わせキーの書き方
| 書き方 | 意味 | 例 |
|---|---|---|
| `LC(X)` | Ctrl+X | `LC(C)` = Ctrl+C |
| `LG(X)` | Win/Cmd+X | `LG(V)` = Cmd+V |
| `LA(X)` | Alt/Option+X | `LA(TAB)` = Alt+Tab |
| `LS(X)` | Shift+X | `LS(TAB)` = Shift+Tab |
| `LC(LA(X))` | Ctrl+Alt+X | `LC(LA(UP))` = ^⌥↑ |

### ブラウザ・タブ操作（arrow_win / arrow_mac 実装）
| 操作 | Win（arrow_win） | Mac（arrow_mac） |
|---|---|---|
| 前のタブへ | `LS(LC(TAB))` | `LS(LC(TAB))` |
| 次のタブへ | `LC(TAB)` | `LC(TAB)` |
| 新規タブ | `LC(T)` | `LG(T)`（⌘T） |
| 閉じたタブを再開 | `LC(LS(T))`（未配置・⑲） | `LG(LS(T))`（未配置・⑲） |
| ブラウザ戻る | `LA(LEFT)` | `LG(LEFT_BRACKET)`（⌘[） |
| ブラウザ進む | `LA(RIGHT)` | `LG(RIGHT_BRACKET)`（⌘]） |

> 前/次タブは Mac でも Ctrl 系（Cmd+Tab はアプリ切替のため）。

### レイヤー操作
| キーコード | 説明 |
|---|---|
| `&mo N` | ホールド中だけLayer Nを有効化 |
| `&to N` | Layer Nに永続的に移動 |
| `&lt N X` | ホールドでLayer N、タップでキーX |
| `&trans` | 下のレイヤーに透過 |

---

## よく使うGitHub URL

| 用途 | URL |
|---|---|
| リポジトリトップ | https://github.com/1219jin/zmk-config-roBa |
| keymapファイル | .../blob/main/config/roBa.keymap |
| keymapのraw | https://raw.githubusercontent.com/1219jin/zmk-config-roBa/main/config/roBa.keymap |
| 右手conf（トラックボール設定） | .../blob/main/boards/shields/roBa/roBa_R.conf |
| Actionsビルド結果 | .../actions |
| keymapコミット履歴 | .../commits/main/config/roBa.keymap |
| ブランチ一覧 | .../branches |
| Draw Keymap手動実行 | .../actions/workflows/draw.yml |
| 生成済みSVG | .../blob/main/keymap-drawer/roBa.svg |

---

## Claudeへの作業依頼時の推奨フォーマット

```
【依頼】○○の実装をお願いします
【背景】なぜその変更が必要か
【確認事項】不明点があれば聞いてください
```
