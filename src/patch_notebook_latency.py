"""
patch_notebook_latency.py
Thêm cell so sánh latency vào cuối notebook 06_baseline_v3.ipynb
"""
import json
import os
from pathlib import Path

BASE = Path(__file__).parent.parent
NB_PATH = BASE / "notebookes" / "06_baseline_v3.ipynb"

# ── Markdown cell (tiêu đề) ───────────────────────────────────────────────────
md_cell = {
    "cell_type": "markdown",
    "id": "latency_title",
    "metadata": {},
    "source": [
        "---\n",
        "## So sánh Latency theo các bộ test (Set 1 → Set 4)\n",
        "\n",
        "Phân tích thời gian chấm bài thực tế trên **50 submissions** với 4 cấu hình:\n",
        "- **Set 1** — 3 public tests\n",
        "- **Set 2** — 3 public + 6 hidden = 9 tests\n",
        "- **Set 3** — 3 public + 6–10 hidden = 13 tests (Full-run)\n",
        "- **Set 4** — Set 3 + **Fail-Fast** (dừng sớm khi gặp lỗi đầu tiên)\n"
    ]
}

# ── Code cell chính ───────────────────────────────────────────────────────────
code_lines = [
    "import json\n",
    "import os\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.patches as mpatches\n",
    "import numpy as np\n",
    "from pathlib import Path\n",
    "\n",
    "# ── 1. Resolve BASE path ────────────────────────────────────────────────────\n",
    "cwd = os.getcwd()\n",
    "if os.path.basename(cwd) in ['notebookes', 'src', 'data', 'results']:\n",
    "    BASE = Path(cwd).parent\n",
    "else:\n",
    "    BASE = Path(cwd)\n",
    "\n",
    "# ── 2. Load comparison_week4.json ──────────────────────────────────────────\n",
    "comp_path = BASE / 'results' / 'comparison_week4.json'\n",
    "with open(comp_path, encoding='utf-8') as f:\n",
    "    comp = json.load(f)\n",
    "stats = comp['stats']\n",
    "\n",
    "SETS   = ['Set 1\\n(3 tests)', 'Set 2\\n(9 tests)', 'Set 3\\n(13 tests)', 'Set 4\\n(13+FF)']\n",
    "KEYS   = ['set1', 'set2', 'set3', 'set4']\n",
    "COLORS = ['#5C9BD1', '#F29C38', '#3CB371', '#E55B5B']\n",
    "\n",
    "avg_test = [stats[k]['avg_latency_test_ms']  for k in KEYS]\n",
    "avg_sub  = [stats[k]['avg_latency_sub_ms']   for k in KEYS]\n",
    "p95_sub  = [stats[k]['p95_latency_sub_ms']   for k in KEYS]\n",
    "total_s  = [stats[k]['total_latency_sub_s']  for k in KEYS]\n",
    "\n",
    "# ── 3. Bảng tóm tắt ────────────────────────────────────────────────────────\n",
    "df_lat = pd.DataFrame({\n",
    "    'Bộ test'             : ['Set 1 (3t)', 'Set 2 (9t)', 'Set 3 (13t)', 'Set 4 (13t+FF)'],\n",
    "    'TB/test (ms)'        : avg_test,\n",
    "    'TB/submission (ms)'  : avg_sub,\n",
    "    'P95/submission (ms)' : p95_sub,\n",
    "    'Tổng 50 bài nộp (s)' : total_s,\n",
    "})\n",
    "print('=' * 72)\n",
    "print('  SO SÁNH LATENCY THEO CÁC BỘ TEST CASES (50 submissions)')\n",
    "print('=' * 72)\n",
    "print(df_lat.to_string(index=False))\n",
    "\n",
    "speedup_total = total_s[2] / total_s[3]\n",
    "speedup_p95   = p95_sub[2]  / p95_sub[3]\n",
    "print(f\"\"\"\n",
    "  ✓ Fail-Fast (Set 4) nhanh hơn Full-run (Set 3):\n",
    "     • Tổng thời gian chấm : {speedup_total:.2f}x  ({total_s[2]:.3f}s → {total_s[3]:.3f}s)\n",
    "     • Độ trễ P95/bài nộp : {speedup_p95:.2f}x  ({p95_sub[2]:.1f}ms → {p95_sub[3]:.1f}ms)\n",
    "\"\"\")\n",
    "\n",
    "# ── 4. Vẽ 3 biểu đồ ────────────────────────────────────────────────────────\n",
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), dpi=130)\n",
    "fig.suptitle('So sánh Latency theo các Bộ Test (50 submissions)',\n",
    "             fontsize=13, fontweight='bold', y=1.02)\n",
    "\n",
    "def style(ax):\n",
    "    ax.spines['top'].set_visible(False)\n",
    "    ax.spines['right'].set_visible(False)\n",
    "    ax.spines['left'].set_alpha(0.3)\n",
    "    ax.spines['bottom'].set_alpha(0.3)\n",
    "    ax.grid(axis='y', alpha=0.2, linestyle='--')\n",
    "\n",
    "def add_bar_labels(ax, bars, fmt='{:.1f}', suffix=''):\n",
    "    for bar in bars:\n",
    "        h = bar.get_height()\n",
    "        ax.text(bar.get_x() + bar.get_width() / 2,\n",
    "                h + max(h * 0.02, 0.5),\n",
    "                fmt.format(h) + suffix,\n",
    "                ha='center', va='bottom', fontsize=8.5, fontweight='bold')\n",
    "\n",
    "# ── Subplot 1: TB latency / test (ms) ──────────────────────────────────────\n",
    "ax1 = axes[0]\n",
    "b1 = ax1.bar(SETS, avg_test, color=COLORS, width=0.5, edgecolor='white', linewidth=0.8)\n",
    "add_bar_labels(ax1, b1, fmt='{:.1f}', suffix=' ms')\n",
    "ax1.set_title('Latency TB / test case (ms)', fontsize=10, fontweight='bold', pad=10)\n",
    "ax1.set_ylabel('ms / test', fontsize=9)\n",
    "ax1.set_ylim(0, max(avg_test) * 1.28)\n",
    "ax1.tick_params(axis='x', labelsize=8)\n",
    "style(ax1)\n",
    "\n",
    "# ── Subplot 2: TB & P95 latency / submission (ms) ──────────────────────────\n",
    "ax2 = axes[1]\n",
    "x = np.arange(len(SETS))\n",
    "w = 0.35\n",
    "b_avg = ax2.bar(x - w / 2, avg_sub, w, color=COLORS, alpha=0.85, edgecolor='white')\n",
    "b_p95 = ax2.bar(x + w / 2, p95_sub, w, color=COLORS, alpha=0.40,\n",
    "                edgecolor=[c for c in COLORS], linewidth=1.2)\n",
    "add_bar_labels(ax2, b_avg, fmt='{:.0f}', suffix=' ms')\n",
    "add_bar_labels(ax2, b_p95, fmt='{:.0f}', suffix=' ms')\n",
    "ax2.set_title('Latency TB & P95 / submission (ms)', fontsize=10, fontweight='bold', pad=10)\n",
    "ax2.set_ylabel('ms / submission', fontsize=9)\n",
    "ax2.set_ylim(0, max(p95_sub) * 1.32)\n",
    "ax2.set_xticks(x)\n",
    "ax2.set_xticklabels(SETS, fontsize=8)\n",
    "ax2.annotate(\n",
    "    f'P95: {speedup_p95:.1f}x\\nnhanh hơn',\n",
    "    xy=(x[3] + w / 2, p95_sub[3]),\n",
    "    xytext=(x[3] + w / 2 + 0.05, p95_sub[3] + max(p95_sub) * 0.20),\n",
    "    arrowprops=dict(arrowstyle='->', color='#C82323', lw=1.5),\n",
    "    fontsize=8.5, color='#C82323', fontweight='bold', ha='center'\n",
    ")\n",
    "avg_patch = mpatches.Patch(color='grey', alpha=0.85, label='TB / bài nộp')\n",
    "p95_patch = mpatches.Patch(color='grey', alpha=0.40, label='P95 / bài nộp')\n",
    "ax2.legend(handles=[avg_patch, p95_patch], fontsize=8.5, loc='upper left')\n",
    "style(ax2)\n",
    "\n",
    "# ── Subplot 3: Tổng thời gian chấm 100 submissions (s) ──────────────────────\n",
    "ax3 = axes[2]\n",
    "b3 = ax3.bar(SETS, total_s, color=COLORS, width=0.5, edgecolor='white', linewidth=0.8)\n",
    "add_bar_labels(ax3, b3, fmt='{:.3f}', suffix=' s')\n",
    "ax3.set_title('Tổng thời gian chấm 50 bài nộp (s)', fontsize=10, fontweight='bold', pad=10)\n",
    "ax3.set_ylabel('Giây (s)', fontsize=9)\n",
    "ax3.set_ylim(0, max(total_s) * 1.28)\n",
    "ax3.tick_params(axis='x', labelsize=8)\n",
    "ax3.text(3, total_s[3] + max(total_s) * 0.07,\n",
    "         f'↑ {speedup_total:.1f}x nhanh hơn\\nso với Set 3',\n",
    "         ha='center', va='bottom', fontsize=8.5, color='#C82323', fontweight='bold',\n",
    "         bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3CD',\n",
    "                   alpha=0.9, edgecolor='#F29C38'))\n",
    "style(ax3)\n",
    "\n",
    "plt.tight_layout()\n",
    "out_path = BASE / 'results' / 'baseline_latency_sets.png'\n",
    "plt.savefig(out_path, dpi=130, bbox_inches='tight')\n",
    "plt.show()\n",
    "print(f'✓ Đã lưu biểu đồ: {out_path}')\n"
]

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "latency_comparison",
    "metadata": {},
    "outputs": [],
    "source": code_lines
}

# ── Đọc notebook hiện tại ─────────────────────────────────────────────────────
with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ── Xóa các cell latency cũ nếu đã tồn tại (idempotent) ─────────────────────
nb["cells"] = [c for c in nb["cells"] if c.get("id") not in ("latency_title", "latency_comparison")]

# ── Thêm 2 cell mới vào cuối ──────────────────────────────────────────────────
nb["cells"].append(md_cell)
nb["cells"].append(code_cell)

# ── Ghi lại notebook ──────────────────────────────────────────────────────────
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"[OK] Đã thêm cell so sánh latency vào: {NB_PATH}")
print(f"     Tổng số cell: {len(nb['cells'])}")
