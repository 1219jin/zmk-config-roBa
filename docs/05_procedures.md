# 作業手順・バージョン管理・リファレンス

> バージョンの節目と特徴は `07_version_history.md` に記録する（現行 2.0.3）。

## コミットメッセージ規則
- タイトル：英語（`feat:` / `fix:` / `chore:` / `ci:` / `restore:` / `refactor:`）
- 説明文（Extended description）：日本語

---

## 作業前の必須手順
1. `https://github.com/1219jin/zmk-config-roBa` を開く（mainを確認）
2. **live keymap を raw から取得して現物を確認**（ナレッジのキャッシュは信用しない）
3. バックアップブランチを作成：`backup/YYYYMMDD-作業内容`
4. 大改修時は keymap 全文の凍結ファイルも別途保存しておく

> **重要な教訓：** ナレッジ（docs）と GitHub 実態は乖離し得る。実装判断は必ず live keymap を直接フェッチして行う。
> raw.githubusercontent.com は数分キャッシュされるため、push 直後の確認は codeload のtarball取得が確実。

---

## バックアップブランチ一覧

| ブランチ名 | 内容 |
|---|---|
| `backup/before-sync-20260504` | 2026/05/04 作業開始前 |
| `backup/20260504-working` | 2026/05/04 全作業完了・動作確認済み |
| `backup/20260607-before-redesign` | 2026/06/07 大改修前（commit `1c8e5de`） |
| `backup/20260608-before-reorder` | 2026/06/08 OS隣接11層＋iPad層 再編前【2.0.0】 |
| `backup/20260608-before-combos` | 2026/06/08 Del/Alt+F4/F系コンボ 前【2.0.1】 |
| `backup/20260608-before-hjk` | 2026/06/08 bluetooth H/J/K 前【2.0.2】 |

> 凍結ファイル：`roBa_keymap_20260607_baseline.keymap`（大改修前の全文）

---

## レイヤー移動トリガー（現行）

| レイヤー | 移動方法 |
|---|---|
| num_sym (6) | Spaceホールド（左親指）/ Slashホールド（右手） |
| window (1/3/5) | 変換／無変換ホールド（OS別） |
| nav (7) | TABホールド |
| scroll (9) | Kホールド |
| bluetooth (10) | 3キー同時押し（37 38 39） |
| mouse (8) | AML（トラックボール） |

---

## GitHub Actions ワークフロー

| ファイル | トリガー | 役割 |
|---|---|---|
| `lint.yml` | push / PR / 手動 | keymap構造を静的検証（キー数・ブレース・レイヤー参照・JP_*混入）。build/drawより先に構造ミスを検出 |
| `build.yml` | push（全般） | ファームウェア（uf2）ビルド |
| `draw.yml` | push to main（keymap関連変更）/ 手動 | キーマップSVG生成 → keymap-drawer/にコミット |

### キーマップ画像の自動更新
`config/roBa.keymap` / `keymap_drawer.config.yaml` / `config/roBa.dtsi` を main にpush → `draw.yml` 起動 → `keymap-drawer/roBa.svg` 再生成 → README が最新画像を表示。

---

## ファームウェア書き込み手順
1. Actions の最新 ✅ run → Artifacts → firmware をダウンロード
2. 保存：`~/Documents/roBa/firmware/` に `YYYYMMDD_roBa_L.uf2 / _R.uf2`
3. 右手リセット2回押し → USBドライブ認識 → `roBa_R-seeeduino_xiao_ble.uf2` をドラッグ
4. 左手も同様（`roBa_L-...`）
5. ZIP・元名uf2は削除、日付リネーム版のみ保管

---

## トラックボール（PMW3610）設定リファレンス
設定は `boards/shields/roBa/roBa_R.conf`（右手側）。

| 設定 | 役割 | 現行値 |
|---|---|---|
| `CONFIG_PMW3610_CPI` | 感度 | 400 |
| `CONFIG_PMW3610_AUTOMOUSE_TIMEOUT_MS` | mouse層維持時間(ms) | 700 |
| `CONFIG_PMW3610_MOVEMENT_THRESHOLD` | AML起動しきい値（大きいほど誤起動しにくい） | 5 |
| `CONFIG_PMW3610_SMART_ALGORITHM` | スムージング | y |

---

