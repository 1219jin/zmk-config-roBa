# roBa キーボード管理プロジェクト

## リポジトリ
https://github.com/1219jin/zmk-config-roBa

## 基本情報
- キーボード：roBa（左右分割・トラックボール付き・ロータリーエンコーダー付き）
- マイコン：Seeeduino XIAO BLE
- ファームウェア：ZMK（v0.3-branchに固定）
- トラックボールドライバー：kumamuk-git/zmk-pmw3610-driver（mainブランチ）
- ビルド：GitHub Actions（自動）

## 重要制約（変更禁止）
config/west.yml の revision 設定：
- zmk → v0.3-branch（mainにすると壊れる）
- zmk-pmw3610-driver → main

## west.yml 正しい状態
```yaml
- name: zmk
  remote: zmkfirmware
  revision: v0.3-branch

- name: zmk-pmw3610-driver
  remote: kumamuk-git
  revision: main
```

## 使用環境
- メイン：Windows（有線 / BT0）
- サブ：Mac（有線 / BT1）
- サブ：iPad（BT2）
- 日本語入力：OSはJIS設定のまま使用（keymapでJP_定義を使用）
- Mac/iPad日本語入力：英数/かなキーで切り替え（LANG1/LANG2）

## BetterSnapTool設定（Mac）
| 動作 | ショートカット |
|---|---|
| 最大化 | Ctrl+Option+↑ |
| 左半分 | Ctrl+Option+← |
| 右半分 | Ctrl+Option+→ |
| 元に戻す | Ctrl+Option+↓ |

## ファームウェア保管場所
~/Documents/roBa/firmware/
命名規則：YYYYMMDD_roBa_L.uf2 / YYYYMMDD_roBa_R.uf2

---

## 情報管理のグランドルール

roBaに関する全情報（ナレッジ・keymap・各種設定）は以下の原則で管理する。

### 大原則：1ファイル＝1つの上流（編集場所）
各ファイルについて「編集してよい場所（上流）」を1つに固定し、それ以外では読むだけにする。
同じファイルを2か所から編集すると衝突（コンフリクト）の原因になる。

| 対象 | 上流（ここだけで編集） | 下流（読むだけ） |
|---|---|---|
| config/roBa.keymap | keymap editor（GitHub側） | ローカル・各LLM |
| docs/（ナレッジ） | ローカルclone（Claude Code） | GitHub・各LLM |
| その他（roBa_R.conf, west.yml 等） | ローカルclone（Claude Code） | GitHub |

> 例外は keymap editor で編集する keymap だけ。それ以外は全部ローカルが上流。

### 全ファイル共通の3習慣
1. 作業前に必ず `git pull`（上流がどこでも、まずローカルを最新化）
2. 1ファイル＝1つの上流（決めた場所以外で編集しない）
3. 編集したら早めに push／反映（差分を溜めない＝衝突しにくい）

> ルールは情報の種類ごとに違うのではなく「どれも pull→編集→push。編集場所が違うだけ」。
