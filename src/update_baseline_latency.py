"""
update_baseline_latency.py
Tạo lại baseline_latency.png với dữ liệu mới nhất
và cập nhật output của cell baseline_chart trong notebook 06_baseline.ipynb
"""

import json
import base64
import io
import os
import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

BASE = Path(__file__).parent.parent

# ── 1. Load dữ liệu ─────────────────────────────────────────────────────────
df_bl = pd.read_csv(BASE / "results" / "baseline_summary.csv")

# Latency by topic
lat_by_topic = (
    df_bl.groupby("topic")["avg_latency_total"]
    .agg(["mean", "min", "max", "std", "count"])
    .round(4)
)
lat_by_topic.columns = ["mean", "min", "max", "std", "count"]

# Pub / Hid latency by topic
lat_detail = df_bl.groupby("topic")[["pub_latency", "hid_latency", "avg_latency_total"]].mean().round(4)

overall_avg = round(df_bl["avg_latency_total"].mean(), 4)
n_pass      = int(df_bl["baseline_ok"].sum())
n_total     = len(df_bl)

print("=== BASELINE LATENCY BY TOPIC ===")
print(lat_by_topic.to_string())
print()
print("Pub/Hid detail:")
print(lat_detail.to_string())
print()
print(f"Overall avg: {overall_avg}s  |  Pass: {n_pass}/{n_total}")

# ── 2. Vẽ biểu đồ ────────────────────────────────────────────────────────────
topics   = ["list", "math", "string"]
colors   = {"list": "#5C9BD1", "math": "#E55B5B", "string": "#3CB371"}
t_labels = ["List", "Math", "String"]

avg_vals = [lat_by_topic.loc[t, "mean"] for t in topics]
min_vals = [lat_by_topic.loc[t, "min"]  for t in topics]
max_vals = [lat_by_topic.loc[t, "max"]  for t in topics]
std_vals = [lat_by_topic.loc[t, "std"]  for t in topics]
pub_vals = [lat_detail.loc[t, "pub_latency"] for t in topics]
hid_vals = [lat_detail.loc[t, "hid_latency"] for t in topics]

fig = plt.figure(figsize=(16, 6), dpi=130)
fig.suptitle("Baseline Analysis — Latency theo Chủ đề Bài toán", fontsize=13, fontweight="bold", y=1.01)

# ── Subplot 1: Scatter plot latency từng task ─────────────────────────────
ax1 = fig.add_subplot(1, 3, 1)
for t, c, label in zip(topics, [colors[t] for t in topics], t_labels):
    sub = df_bl[df_bl["topic"] == t]
    ax1.scatter(sub["task_id"], sub["avg_latency_total"],
                color=c, alpha=0.75, s=40, label=label, zorder=3)
ax1.axhline(overall_avg, color="black", linestyle="--", linewidth=1.3,
            label=f"TB: {overall_avg}s", zorder=2)
ax1.set_title("Latency Code Chuẩn theo Task ID", fontsize=10, fontweight="bold", pad=8)
ax1.set_xlabel("Task ID", fontsize=9)
ax1.set_ylabel("Latency trung bình (s)", fontsize=9)
ax1.legend(loc="upper right", fontsize=8)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.2, linestyle="--")

# ── Subplot 2: TB latency theo chủ đề (bar + error bar) ──────────────────
ax2 = fig.add_subplot(1, 3, 2)
x = np.arange(len(topics))
bar_colors = [colors[t] for t in topics]
bars = ax2.bar(x, avg_vals, color=bar_colors, width=0.45, alpha=0.85,
               edgecolor="white", linewidth=0.8, zorder=3)
ax2.errorbar(x, avg_vals, yerr=std_vals,
             fmt="none", color="black", capsize=5, linewidth=1.5, zorder=4)
for bar, v in zip(bars, avg_vals):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             v + max(avg_vals) * 0.015,
             f"{v:.4f}s",
             ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax2.set_title("Latency TB theo Chủ đề (± std)", fontsize=10, fontweight="bold", pad=8)
ax2.set_xlabel("Chủ đề bài toán", fontsize=9)
ax2.set_ylabel("Latency trung bình (s)", fontsize=9)
ax2.set_xticks(x)
ax2.set_xticklabels(t_labels, fontsize=9)
ax2.set_ylim(0, max(max_vals) * 1.30)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", alpha=0.2, linestyle="--")

