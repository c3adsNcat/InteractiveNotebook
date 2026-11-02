"""
Tools for MATH 131 Project 3: From Rates to Totals.
Students do NOT need to open or edit this file. Installed with the math_interactive package (InteractiveNotebook repo).
"""
import numpy as np
import matplotlib.pyplot as plt


SCENARIOS = {
    "example":   dict(name="⚡ Power used by a campus building", t=np.arange(6, 19),
                      rate=[120, 160, 210, 250, 280, 300, 305, 300, 285, 255, 215, 170, 130],
                      t_label="hour of the day (6 = 6 am, 18 = 6 pm)", rate_label="power used (kW)", total_unit="kWh"),
    "solar":     dict(name="☀️ Solar panels on a house (sunny day)", t=np.arange(6, 19),
                      rate=[0.0, 1.4, 3.1, 4.3, 5.1, 5.7, 6.0, 5.9, 5.2, 4.1, 2.9, 1.6, 0.1],
                      t_label="hour of the day (6 = 6 am, 18 = 6 pm)", rate_label="power produced (kW)", total_unit="kWh"),
    "parking":   dict(name="🚗 Cars entering a campus parking deck", t=np.arange(7, 20),
                      rate=[120, 310, 420, 380, 300, 260, 240, 220, 180, 150, 110, 80, 50],
                      t_label="hour of the day (7 = 7 am, 19 = 7 pm)", rate_label="cars per hour", total_unit="cars"),
    "streaming": dict(name="📺 Streaming a 2-hour movie in HD", t=np.arange(0, 121, 10),
                      rate=[18, 24, 26, 25, 27, 26, 24, 25, 27, 26, 25, 23, 20],
                      t_label="minutes into the movie", rate_label="data rate (MB per minute)", total_unit="MB"),
    "walk":      dict(name="🚶 A 1-hour walk (fitness watch)", t=np.arange(0, 61, 5),
                      rate=[60, 95, 110, 115, 118, 116, 117, 114, 112, 105, 98, 80, 50],
                      t_label="minutes into the walk", rate_label="steps per minute", total_unit="steps"),
}

def load_scenario(key):
    if key not in SCENARIOS:
        raise ValueError('scenario must be one of: "solar", "parking", "streaming", "walk"')
    s = SCENARIOS[key]
    return np.array(s["t"], dtype=float), np.array(s["rate"], dtype=float), s

def _style(info, title):
    plt.xlabel(info["t_label"]); plt.ylabel(info["rate_label"]); plt.title(title); plt.grid(alpha=0.3)

def show_data(t, rate, info):
    plt.figure(figsize=(8, 3.4)); plt.plot(t, rate, "o-"); plt.fill_between(t, 0, rate, alpha=0.15)
    _style(info, info["name"]); plt.ylim(bottom=0); plt.show()

def show_riemann(t, rate, info, left, right):
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.4), sharey=True)
    w = t[1] - t[0]
    for ax, kind, val, col in [(axs[0], "Left", left, "tab:blue"), (axs[1], "Right", right, "tab:green")]:
        h = rate[:-1] if kind == "Left" else rate[1:]
        ax.bar(t[:-1], h, width=w, align="edge", alpha=0.3, color=col, edgecolor=col)
        ax.plot(t, rate, "o-", color="tab:orange"); ax.set_title(f"{kind} sum = {val:,.1f} {info['total_unit']}")
        ax.set_xlabel(info["t_label"]); ax.grid(alpha=0.3)
    axs[0].set_ylabel(info["rate_label"]); plt.show()

def show_model(t, rate, coeffs, info):
    ts = np.linspace(t[0], t[-1], 300)
    plt.figure(figsize=(8, 3.4)); plt.plot(t, rate, "o", label="data"); plt.plot(ts, np.polyval(coeffs, ts), label="quadratic model")
    a, b, c = coeffs; _style(info, f"model: r(t) = {a:.4f}t² + {b:.3f}t + {c:.2f}"); plt.legend(); plt.show()

def show_ftc(t, coeffs, F, total, info):
    ts = np.linspace(t[0], t[-1], 300)
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.4))
    axs[0].plot(ts, np.polyval(coeffs, ts), color="tab:orange"); axs[0].fill_between(ts, 0, np.polyval(coeffs, ts), color="tab:orange", alpha=0.2)
    axs[0].set_title(f"area = {total:,.1f} {info['total_unit']}"); axs[0].set_xlabel(info["t_label"]); axs[0].set_ylabel(info["rate_label"])
    axs[1].plot(ts, F(ts) - F(t[0]), color="tab:blue"); axs[1].set_title("running total  F(t) − F(start)")
    axs[1].set_xlabel(info["t_label"]); axs[1].set_ylabel(info["total_unit"])
    for ax in axs: ax.grid(alpha=0.3)
    plt.show()

def show_viral(A_v, k, T, total, label="views per hour"):
    ts = np.linspace(0, T, 300); ys = A_v * np.exp(k * ts)
    plt.figure(figsize=(8, 3.4)); plt.plot(ts, ys, color="tab:purple"); plt.fill_between(ts, 0, ys, color="tab:purple", alpha=0.15)
    plt.xlabel("hours after posting"); plt.ylabel(label); plt.title(f"total = {total:,.0f}"); plt.grid(alpha=0.3); plt.show()
    check = np.sum(A_v * np.exp(k * np.linspace(0, T, 100000, endpoint=False))) * (T / 100000)
    print(f"Check with 100,000 tiny rectangles: {check:,.0f}")


def show_compare(left_sum, right_sum, total_FTC, rate, dt, info):
    labels = ["left sum", "right sum", "FTC (model)"]
    values = [left_sum, right_sum, total_FTC]
    plt.figure(figsize=(7, 3.4)); plt.bar(labels, values, color=["tab:blue", "tab:green", "tab:orange"])
    for i, v in enumerate(values): plt.text(i, v, f"{v:,.1f}", ha="center", va="bottom")
    plt.ylabel(info["total_unit"]); plt.title(info["name"]); plt.show()
    print(f"first rate = {rate[0]},  last rate = {rate[-1]},  dt = {dt}")
    print(f"right - left = {right_sum - left_sum:,.2f}   and   (last - first) * dt = {(rate[-1] - rate[0]) * dt:,.2f}")
