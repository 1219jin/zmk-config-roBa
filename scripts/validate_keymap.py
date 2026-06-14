#!/usr/bin/env python3
"""roBa keymap 構造検証スクリプト（CI lint用）。
検証項目:
  1. 全レイヤーのキー数が物理レイアウト数と一致するか
  2. {} と <> のバランス
  3. レイヤー参照（&lt/&mo/&to/&tog_off/layers/#define MOUSE/scroll-layers 等）が
     実在レイヤー範囲内か、かつ MOUSE/scroll の #define が実インデックスと一致するか
  4. keymap本体に JP_* 定義が混入していないか（keymap-drawer失敗の予防）
終了コード: 問題なし=0 / 問題あり=1
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYMAP = ROOT / "config" / "roBa.keymap"
DTSI = ROOT / "boards" / "shields" / "roBa" / "roBa.dtsi"

# レイヤー名（keymap内の出現順＝インデックス）
LAYER_NAMES = [
    "default_win", "window_win", "default_mac", "window_mac",
    "default_ipad", "window_ipad", "num_sym", "nav",
    "mouse", "scroll", "bluetooth",
]

errors, warnings = [], []
src = KEYMAP.read_text()

# --- 物理キー数 ---
phys = DTSI.read_text().count("key_physical_attrs")

# --- 各レイヤーの bindings を抽出してキー数カウント ---
def extract_bindings(name):
    m = re.search(rf"\b{name}\s*\{{", src)
    if not m:
        return None
    b = src.index("bindings = <", m.end())
    end = src.index(">", b)
    body = src[b + len("bindings = <"):end]
    return len(re.findall(r"&\w+", body))

print(f"物理レイアウトキー数: {phys}")
print("-" * 48)
counts = {}
for name in LAYER_NAMES:
    c = extract_bindings(name)
    if c is None:
        errors.append(f"レイヤー '{name}' が見つからない")
        continue
    counts[name] = c
    status = "OK" if c == phys else "NG"
    if c != phys:
        errors.append(f"レイヤー '{name}' のキー数 {c} != 物理 {phys}")
    print(f"  [{status}] {name:14s} : {c} keys")

# --- ブレースバランス ---
for op, cl, label in [("{", "}", "{}"), ("<", ">", "<>")]:
    if src.count(op) != src.count(cl):
        errors.append(f"{label} の対応が不一致（{op}={src.count(op)} {cl}={src.count(cl)}）")

# --- レイヤー参照監査 ---
maxidx = len(LAYER_NAMES) - 1
refs = []
for pat in [r"&lt\s+(\d+)", r"&mo\s+(\d+)", r"&to\s+(\d+)",
            r"&tog_off\s+(\d+)", r"scroll-layers\s*=\s*<\s*(\d+)",
            r"zip_temp_layer\s+(\d+)"]:
    refs += [int(x) for x in re.findall(pat, src)]
for grp in re.findall(r"layers\s*=\s*<([\d\s]+)>", src):
    refs += [int(x) for x in grp.split()]
bad = sorted({n for n in refs if not (0 <= n <= maxidx)})
if bad:
    errors.append(f"範囲外のレイヤー参照: {bad}（有効範囲 0..{maxidx}）")

# #define MOUSE / scroll-layers が実インデックスと一致するか
m = re.search(r"#define\s+MOUSE\s+(\d+)", src)
if m and int(m.group(1)) != LAYER_NAMES.index("mouse"):
    errors.append(f"#define MOUSE {m.group(1)} != 実mouse index {LAYER_NAMES.index('mouse')}")
m = re.search(r"scroll-layers\s*=\s*<\s*(\d+)", src)
if m and int(m.group(1)) != LAYER_NAMES.index("scroll"):
    errors.append(f"scroll-layers <{m.group(1)}> != 実scroll index {LAYER_NAMES.index('scroll')}")

# --- JP_* 混入チェック ---
if re.search(r"&kp\s+JP_", src):
    warnings.append("keymap本体に JP_* 定義が混入（keymap-drawer失敗の恐れ）")

# --- 結果 ---
print("-" * 48)
for w in warnings:
    print(f"WARN: {w}")
if errors:
    for e in errors:
        print(f"ERROR: {e}")
    print(f"\n検証失敗: {len(errors)} 件のエラー")
    sys.exit(1)
print("検証成功: 全レイヤー整合・参照健全")
sys.exit(0)