# ── Subplot 3: Pub vs Hid latency per topic ───────────────────────────────
ax3 = fig.add_subplot(1, 3, 3)
w = 0.30
b_pub = ax3.bar(x - w / 2, pub_vals, w, color=bar_colors, alpha=0.90,
                edgecolor="white", label="Public tests")
b_hid = ax3.bar(x + w / 2, hid_vals, w, color=bar_colors, alpha=0.45,
                edgecolor=[colors[t] for t in topics], linewidth=1.2,
                label="Hidden tests")
for bars_g, vals in [(b_pub, pub_vals), (b_hid, hid_vals)]:
    for bar, v in zip(bars_g, vals):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 v + max(max(pub_vals), max(hid_vals)) * 0.012,
                 f"{v:.4f}",
                 ha="center", va="bottom", fontsize=7.5, fontweight="bold")

import matplotlib.patches as mpatches
pub_patch = mpatches.Patch(color="grey", alpha=0.90, label="Public tests")
hid_patch = mpatches.Patch(color="grey", alpha=0.45, label="Hidden tests")
ax3.legend(handles=[pub_patch, hid_patch], fontsize=8.5, loc="upper right")
ax3.set_title("Public vs Hidden Latency (s/test)", fontsize=10, fontweight="bold", pad=8)
ax3.set_xlabel("Chủ đề bài toán", fontsize=9)
ax3.set_ylabel("Latency (s)", fontsize=9)
ax3.set_xticks(x)
ax3.set_xticklabels(t_labels, fontsize=9)
ax3.set_ylim(0, max(max(pub_vals), max(hid_vals)) * 1.32)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.grid(axis="y", alpha=0.2, linestyle="--")

plt.tight_layout()

# ── 3. Lưu PNG ra results/ ───────────────────────────────────────────────────
out_png = BASE / "results" / "baseline_latency.png"
plt.savefig(out_png, dpi=130, bbox_inches="tight")
print(f"[OK] Lưu PNG: {out_png}")

# ── 4. Encode PNG sang base64 để nhúng vào notebook ─────────────────────────
buf = io.BytesIO()
plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
buf.seek(0)
b64_img = base64.b64encode(buf.read()).decode("ascii")
plt.close()

# ── 5. Cập nhật output của cell "baseline_chart" trong notebook ──────────────
nb_path = BASE / "notebookes" / "06_baseline.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Tìm cell baseline_latency_topic để cập nhật output bảng latency by topic
topic_table_lines = [
    "Latency theo chủ đề bài toán:\n",
    f"        Trung bình (s)  Min (s)  Max (s)  Std (s)\n",
    f"topic                                            \n",
]
for t in topics:
    row = lat_by_topic.loc[t]
    topic_table_lines.append(
        f"{t:<10}      {row['mean']:.4f}   {row['min']:.4f}   {row['max']:.4f}   {row['std']:.4f}\n"
    )

# Tìm cell baseline_chart và cập nhật output (ảnh)
updated_chart = False
updated_topic = False

for cell in nb["cells"]:
    cid = cell.get("id", "")

    if cid == "baseline_latency_topic":
        cell["outputs"] = [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": ["Latency theo chủ đề bài toán:\n"]
            },
            {
                "data": {
                    "text/plain": [
                        f"        Trung bình (s)  Min (s)  Max (s)  Std (s)\n",
                        f"topic                                            \n",
                    ] + [
                        f"{t:<10}      {lat_by_topic.loc[t, 'mean']:.4f}   "
                        f"{lat_by_topic.loc[t, 'min']:.4f}   "
                        f"{lat_by_topic.loc[t, 'max']:.4f}   "
                        f"{lat_by_topic.loc[t, 'std']:.4f}\n"
                        for t in topics
                    ]
                },
                "metadata": {},
                "output_type": "display_data"
            }
        ]
        cell["execution_count"] = 5
        updated_topic = True
        print("[OK] Cập nhật output cell: baseline_latency_topic")

    elif cid == "baseline_chart":
        cell["outputs"] = [
            {
                "data": {
                    "image/png": b64_img,
                    "text/plain": ["<Figure size 2080x780 with 3 Axes>"]
                },
                "metadata": {},
                "output_type": "display_data"
            }
        ]
        cell["execution_count"] = 6
        updated_chart = True
        print("[OK] Cập nhật output cell: baseline_chart")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

if updated_chart:
    print("[OK] Đã ghi notebook:", nb_path)
else:
    print("[WARN] Không tìm thấy cell 'baseline_chart' trong notebook!")

if not updated_topic:
    print("[WARN] Không tìm thấy cell 'baseline_latency_topic' trong notebook!")
