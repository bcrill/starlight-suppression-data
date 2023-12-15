import matplotlib.pyplot as plt
from astropy.table import Table
import numpy as np
from matplotlib.ticker import ScalarFormatter

version = "2023.12.14"
output_plot_file = f"Contrast_lab_demos_{version}.png"
output_readme_file = f"README_Contrast_lab_demos_{version}.txt"


fnames = [
    "Seo_et_al_fig3_digitized.csv",
    "VVC_650nm_oneBMCDM_clearPupil.csv",
    "starshade_ms1b.csv",
    "VVC_635nm_twoAOXDMs_clearPupil_v2.csv",
    "PIAACMC_650nm_Belikov2022_BB.csv",
    "VVC_650nm_oneBMCDM_segPupil.csv",
    "PIAA_Tdem10_GuyonKern2014_BB.csv",
    "SLEEC_prelim_trial53.csv",
    "PAPLC_HiCAT.csv",
    "Roman_CGI_HLC_static_milestone9.csv",
]


# prepare readme text
readme = f"The plot {output_plot_file} shows reported lab demonstrations of starlight suppression technology.\n\n"

# prepare to collect references
references = []

# prepare to plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)

# loop over filenames
for fname in fnames:
    T = Table.read(f"../data/contrast_curves/{fname}", format="ascii.ecsv")

    if T.meta["coronagraph"] == "starshade":
        labelstr = f"{T.meta['testbed']}\n"
    else:
        labelstr = (
            f"{T.meta['testbed']} {T.meta['pupil']} pupil {T.meta['coronagraph']}\n"
        )
    labelstr += f"{T.meta['wl']}nm ({T.meta['reference']}) {T.meta['bp_pct']}% band"

    ax.plot(
        T["x"],
        T["y"],
        color=T.meta["color"],
        ls=T.meta["ls"],
        label=labelstr,
    )

    readmestr = (
        f"* {T.meta['color']} "
        + {
            "-": "solid curve",
            "--": "dashed curve",
            ":": "dotted curve",
            "-.": "dash-dot",
        }[T.meta["ls"]]
        + " : \n"
    )
    if T.meta["coronagraph"] != "starshade":
        readmestr += f"demonstration of {T.meta['coronagraph']} coronagraph with a {T.meta['pupil']} pupil "
        readmestr += f"using {T.meta['DM']} deformable mirror(s) for wavefront control "
    else:
        readmestr += f"demonstration of {T.meta['coronagraph']} "
    readmestr += (
        f"at {T.meta['wl']}nm over a {T.meta['bp_pct']}% band ({T.meta['reference']}). "
    )
    if "courtesy" in T.meta.keys():
        readmestr += "Data courtesy of " + T.meta["courtesy"] + "."
    readmestr += "\n"
    if "note" in T.meta.keys():
        readmestr += T.meta["note"] + "\n"
    readmestr += "\n"

    # add reference
    if "reference" in T.meta.keys():
        refstr = T.meta["reference"] + " " + T.meta["url"]
        if refstr not in references:
            references.append(refstr)
    readme += readmestr

# add version watermark
plt.text(
    0.02,
    0.01,
    f"Version {version}",
    horizontalalignment="left",
    alpha=0.5,
    fontsize=8,
    transform=plt.gca().transAxes,
)

plt.loglog()
ax.set_xlim(0.95, 50)
ax.set_ylim(0.7e-12, 4.1e-7)

ax.set_ylabel("Normalized intensity")
ax.set_xlabel("Angle [$\lambda$/D]")


ax.axhspan(1e-13, 1e-10, alpha=0.1, facecolor="k")

plt.legend(fontsize=6, loc="lower right")
# plt.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.05, 1.0))
plt.text(
    3.5,
    7e-11,
    "Contrast goal $\leq$10$^{-10}$",
    horizontalalignment="left",
    alpha=0.8,
    fontsize=8,
)
ax.axvline(x=3.0, ls="--", color="k", alpha=0.3)
plt.text(
    2.7,
    1e-9,
    "Inner working angle goal $\leq$3$\lambda$/D",
    alpha=0.9,
    fontsize=7,
    rotation="vertical",
)
ax.axvline(x=45, ls="--", color="k", alpha=0.3)
plt.text(
    41,
    1e-9,
    "Outer working angle goal $\geq$45$\lambda$/D",
    alpha=0.8,
    fontsize=7,
    rotation="vertical",
)

# convert from lambda/D to milliarcseconds on a 6 meter and 640 nm
lDtomas = 640e-9 / 6 * 180 / np.pi * 3600 * 1000


def ldtomas(x):
    return x * lDtomas


def mastold(x):
    return x / lDtomas


# Add additional axis
ax2 = ax.secondary_xaxis("top", functions=(ldtomas, mastold))
ax2.set_xlabel("Angle [mas] on a 6m telescope at 640 nm")

# Do this to get rid of exponential formatted axis labels:
for axis in [ax.xaxis, ax2.xaxis]:
    axis.set_major_formatter(ScalarFormatter())

plt.suptitle("Starlight suppression broadband lab demonstrations")
plt.tight_layout()
plt.savefig(output_plot_file)


with open(output_readme_file, "w") as f:
    f.write(readme)

    f.write("\nReferences\n")
    f.write("----------\n")
    for reference in references:
        f.write(f"* {reference}\n")
    f.write("\n")

    f.close()
