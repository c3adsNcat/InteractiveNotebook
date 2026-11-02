"""
Tools for MATH 104 Project 3: My City in Data.
Students do NOT need to open this file. Installed with the math_interactive package.
"""
import numpy as np
import matplotlib.pyplot as plt


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months = np.arange(1, 13)                      # 1 = January, ..., 12 = December
x_smooth = np.linspace(1, 12, 200)

# Example + comparison city: Marquette, Michigan. Average daily HIGH temperature (°F), NOAA 1991-2020 normals
CMP_NAME = "Marquette, MI"
CMP_LAT, CMP_LON = 46.5, -87.4
cmp_temps = np.array([24.6, 26.9, 35.3, 45.8, 58.7, 67.9, 74.6, 74.3, 67.3, 53.9, 40.6, 30.2])
lat2, lon2 = np.radians(CMP_LAT), np.radians(CMP_LON)   # Marquette in radians (used in Task 5)

def month_name(x):
    return MONTH_NAMES[(int(round(x)) - 1) % 12]

def _style(title, ylabel="average high (°F)"):
    plt.xticks(months, MONTH_NAMES); plt.ylabel(ylabel); plt.title(title); plt.grid(alpha=0.3)

def show_city(temps, name):
    plt.figure(figsize=(8, 3.3)); plt.plot(months, temps, "o-", label=name)
    _style(f"{name}: average high temperature by month"); plt.legend(); plt.show()

def show_model(temps, A, B, C, D, name):
    plt.figure(figsize=(8, 3.3)); plt.plot(months, temps, "o", label="data")
    plt.plot(x_smooth, A * np.sin(B * (x_smooth - C)) + D, label="sine model")
    plt.axhline(D, ls="--", color="gray", label="midline D")
    _style(f"{name}: y = {A:.1f} sin({B:.3f}(x - {C})) + {D:.1f}"); plt.legend(); plt.show()

def show_errors(errors, name, mae):
    plt.figure(figsize=(8, 3)); plt.bar(MONTH_NAMES, errors, color=["tab:green" if e >= 0 else "tab:orange" for e in errors])
    plt.axhline(0, color="black", lw=1); plt.ylabel("error (°F)"); plt.title(f"{name}: errors (average size = {mae:.2f} °F)"); plt.show()

def show_target(A, B, C, D, target, m_warm, m_cool, name):
    plt.figure(figsize=(8, 3.3)); plt.plot(x_smooth, A * np.sin(B * (x_smooth - C)) + D, label="sine model")
    plt.axhline(target, ls="--", color="tab:blue", label=f"target = {target} °F")
    for m in (m_warm, m_cool): plt.plot(m if m >= 0.5 else m + 12, target, "ko")
    _style(f"{name}: reaches {target} °F in {month_name(m_warm)}, drops below in {month_name(m_cool)}"); plt.legend(); plt.show()

def show_map(lat, lon, name, miles):
    plt.figure(figsize=(8, 4)); plt.plot([lon, CMP_LON], [lat, CMP_LAT], "--", color="gray")
    plt.plot(CMP_LON, CMP_LAT, "o", color="tab:orange", ms=10, label=CMP_NAME)
    plt.plot(lon, lat, "o", color="tab:blue", ms=10, label=name)
    plt.axhline(0, color="tab:red", lw=0.8); plt.axvline(0, color="tab:green", lw=0.8)
    plt.xlim(-180, 180); plt.ylim(-90, 90); plt.xlabel("longitude (°)"); plt.ylabel("latitude (°)")
    plt.title(f"About {miles:,.0f} miles apart"); plt.legend(loc="lower left"); plt.grid(alpha=0.3); plt.show()


def show_compare(temps, A, B, C, D, name):
    """Task 6: plot the student's city against Marquette and print both amplitudes and midlines."""
    A_m = (cmp_temps.max() - cmp_temps.min()) / 2
    D_m = (cmp_temps.max() + cmp_temps.min()) / 2
    C_m = np.argmax(cmp_temps) + 1 - 3
    plt.figure(figsize=(8, 3.6))
    plt.plot(months, cmp_temps, "o", color="tab:orange")
    plt.plot(x_smooth, A_m * np.sin(B * (x_smooth - C_m)) + D_m, color="tab:orange", label=f"{CMP_NAME} (A = {A_m:.1f} °F)")
    plt.plot(months, temps, "o", color="tab:blue")
    plt.plot(x_smooth, A * np.sin(B * (x_smooth - C)) + D, color="tab:blue", label=f"{name} (A = {A:.1f} °F)")
    _style(f"My city vs. {CMP_NAME}"); plt.legend(); plt.show()
    print(f"Amplitude: {name} = {A:.1f} °F,  Marquette = {A_m:.1f} °F")
    print(f"Midline:   {name} = {D:.1f} °F,  Marquette = {D_m:.1f} °F")