> **AMLの移行先レイヤー参照は2か所にある**（番号変更時は両方要更新）：
> - `config/roBa.keymap`：`&mkp_input_listener { input-processors = <&zip_temp_layer N ...>; }`
> - `boards/shields/roBa/roBa_R.overlay`：`trackball_listener { input-processors = <&zip_temp_layer N ...>; }`
> N は現 mouse レイヤー番号（現行 8）。片方だけだとクリックが別レイヤーに飛んで効かない（2.0.3で発生・修正）。

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| `west update failed` | west.ymlのrevision違い | zmk→`v0.3-branch`、pmw3610→`main` |
| `CMake parse error` | keymap構文エラー | 行頭の不要文字・閉じ忘れを確認 |
| `INTERNATIONAL_2`エラー | v0.3-branchで廃止 | `INT_HENKAN`に置換 |
| Draw が `Number of keys differ` | レイヤー間でキー数不一致 | 全レイヤーを43キーに揃える |
| Draw が keymap-editor 非互換で失敗 | エディタが解決できない特定コード使用 | 記号は `LS(NUMBER_n)` 等の**直接コード**に統一 |
| **`=` を押すと `~` が出る** | `LS(EQUAL)` を使用（JISでは`~`） | `=` は **`LS(MINUS)`**（直接コード） |
| AMLがタイピング中に誤起動（初回） | `MOVEMENT_THRESHOLD=0` | roBa_R.conf で `=5` 以上に |
| **AML誤起動が threshold=5 でも一文字目に再発**（J/I が打てない） | 直前キー入力なし状態でのトラボ接触（require-prior-idle-ms は効かないパターン） | `CONFIG_PMW3610_MOVEMENT_THRESHOLD` を `10` に引き上げ（残れば 12→15 と段階的に） |
| **トラボ動くがクリック効かない** | AML temp-layer 参照ずれ（overlay と keymap で不一致） | roBa_R.overlay の `trackball_listener` と keymap の `mkp_input_listener` 両方を現 mouse 層番号に揃える |

---

## キーコードリファレンス

### 日本語入力関連
| キーコード | 用途 | OS |
|---|---|---|
| `INT_HENKAN` / `INT_MUHENKAN` | 変換 / 無変換 | Windows |
| `LANG1` / `LANG2` | かな / 英数 | Mac |

> 変換/無変換はPC側でMac流英/かなにリマップ済み。tap=IME / hold=window レイヤー。

### JIS記号対応表（記号は直接コードで記述）
| 記号 | ZMKコード | 記号 | ZMKコード |
|---|---|---|---|
| `!` | `LS(NUMBER_1)` | `=` | **`LS(MINUS)`** |
| `"` | `LS(NUMBER_2)` | `~` | `LS(EQUAL)` |
| `#` | `LS(NUMBER_3)` | `+` | `LS(SEMICOLON)` |
| `$` | `LS(NUMBER_4)` | `*` | `LS(SINGLE_QUOTE)` |
| `%` | `LS(NUMBER_5)` | `:` | `SINGLE_QUOTE` |
| `&` | `LS(NUMBER_6)` | `@` | `LEFT_BRACKET` |
| `'` | `LS(NUMBER_7)` | `` ` `` | `LS(LEFT_BRACKET)` |
| `(` | `LS(NUMBER_8)` | `[` | `RIGHT_BRACKET` |
| `)` | `LS(NUMBER_9)` | `]` | `BACKSLASH` |
| `_` | `LS(INT_RO)` | `{` | `LS(RIGHT_BRACKET)` |
| `^` | `EQUAL` | `}` | `LS(BACKSLASH)` |
| `¥` | `INT_YEN` | `/` `−` `.` | `SLASH` `MINUS` `DOT/PERIOD` |

> **要注意：** `=` と `~` を取り違えやすい。`=`=`LS(MINUS)`、`~`=`LS(EQUAL)`。

### レイヤー操作
| キーコード | 説明 |
|---|---|
| `&mo N` | ホールド中だけLayer N |
| `&to N` | Layer Nに永続移動 |
| `&lt N X` | ホールドでLayer N、タップでX |
| `&trans` | 下のレイヤーに透過 |

---

## よく使うGitHub URL
| 用途 | URL |
|---|---|
| リポジトリ | https://github.com/1219jin/zmk-config-roBa |
| keymap raw | https://raw.githubusercontent.com/1219jin/zmk-config-roBa/main/config/roBa.keymap |
| 右手conf | .../blob/main/boards/shields/roBa/roBa_R.conf |
| Actions | .../actions |
| コミット履歴 | .../commits/main/config/roBa.keymap |
| ブランチ | .../branches |
| 生成SVG | .../blob/main/keymap-drawer/roBa.svg |

---

## GitHub編集（Chrome経由）
Chrome経由で編集する場合は `github-chrome-editor` スキルを参照。Claude in Chrome 未接続のセッションでは、修正版ファイルを出力してGitHubに貼り付け／Upload で対応。
