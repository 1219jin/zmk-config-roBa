# バージョン履歴

> roBa キーマップのバージョンと特徴を記録する。**コミットの正は GitHub。** ここは「節目と狙い」を残す台帳。
> 付番ルール：**メジャー＝レイヤー構造の作り替え**、マイナー＝機能追加・再編、パッチ＝小修正。
> 現行：**2.0.3**

---

## 2.0 系（OS隣接11層 ＋ iPad専用層）

「今回の大幅な改修」以降。レイヤーをOS単位でペア隣接させ、iPad専用の操作層を新設した世代。

### 2.0.3（2026-06-08）AML参照漏れ修正（マウスクリック不動）
- **不具合**：AML（オートマウス）でレイヤーには入るがクリックが効かない。
- **原因**：2.0.0 の番号再編で `boards/shields/roBa/roBa_R.overlay` の `trackball_listener` の AML参照が旧 mouse層 `4` のまま残存。再編後 4 は default_ipad のため、AML が誤った層へ移行していた。
- **修正**：`roBa_R.overlay` の `input-processors = <&zip_temp_layer 4 ...>` を `8`（現 mouse 層）に。
- **教訓**：AML temp-layer 参照は **keymap（mkp_input_listener）と overlay（trackball_listener）の2か所**にある。番号変更時は両方を更新する。
- commit: `2e9629e`（fix: AML layer reference 4->8 in trackball_listener）

### 2.0.2（2026-06-08）bluetooth フォールバック整理
- bluetooth層の手動切替を **H/J/K = Win/Mac/iPad** に統一（上段 Y/U/I と同並び）。
- 有線Macの層フォールバック（J=&to 2）を残しつつ iPad（K=&to 4）を確保。
- commit: `refactor: bluetooth layer fallback keys to H/J/K ...`

### 2.0.1（2026-06-08）Windows操作強化・F系整理
- **Del 復元**：window_win/mac/ipad の Backspace位置（pos28）に Delete。
- **Alt+F4**：直キー無効化＋ **X+C+V コンボ**化（window_win限定）。
- **F6-F10**：nav の F6-F10 を左に1つシフト（F10をエンコーダ隣 pos15→pos14）。
- **F7-F10 コンボ**（num_sym限定）：F7=R+T / F8=F+G / F9=Y+U / F10=H+J。
- F10=H+J(17,18) と Alt_Left(MB4) の競合回避で Alt_Left を layers=<0 1 2 3 4 5> に限定。
- commit: `feat: iPad layer fallback, Alt+F4 combo, Delete restore, F6-F10 reorg with combos`

### 2.0.0（2026-06-08）OS隣接11層 ＋ iPad専用層　★メジャー
- レイヤーを **0 win / 1 window_win / 2 mac / 3 window_mac / 4 ipad / 5 window_ipad / 6 num_sym / 7 nav / 8 mouse / 9 scroll / 10 bluetooth** に再編。
- iPad専用層 **default_ipad / window_ipad** を新設。window_ipad は **Globeベース**操作（Exposé・タイル・アプリ切替・全画面・Dock・通知・絵文字＝Globe単押し）。
- **Globeマクロ9種**追加（macro_press/tap/release、v0.3-branchで利用可確認）。
- 番号移動（mouse4→8 / scroll5→9 / bluetooth6→10 / num_sym7→6 / nav8→7）に伴う全参照更新。sw_ipad は &to 4（default_ipad）へ。
- backup: `backup/20260608-before-reorder`
- commit: `feat: reorder layers (OS-paired) and add iPad dedicated layers`

---

## 1.0 系（〜2026-06-07）

OS隣接化・iPad専用層の前まで。マルチOS対応と機能再編で実用構成を確立した世代。

### 1.4.0（2026-06-07）機能再編 大改修
- SYMBOL＋NUM を **num_sym**（左手記号・右手電卓）に統合。
- ARROW/ARROW_MAC を **nav**（矢印・F）＋ **window_win/window_mac**（ウィンドウ・タブ・ブラウザ）に再編。9層構成。
- escape / close_win / close_mac コンボ追加。window_mac に5方向スナップ。
- num_sym の `=` バグ修正（JISで`~`が出る `LS(EQUAL)`→`LS(MINUS)`）、`*` 復活、`&`を amp コンボへ。
- backup: `backup/20260607-before-redesign`（commit `1c8e5de`）／凍結 `roBa_keymap_20260607_baseline.keymap`
- commit: `467f40a` 他

### 1.3.0（2026-06-04）トラックボール誤爆対策・ブラウザ操作
- AML誤起動対策：`CONFIG_PMW3610_MOVEMENT_THRESHOLD` 0→5（roBa_R.conf）。commit `5ec03f1`。
- arrow_win/arrow_mac にタブ移動・PageUp/Down・ブラウザ戻る/進む・新規タブを追加。commit `83cc2a8` / `35df8ff`。

### 1.2.0（2026-05-06）安定化・JIS整備
- `require-prior-idle-ms` / `quick-tap-ms` 調整、Mac を &trans 透過方式に変更、レイヤー再構成。
- JIS記号を直接キーコード化（`JP_*` define 廃止）。commit `852f871` / `565bc73` / `9952d4f` / `94a5882`。

### 1.1.0（2026-05-04）マルチOS対応
- Mac/iPad対応、BT＋レイヤー同時切替マクロ（sw_win/sw_mac/sw_ipad）、有線手動切替。commit `ae4e67d` 他。

### 1.0.0（2026-05-04）初期安定版
- ZMK **v0.3-branch** に固定。基本キーマップ確立。`INTERNATIONAL_2`→`INT_HENKAN` 等の移行。

---

## 付番の運用メモ
- 新しい節目を切ったら、このファイルの先頭「現行」を更新し、該当系列に追記する。
- コミットメッセージの英語タイトル＋日本語説明（05参照）と対応づける。ハッシュの正は GitHub。
