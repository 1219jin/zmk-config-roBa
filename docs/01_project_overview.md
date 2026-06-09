# roBa キーボード管理プロジェクト

> **現行バージョン：2.0.3**（OS隣接11層＋iPad専用層）。履歴は `07_version_history.md`。

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

### 大原則：上流を固定する（例外は keymap のみ）
各ファイルについて「編集してよい場所（上流）」を1つに固定し、それ以外では読むだけにする。
同じファイルを2か所から編集すると衝突（コンフリクト）の原因になる。

| 対象 | 上流（編集してよい場所） | 下流（読むだけ） |
|---|---|---|
| config/roBa.keymap | **keymap editor（軽微な修正）＋ Claude Code（複雑な変更）の2つ** | 各LLM（読むだけ） |
| docs/（ナレッジ） | ローカルclone（Claude Code） | GitHub・各LLM |
| その他（roBa_R.conf, west.yml 等） | ローカルclone（Claude Code） | GitHub |

> **keymap は唯一の例外**：軽微な修正は keymap editor で、複雑な変更は Claude Code で行う二重編集を許容する。
> ただし二重編集するからこそ、下記の安全規律を人も Claude も厳守する。

### keymap 二重編集の安全規律
- **着手前に必ず `git pull`**（editor で保存する前も、ローカルで編集する前も）
- **完了後に必ず push／保存を即実施**（差分を溜めない＝衝突しにくい）
- editor で保存しっ放し → ローカルで別編集、という状態は必ず衝突するため厳禁

### 全ファイル共通の3習慣
1. 作業前に必ず `git pull`（上流がどこでも、まずローカルを最新化）
2. 上流以外の場所では編集しない（keymap の二重編集は明示的に許容した例外）
3. 編集したら早めに push／反映（差分を溜めない＝衝突しにくい）
