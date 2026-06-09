# 作業完了後のナレッジ更新チェックリスト

> **2026/06/06 ナレッジ移行：** ナレッジ（01〜06）は GitHub `docs/` に移行済み。**GitHubが正（source of truth）**。
> 以下の各ファイル名（`04_improvements.md` 等）はすべて GitHub `docs/` 配下のファイルを指す。
> 更新は GitHub 側（`docs/`）で行い、Project内コピーは参照用とする。
> raw 参照例：`https://raw.githubusercontent.com/1219jin/zmk-config-roBa/main/docs/04_improvements.md`

一通りの作業が完了したら、以下を順番に確認・実施すること。

---

## 必須チェック項目

### □ 1. keymapに変更があったか？
→ YES の場合：**GitHubへのコミットが完了していることを確認する**
- プロジェクトの `03_roBa_keymap.md` は更新不要（GitHubが正）
- コミット履歴：https://github.com/1219jin/zmk-config-roBa/commits/main/config/roBa.keymap

### □ 2. 改善リストの項目を実装したか？
→ YES の場合：GitHub `docs/04_improvements.md` を更新
- 実装した項目を「未実装」から「実装済み ✅」セクションに移動
- 日付・コミットIDを記載

### □ 3. レイヤー構成やコンボに変更があったか？
→ YES の場合：GitHub `docs/02_layers.md` を更新
- レイヤー一覧・移動トリガー・差分表を修正

### □ 4. 新しいバックアップブランチを作成したか？
→ YES の場合：GitHub `docs/05_procedures.md` のバックアップブランチ一覧に追記

### □ 5. バージョンの節目を切ったか？（構造変更・機能追加）
→ YES の場合：`07_version_history.md` に追記し、先頭「現行」を更新

---

## Claudeへの依頼テンプレート

作業が完了したタイミングで以下を伝えるだけでナレッジ更新を依頼できる：
```
今回の作業が完了しました。
ナレッジファイルの更新が必要な箇所をまとめて、
更新後の各ファイルの全文を出力してください。
```

---

## ナレッジ更新フロー（★Claude Code 経由が本命）

ローカルclone（`~/Documents/roBa/zmk-config-roBa`）を Claude Code で編集 → commit → push する。

1. 設計・文章づくりが要るときは claude.ai で相談 → 固めた指示を Claude Code に渡す
2. 軽い更新は Claude Code に直接依頼してよい
3. Claude Code がローカルの `docs/` を編集 → commit → `push origin main`（ターミナルで Yes を押すだけ）
4. push 後、Gemini Gem 等が raw URL 経由で次回から最新を参照

- 環境：origin=`1219jin/zmk-config-roBa`、gh CLI（HTTPS）認証、SSH鍵は未使用
- コミット規則：英語タイトル + 日本語説明（feat/fix/chore/docs/refactor 等）

### 予備手段
- claude.ai が更新版全文を出力 → GitHubの `upload/main/docs` に同名アップロード（上書き）
- Claude in Chrome の base64注入アップロード（詳細は 05_procedures.md）
- 軽微な1〜数行は GitHub Web の Edit で直接修正

---

## ナレッジファイル一覧と役割

| ファイル名 | 役割 | 更新タイミング |
|---|---|---|
| 01_project_overview.md | 環境・制約・OS設定 | 環境・使用OS・BetterSnapTool設定変更時 |
| 02_layers.md | レイヤー設計の意図・構成説明 | レイヤー構成・コンボ変更時 |
| 03_roBa_keymap.md | GitHubへの参照URLのみ（全文は管理しない） | 基本変更不要 |
| 04_improvements.md | 未実装アイデア・改善リスト | 実装完了・新規項目追加時 |
| 05_procedures.md | 手順・リファレンス | バックアップブランチ追加時 |
| 06_post_work_checklist.md | このファイル | 基本変更不要 |
| 07_version_history.md | バージョン履歴（節目と特徴） | 節目を切った時 |

> **原則：ナレッジ（01〜06）は GitHub `docs/` が唯一の正（source of truth）。**
> 更新は GitHub `docs/`（＝ローカルclone）側で行い、Project内コピーは参照専用とする。
> 各ファイルは raw URL で参照可能（Gemini Gem 等が参照）：
> `https://raw.githubusercontent.com/1219jin/zmk-config-roBa/main/docs/<ファイル名>`
