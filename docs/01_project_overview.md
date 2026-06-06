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
