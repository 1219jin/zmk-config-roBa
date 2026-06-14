# キーマップ改善リスト

> 実装の正は GitHub。バージョンごとの節目は `07_version_history.md` を参照。ここは「これからやること／観察中」を管理。

## 実装済み ✅（要点のみ・詳細は 07_version_history.md）

### 2.0 系（2026-06-08〜）
- OS隣接11層へ再編＋ **iPad専用層**（default_ipad / window_ipad）＋ Globeマクロ9種【2.0.0】
- **Del 復元**（window_win/mac/ipad の pos28）【2.0.1】
- **Alt+F4** 直キー無効化＋ X+C+V コンボ化（window_win限定）【2.0.1】
- **F6-F10** を nav で左シフト＋ **F7-F10 コンボ**（num_sym：R+T/F+G/Y+U/H+J）【2.0.1】
- bluetooth フォールバックを **H/J/K = Win/Mac/iPad** に統一【2.0.2】
- **AML参照漏れ修正**：trackball_listener(roBa_R.overlay) の旧mouse層4→8（クリック不動の解消）【2.0.3】
- **ESCコンボをベース6層(0-5)限定化**：num_sym作業中のF10コンボ(17+18)との誤爆解消【2026-06-14】
- **num_sym層にF2/F4コンボ追加**：左手下段 22+23 / 24+25（Excel多用・F7-F10と同レイヤーに集約）【2026-06-14】

### 1.0 系（〜2026-06-07）
- 大改修（num_sym統合・nav/window分割・9層・escape/close_win/close_macコンボ・5方向スナップ・=バグ修正・ampコンボ）【1.4.0】
- AML誤爆対策（MOVEMENT_THRESHOLD 0→5）・arrowのブラウザ/タブ操作【1.3.0】
- JIS直接キー化・Mac透過方式・idle/quick-tap調整【1.2.0】
- マルチOS対応（sw_win/mac/ipad・有線切替）【1.1.0】／ v0.3-branch固定【1.0.0】

---

## 要観察・要検証 🔬（2.0系の実装に伴う宿題）

### 誤爆観察中（隣接キーコンボ）
- **alt_f4（X+C+V）**：隣接3キー。レイヤー不慣れ期の誤爆を承知で採用。誤爆が出たら非隣接へ再設計。
- **F7-F10（R+T / F+G / Y+U / H+J）**：num_sym限定・idle150ms付き。特に右手側（Y+U、H+J）は数字打鍵との干渉に注意。
- いずれも `require-prior-idle-ms` / `timeout-ms` の調整、または位置変更で対処可能。

### 実機確認したい
- **globe_ctrl_left/right**（Globe+Ctrl+矢印のタイル）：3要素マクロ。動かなければ単キー版へ差し替え。
- **絵文字（Globe単押し）**：iPad設定により「絵文字」か「入力ソース切替」か変わる。想定と違えば iPad 側設定で調整。
- **番号振り直しの整合**：scroll(9)のKホールド、bluetooth(10)の3キー同時押しが正しく動くか（mouse(8)のAMLクリックは2.0.3で修正済み）。

---

## 未実装・優先度中 🟡

### iPad スクリーンショットキー
**現状：** default_ipad の pos15（Mac版のスクショ位置）は &trans。
**候補：** iPadのハードウェアキーボード用スクショ操作を確認のうえ配置。

### ⑤ window/nav 下段の編集キー活用
**候補：** Undo/Redo/保存/検索/全選択（`LC(Z)`/`LC(Y)`/`LC(S)`/`LC(F)`/`LC(A)`）。
**注意：** 「文書編集」でありウィンドウ操作とは別コンセプト。window でなく **nav 側**に置くのが筋。

### ⑩ default_mac の Mac固有キー拡充
**候補：** `LG(SPACE)`（Spotlight）/ `LC(SPACE)`（入力ソース切替）。default_ipad にも横展開可。

### iPad スクリーンショットキー（継続）
**現状：** default_ipad の pos15 は &trans のまま。iPadのハードウェアキーボード用スクショを確認のうえ配置。

---

## 未実装・優先度低 ⚪

### snipeトグル（精密マウスモード）保留
`CONFIG_PMW3610_SNIPE_CPI` 等によるスナイプモード（一時的に低CPI）。図面・微調整操作の頻度を見て将来検討。不採用ではなく保留。

### ⑦ Caps Word の検討
**現状：** `CAPSLOCK`（トグル）は配置済み。`caps_word`（次の単語だけ大文字・自動解除）とは別物。
**残：** snake_case／定数入力で使い分けるか置換を検討。

### ⑱ window_mac / window_ipad の右親指キー見直し
**候補：** `RIGHT_ALT`（Right Option）等。

---

## 見送り決定 ❌

### ⑥ hold-trigger-key-positions
**理由：** 左手Shift（Z位置のみ）の使い方と相容れない。左手大文字が打てなくなる。

### ⑲ 閉じたタブを再開
**決定（2026-06-07）：** 普段使わないため課題から削除。新規タブ（Win=LC(T)/Mac=LG(T)）は実装済み。

### ⑪ mouse層へのMB4/MB5追加
**決定（2026-06-14）：** 却下。戻る操作はコンボ Alt_Left（key-positions 17+18 = &mkp MB4）で充足済み。MB5（進む）は使用頻度が低く不要と判断。

### 大西配列(Fish keyboard)由来バックログ ㉑〜㉔
**決定（2026-06-14）：** 却下。大西配列の考え方はroBaに合わないと判断。
num_sym右手は電卓配置（テンキー7-9/4-6/0-3＋四則演算＋=.）として既に完成・洗練済みのため変更しない。
- ㉑ 比較演算子クラスタ `< = >`
- ㉒ num_sym右手ホームロウの演算子置換
- ㉓ 文末句読点クラスタ
- ㉔ `_`配置改善

---

## 補足：keymap-editor 経由の編集について
- 微調整は keymap-editor でも可。記号は **直接キーコード**で統一（`JP_*` 不使用）。
- `=` のように生コードを誤ると JIS で別記号が出るため、JIS対応表（05）で必ず確認すること。
