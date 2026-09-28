"""Publication figures for the Batteries manuscript.

Model figures are re-plotted from the result CSVs produced by ../../batt/figures.py
(no re-simulation). The Geant4 validation figure uses the numbers of the workstation
validation run (report/VALIDATION.md, Livermore physics, scale 1.0), transcribed below.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle, Circle
import numpy as np
import pandas as pd

import os
MODEL = Path(os.environ.get("EDET_MODEL", "~/electrode_detectability")).expanduser()  # model code + out/ CSVs from figures.py
sys.path.insert(0, str(MODEL))
from materials import CONTAMINANTS, ELECTRODES  # noqa: E402
from model import System  # noqa: E402
from spectrum import energy_grid, w_spectrum  # noqa: E402
from xsec import mu_rho_mix  # noqa: E402

RES = MODEL / "out"
FIG = Path(__file__).resolve().parents[1] / "figs"; FIG.mkdir(exist_ok=True)
ELS = list(ELECTRODES)
LAB = {el: el.replace(" | ", "/") for el in ELS}
COL = {"Fe": "#2a78d6", "SS316": "#eb6834", "Ni": "#1baf7a", "Cu": "#eda100", "Zn": "#e87ba4", "Al": "#008300"}
MK = {"Fe": "o", "SS316": "s", "Ni": "^", "Cu": "D", "Zn": "v", "Al": "P"}
ELCOL = {"Graphite | Cu": "#2a78d6", "NMC811 | Al": "#eb6834", "LFP | Al": "#1baf7a"}
ELLS = {"Graphite | Cu": "-", "NMC811 | Al": "--", "LFP | Al": "-."}
INK, MUTED, GRID = "#1f1f1e", "#5c5b55", "#e4e2dc"
BASE = System()

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 1.4, "lines.markersize": 4,
    "legend.frameon": False, "savefig.dpi": 400, "pdf.fonttype": 42,
})


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", dpi=250)
    plt.close(fig)


def panel(ax, letter):
    ax.text(-0.02, 1.04, f"({letter})", transform=ax.transAxes, fontsize=9, fontweight="bold",
            ha="right", va="bottom", color=INK)


# ------------------------------------------------------------------ Figure 1
def fig1():
    fig = plt.figure(figsize=(6.9, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], hspace=0.42, wspace=0.28)
    a = fig.add_subplot(gs[0, :]); a.set_axis_off(); a.set_xlim(0, 100); a.set_ylim(0, 32)
    # source
    a.add_patch(Circle((5, 16), 0.9, color="#1f1f1e"))
    a.text(5, 11.5, "W focal spot\n(FWHM f)", ha="center", va="top", fontsize=7, color=INK)
    # cone
    a.add_patch(Polygon([[5.6, 16], [93, 29], [93, 3]], closed=True, color="#86b6ef", alpha=0.25, lw=0))
    # sheet (magnified schematic)
    x0 = 38
    a.add_patch(Rectangle((x0 - 1.6, 6), 1.3, 20, color="#9a9a93"))        # coating
    a.add_patch(Rectangle((x0 - 0.3, 6), 0.6, 20, color="#c77c2c"))        # foil
    a.add_patch(Rectangle((x0 + 0.3, 6), 1.3, 20, color="#9a9a93"))        # coating
    a.add_patch(Circle((x0 - 0.95, 16.8), 0.85, color="#184f95"))
    a.annotate("metallic particle\n(sphere, diameter d)", xy=(x0 - 1.4, 17.4), xytext=(17, 27),
               fontsize=7, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    a.annotate("coating", xy=(x0 - 1.0, 8.5), xytext=(24, 8.0), fontsize=7, color=INK,
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    a.annotate("current-collector foil", xy=(x0, 9), xytext=(45, 4.0), fontsize=7, color=INK,
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    # detector
    for i in range(14):
        a.add_patch(Rectangle((93, 3 + i * 26 / 14), 1.6, 26 / 14 * 0.9, color="#3987e5" if 6 <= i <= 7 else "#b7d3f6"))
    a.text(96.2, 16, "flat-panel\ndetector\n(pixel p)", ha="left", va="center", fontsize=7, color=INK)
    # distances
    a.add_patch(FancyArrowPatch((5, 1.2), (x0, 1.2), arrowstyle="<->", mutation_scale=7, color=MUTED, lw=0.7))
    a.text((5 + x0) / 2, 1.8, "SOD", ha="center", va="bottom", fontsize=7, color=INK)
    a.add_patch(FancyArrowPatch((5, -1.2), (93, -1.2), arrowstyle="<->", mutation_scale=7, color=MUTED, lw=0.7))
    a.text(49, -0.8, "SDD      (M = SDD/SOD)", ha="center", va="bottom", fontsize=7, color=INK)
    a.set_ylim(-2.5, 32)
    panel(a, "a")

    b = fig.add_subplot(gs[1, 0])
    blues = ["#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
    for kv, c in zip((30, 40, 60, 80, 100, 140), blues):
        E = energy_grid(kv, dE=0.5)
        I = min(BASE.power_W / kv, BASE.i_max_mA)
        s = w_spectrum(kv, E, BASE.takeoff_deg, BASE.be_mm) * I
        b.plot(E, s / 1e3, color=c, lw=1.1, label=f"{kv} kV")
    b.set(xlabel="Photon energy (keV)", ylabel="Fluence at 1 m\n(10$^3$ mm$^{-2}$ s$^{-1}$ keV$^{-1}$)", xlim=(0, 142))
    b.legend(ncol=2, loc="upper right")
    panel(b, "b")

    c = fig.add_subplot(gs[1, 1])
    E = np.arange(5, 150.5, 0.5)
    for el in ELS:
        e = ELECTRODES[el]
        mu = (mu_rho_mix(e.coating, E) * e.coating_density * e.coating_um_total * 1e-4 +
              mu_rho_mix(e.foil, E) * e.foil_density * e.foil_um * 1e-4)
        c.plot(E, np.exp(-mu), color=ELCOL[el], ls=ELLS[el], label=LAB[el])
    c.set(xlabel="Photon energy (keV)", ylabel="Sheet transmission", xscale="log", ylim=(0, 1.02))
    c.set_xticks([5, 10, 20, 50, 100, 150]); c.set_xticklabels(["5", "10", "20", "50", "100", "150"])
    c.legend(loc="lower right")
    panel(c, "c")
    save(fig, "fig1_geometry_spectra")


# ------------------------------------------------------------------ Figure 2
def fig2():
    E = np.arange(10, 150.5, 0.5)
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.5), sharey=True)
    for i, (a, el) in enumerate(zip(ax, ELS)):
        e = ELECTRODES[el]
        mu_c = mu_rho_mix(e.coating, E) * e.coating_density
        for cn, (mf, rho) in CONTAMINANTS.items():
            dmu = mu_rho_mix(mf, E) * rho - mu_c
            neg = dmu < 0
            a.plot(E, np.where(neg, np.nan, dmu), color=COL[cn], label=cn, lw=1.2)
            if neg.any():
                a.plot(E, np.where(neg, -dmu, np.nan), color=COL[cn], lw=1.2, ls="--")
        a.set(xscale="log", yscale="log", title=LAB[el], xlabel="Photon energy (keV)", ylim=(0.05, 3e3))
        a.set_xticks([10, 20, 50, 100]); a.set_xticklabels(["10", "20", "50", "100"])
        panel(a, "abc"[i])
    ax[0].set_ylabel(r"$|\Delta\mu|$ (cm$^{-1}$)")
    ax[2].legend(ncol=2, loc="upper right")
    fig.tight_layout()
    save(fig, "fig2_contrast_vs_energy")


# ------------------------------------------------------------------ Figure 3
def fig3():
    df = pd.read_csv(RES / "kv_sweep.csv")
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.6), sharey=True)
    for i, (a, el) in enumerate(zip(ax, ELS)):
        sub = df[(df.electrode == el)]
        for cn in ("Fe", "SS316", "Cu", "Al"):
            s = sub[(sub.contaminant == cn) & np.isfinite(sub.d_min) & (sub.d_min < 999)]
            a.plot(s.kvp, s.d_min, color=COL[cn], marker=MK[cn], label=cn, ms=3.5)
        a.set(title=LAB[el], xlabel="Tube voltage (kV)", yscale="log", ylim=(15, 1100))
        a.set_yticks([20, 50, 100, 200, 500, 1000]); a.set_yticklabels(["20", "50", "100", "200", "500", "1000"])
        panel(a, "abc"[i])
    ax[0].set_ylabel(r"$d_{\min}$ ($\mu$m)")
    ax[0].legend(loc="upper left")
    fig.tight_layout()
    save(fig, "fig3_dmin_vs_kv")


# ------------------------------------------------------------------ Figure 4
def fig4():
    dm = pd.read_csv(RES / "matrix.csv")
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.3), sharey=True)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "b", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
    titles = {"CsI": "CsI (energy integrating)", "CdTe-20": "CdTe PCD, 20 keV threshold",
              "CdTe-10": "CdTe PCD, 10 keV threshold"}
    cons = list(CONTAMINANTS)
    for i, (a, det) in enumerate(zip(ax, ("CsI", "CdTe-20", "CdTe-10"))):
        sub = dm[dm.detector == det]
        M = np.array([[sub[(sub.electrode == el) & (sub.contaminant == c)].d_min.values[0] for c in cons] for el in ELS])
        K = np.array([[sub[(sub.electrode == el) & (sub.contaminant == c)].kv_opt.values[0] for c in cons] for el in ELS])
        a.imshow(np.log10(M), cmap=cmap, vmin=np.log10(15), vmax=np.log10(250), aspect="auto")
        a.grid(False)
        a.set_xticks(range(len(cons))); a.set_xticklabels(cons, fontsize=6.8)
        a.set_yticks(range(len(ELS))); a.set_yticklabels([LAB[e] for e in ELS])
        for r in range(len(ELS)):
            for c in range(len(cons)):
                a.text(c, r, f"{M[r, c]:.0f}\n{K[r, c]:.0f} kV", ha="center", va="center", fontsize=5.8,
                       color="white" if np.log10(M[r, c]) > 1.72 else INK)
        a.set_title(titles[det], fontsize=7.8)
        panel(a, "abc"[i])
    fig.tight_layout()
    save(fig, "fig4_dmin_matrix")


# ------------------------------------------------------------------ Figure 5
def fig5():
    dg = pd.read_csv(RES / "geometry.csv")
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.6), sharey=True)
    cols = ["#9ec5f4", "#5598e7", "#256abf", "#0d366b"]
    for i, (a, el) in enumerate(zip(ax, ELS)):
        for f, c in zip((5, 10, 20, 50), cols):
            s = dg[(dg.electrode == el) & (dg.focal == f)]
            a.plot(s.M, s.d_min, color=c, marker="o", ms=3, label=f"{f} µm / {f} W")
        a.set(title=LAB[el], xlabel="Magnification M", yscale="log", xscale="log")
        a.set_xticks([1.1, 1.5, 2, 3, 4, 6, 8]); a.set_xticklabels(["1.1", "1.5", "2", "3", "4", "6", "8"])
        a.set_yticks([10, 20, 50, 100]); a.set_yticklabels(["10", "20", "50", "100"])
        panel(a, "abc"[i])
    ax[0].set_ylabel(r"Fe $d_{\min}$ ($\mu$m)")
    ax[0].legend(title="focal spot / power", title_fontsize=6.5, fontsize=6.5, loc="upper right")
    fig.tight_layout()
    save(fig, "fig5_geometry_tradeoff")


# ------------------------------------------------------------------ Figure 6
def fig6():
    dx = pd.read_csv(RES / "exposure.csv")
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.6), sharey=True)
    for i, (a, el) in enumerate(zip(ax, ELS)):
        for cn in ("Fe", "Al"):
            for tex, ls in ((True, "-"), (False, ":")):
                s = dx[(dx.electrode == el) & (dx.contaminant == cn) & (dx.texture == tex)]
                s = s[np.isfinite(s.d_min)]
                a.plot(s.N_open, s.d_min, color=COL[cn], ls=ls, marker=MK[cn] if tex else None, ms=3.5,
                       label=f"{cn}, quantum + texture" if tex else f"{cn}, quantum only")
        a.set(title=LAB[el], xlabel="Open-beam photons per pixel", xscale="log", yscale="log")
        a.set_yticks([10, 20, 50, 100, 200]); a.set_yticklabels(["10", "20", "50", "100", "200"])
        panel(a, "abc"[i])
    ax[0].set_ylabel(r"$d_{\min}$ ($\mu$m)")
    ax[1].legend(fontsize=6.3, loc="upper right")
    fig.tight_layout()
    save(fig, "fig6_exposure_texture")


# ------------------------------------------------------------------ Figure 7 (Geant4)
# T1: (electrode, E, model mut, G4 mut, sigma)
T1 = """Graphite | Cu,15,0.54728,0.54384,0.00085
Graphite | Cu,20,0.25125,0.24987,0.00053
Graphite | Cu,30,0.08340,0.08395,0.00030
Graphite | Cu,40,0.03902,0.03909,0.00020
Graphite | Cu,60,0.01494,0.01487,0.00012
Graphite | Cu,80,0.00870,0.00856,0.00009
Graphite | Cu,100,0.00632,0.00630,0.00008
Graphite | Cu,140,0.00451,0.00462,0.00007
NMC811 | Al,15,1.61737,1.60257,0.00199
NMC811 | Al,20,0.73453,0.73716,0.00104
NMC811 | Al,30,0.23746,0.24071,0.00052
NMC811 | Al,40,0.10729,0.10779,0.00034
NMC811 | Al,60,0.03736,0.03714,0.00019
NMC811 | Al,80,0.01959,0.01943,0.00014
NMC811 | Al,100,0.01299,0.01302,0.00011
NMC811 | Al,140,0.00822,0.00809,0.00009
LFP | Al,15,0.99684,0.98768,0.00130
LFP | Al,20,0.44723,0.45009,0.00075
LFP | Al,30,0.14466,0.14677,0.00040
LFP | Al,40,0.06678,0.06699,0.00026
LFP | Al,60,0.02532,0.02500,0.00016
LFP | Al,80,0.01475,0.01471,0.00012
LFP | Al,100,0.01075,0.01080,0.00010
LFP | Al,140,0.00771,0.00756,0.00009"""
# T2: electrode, particle, kV, model peak, G4 peak, sigma, model sum, G4 sum, sigma
T2 = """Graphite | Cu,Fe 30,30,-0.1862,-0.1810,0.0044,-0.8741,-0.8621,0.0307
Graphite | Cu,Fe 30,60,-0.0559,-0.0563,0.0033,-0.2606,-0.2357,0.0201
Graphite | Cu,Fe 60,30,-0.6393,-0.6392,0.0042,-4.6449,-4.6559,0.0239
Graphite | Cu,Fe 60,60,-0.2391,-0.2385,0.0035,-1.6725,-1.6437,0.0210
Graphite | Cu,Al 60,30,-0.1100,-0.1089,0.0024,-0.7555,-0.7298,0.0156
Graphite | Cu,Al 60,60,-0.0211,-0.0204,0.0019,-0.1440,-0.1462,0.0112
NMC811 | Al,Fe 30,30,-0.1052,-0.1040,0.0064,-0.4905,-0.5278,0.0362
NMC811 | Al,Fe 30,60,-0.0300,-0.0307,0.0040,-0.1397,-0.1510,0.0250
NMC811 | Al,Fe 60,30,-0.4420,-0.4482,0.0062,-3.1050,-3.1545,0.0367
NMC811 | Al,Fe 60,60,-0.1455,-0.1538,0.0040,-0.9989,-1.0121,0.0270
NMC811 | Al,Al 60,30,0.3193,0.3227,0.0038,2.1053,2.1572,0.0221
NMC811 | Al,Al 60,60,0.0753,0.0753,0.0022,0.5023,0.4931,0.0149
LFP | Al,Fe 30,30,-0.1347,-0.1248,0.0054,-0.6288,-0.5851,0.0340
LFP | Al,Fe 30,60,-0.0416,-0.0475,0.0037,-0.1934,-0.2121,0.0226
LFP | Al,Fe 60,30,-0.5346,-0.5342,0.0051,-3.7936,-3.8022,0.0349
LFP | Al,Fe 60,60,-0.1931,-0.1905,0.0036,-1.3345,-1.3349,0.0217
LFP | Al,Al 60,30,0.0904,0.0914,0.0032,0.6047,0.6178,0.0190
LFP | Al,Al 60,60,0.0226,0.0229,0.0021,0.1518,0.1717,0.0118"""


def fig7():
    t1 = pd.DataFrame([l.split(",") for l in T1.splitlines()], columns=["el", "E", "m", "g", "s"])
    t1[["E", "m", "g", "s"]] = t1[["E", "m", "g", "s"]].astype(float)
    t2 = pd.DataFrame([l.split(",") for l in T2.splitlines()],
                      columns=["el", "p", "kv", "mp", "gp", "sp", "ms", "gs", "ss"])
    for c in ["kv", "mp", "gp", "sp", "ms", "gs", "ss"]:
        t2[c] = t2[c].astype(float)
    fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.45))
    a = ax[0]
    for k, el in enumerate(ELS):
        s = t1[t1.el == el]
        a.errorbar(s.E * (1 + 0.025 * (k - 1)), 100 * (s.g / s.m - 1), 100 * s.s / s.m, marker="o", ms=3,
                   lw=0.9, capsize=1.5, color=ELCOL[el], ls=ELLS[el], label=LAB[el])
    a.axhline(0, color=MUTED, lw=0.6)
    a.set(xscale="log", xlabel="Photon energy (keV)", ylabel=r"$\mu t$: Geant4/model $-$ 1 (%)")
    a.set_xticks([15, 20, 30, 50, 100, 140]); a.set_xticklabels(["15", "20", "30", "50", "100", "140"])
    a.legend(fontsize=6.3, loc="lower left")
    panel(a, "a")
    a = ax[1]
    lim = 0.7
    a.plot([-lim, lim], [-lim, lim], color=MUTED, lw=0.6)
    for kv, mk in ((30, "o"), (60, "s")):
        s = t2[t2.kv == kv]
        for el in ELS:
            q = s[s.el == el]
            a.errorbar(q.mp, q.gp, q.sp, fmt=mk, ms=3.2, color=ELCOL[el], lw=0.8, capsize=1,
                       label=f"{LAB[el]}, {kv:.0f} kV" if False else None)
    a.set(xlabel="Model peak-pixel contrast", ylabel="Geant4 peak-pixel contrast", xlim=(-0.7, 0.4), ylim=(-0.7, 0.4))
    a.plot([], [], "o", color=MUTED, ms=3.2, label="30 kV"); a.plot([], [], "s", color=MUTED, ms=3.2, label="60 kV")
    a.legend(fontsize=6.3, loc="upper left")
    panel(a, "b")
    a = ax[2]
    pulls = np.r_[(t2.gp - t2.mp) / t2.sp, (t2.gs - t2.ms) / t2.ss]
    bins = np.arange(-3.5, 3.51, 0.5)
    a.hist(pulls, bins=bins, color="#86b6ef", edgecolor="white", lw=0.8, label=f"36 pulls (18 cases)")
    xg = np.linspace(-3.5, 3.5, 200)
    a.plot(xg, len(pulls) * 0.5 * np.exp(-xg ** 2 / 2) / np.sqrt(2 * np.pi), color="#0d366b", lw=1.1,
           label="unit Gaussian")
    a.set(xlabel="Pull  (Geant4 − model)/σ", ylabel="Count", xlim=(-3.5, 3.5))
    a.legend(fontsize=6.3, loc="upper left")
    panel(a, "c")
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig7_geant4_validation")
    return pulls


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        f()
        print("done", f.__name__)
