import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt

T = Table.read("../data/lab_demos.csv")


T2 = T[(T["architecture"] == "Lyot") | (T["architecture"] == "Hybrid Lyot")]
T3 = T2[T2["bw [%]"] == 10]
fig = plt.figure(figsize=(10, 4))
plt.title("Broadband contrast lab demos -- simulated monolith")
plt.plot(T3["publication year"], T3["avg contrast"], "b-s", label="(Hybrid) Lyot")

T2 = T[(T["architecture"] == "Vortex 4") & (T["pupil"] == "clear")]
T3 = T2[T2["bw [%]"] == 10]
plt.plot(T3["publication year"], T3["avg contrast"], "g-o", label="Vortex (charge 4)")

T2 = T[(T["architecture"] == "PIAA") | (T["architecture"] == "PIAACMC")]
# T3 = T2[(T2["bw [%]"] == 10) & (T2["pupil"] == "clear")]
T3 = T2[(T2["bw [%]"] == 10)]

plt.plot(T3["publication year"], T3["avg contrast"], "m-o", label="PIAA(CMC)")

plt.semilogy()
plt.legend()
plt.axhline(y=1e-10, ls=":", color="k")
plt.ylim(8e-11, 5e-6)
plt.xlabel("Publication Year")
plt.ylabel("Average contrast")
plt.savefig("monolith_demo_progress.png")
