"""Insert the reference list into manuscript.tex in order of first citation (MDPI numeric style)."""
import re
from pathlib import Path

REFS = {
    "Setta2025": r"Setta, J.; Lecocq, A.; Desprez, P.; Origuchi, M.; Destriau, L.; Marlair, G.; Carlier, D.; Croguennec, L.; Bordes, A. Internal short circuits in lithium-ion batteries; origins, detection, and experimental reproduction: A review. {\em J. Power Sources} {\bf 2025}, {\em 658}, 238265. \url{https://doi.org/10.1016/j.jpowsour.2025.238265}.",
    "Mohanty2016": r"Mohanty, D.; Hockaday, E.; Li, J.; Hensley, D.K.; Daniel, C.; Wood, D.L. Effect of electrode manufacturing defects on electrochemical performance of lithium-ion batteries: Cognizance of the battery failure sources. {\em J. Power Sources} {\bf 2016}, {\em 312}, 70--79. \url{https://doi.org/10.1016/j.jpowsour.2016.02.007}.",
    "Grabow2023": r"Grabow, J.; Klink, J.; Benger, R.; Hauer, I.; Beck, H.-P. Particle Contamination in Commercial Lithium-Ion Cells---Risk Assessment with Focus on Internal Short Circuits and Replication by Currently Discussed Trigger Methods. {\em Batteries} {\bf 2023}, {\em 9}, 9. \url{https://doi.org/10.3390/batteries9010009}.",
    "Sun2022": r"Sun, Y.; Yuan, Y.; Lu, L.; Han, X.; Kong, X.; Wang, H.; Ouyang, M.; Gao, P.; Zheng, H.; Wang, K. A comprehensive research on internal short circuits caused by copper particle contaminants on cathode in lithium-ion batteries. {\em eTransportation} {\bf 2022}, {\em 13}, 100183. \url{https://doi.org/10.1016/j.etran.2022.100183}.",
    "Masuch2023": r"Masuch, S.; G\"umbel, P.; Kaden, N.; Dr\"oder, K. Applications and Development of X-ray Inspection Techniques in Battery Cell Production. {\em Processes} {\bf 2023}, {\em 11}, 10. \url{https://doi.org/10.3390/pr11010010}.",
    "Evans2023": r"Evans, D.; Luc, P.-M.; Tebruegge, C.; Kowal, J. Detection of Manufacturing Defects in Lithium-Ion Batteries---Analysis of the Potential of Computed Tomography Imaging. {\em Energies} {\bf 2023}, {\em 16}, 6958. \url{https://doi.org/10.3390/en16196958}.",
    "Bergmann2026": r"Bergmann, T.G.; Liu-Th\'eato, X.; Zhu, B.; Leuthner, L. Advanced Classification of Lithium-Ion Battery Defects Using Electrochemical Impedance Spectroscopy and Machine Learning. {\em Batteries} {\bf 2026}, {\em 12}, 228. \url{https://doi.org/10.3390/batteries12070228}.",
    "Hamamatsu2025": r"Hamamatsu Photonics. Microfocus X-ray Sources for Li-ion Batteries: High-Resolution Inspection from Cylindrical to Prismatic Cells. Available online: \url{https://www.hamamatsu.com/eu/en/news/featured-products_and_technologies/2025/microfocus-x-ray-li-ion-battery-inspection-cylindrical-prismatic-cells.html} (accessed on 28 September 2026).",
    "Stock2023": r"Stock, S.; Hagemeister, J.; Grabmann, S.; Kriegler, J.; Keilhofer, J.; Ank, M.; Dickmanns, J.L.S.; Schreiber, M.; Konwitschny, F.; Wassiliadis, N.; et~al. Cell teardown and characterization of an automotive prismatic LFP battery. {\em Electrochim. Acta} {\bf 2023}, {\em 471}, 143341. \url{https://doi.org/10.1016/j.electacta.2023.143341}.",
    "Kwade2018": r"Kwade, A.; Haselrieder, W.; Leith\"off, R.; Modlinger, A.; Dietrich, F.; Droeder, K. Current status and challenges for automotive battery production technologies. {\em Nat. Energy} {\bf 2018}, {\em 3}, 290--300. \url{https://doi.org/10.1038/s41560-018-0130-3}.",
    "Ank2023": r"Ank, M.; Sommer, A.; Abo Gamra, K.; Sch\"oberl, J.; Leeb, M.; Schachtl, J.; Streidel, N.; Stock, S.; Schreiber, M.; Bilfinger, P.; et~al. Lithium-Ion Cells in Automotive Applications: Tesla 4680 Cylindrical Cell Teardown and Characterization. {\em J. Electrochem. Soc.} {\bf 2023}, {\em 170}, 120536. \url{https://doi.org/10.1149/1945-7111/ad14d0}.",
    "Elam2002": r"Elam, W.T.; Ravel, B.D.; Sieber, J.R. A new atomic database for X-ray spectroscopic calculations. {\em Radiat. Phys. Chem.} {\bf 2002}, {\em 63}, 121--128. \url{https://doi.org/10.1016/S0969-806X(01)00227-4}.",
    "XrayDB": r"Newville, M. XrayDB: X-ray Reference Data in SQLite. Available online: \url{https://github.com/xraypy/XrayDB} (accessed on 26 September 2026).",
    "XCOM": r"Berger, M.J.; Hubbell, J.H.; Seltzer, S.M.; Chang, J.; Coursey, J.S.; Sukumar, R.; Zucker, D.S.; Olsen, K. {\em XCOM: Photon Cross Section Database (Version 1.5)}; National Institute of Standards and Technology: Gaithersburg, MD, USA, 2010. \url{https://doi.org/10.18434/T48G6X}.",
    "Birch1979": r"Birch, R.; Marshall, M. Computation of bremsstrahlung X-ray spectra and comparison with spectra measured with a Ge(Li) detector. {\em Phys. Med. Biol.} {\bf 1979}, {\em 24}, 505--517. \url{https://doi.org/10.1088/0031-9155/24/3/002}.",
    "Kramers1923": r"Kramers, H.A. On the theory of X-ray absorption and of the continuous X-ray spectrum. {\em Philos. Mag.} {\bf 1923}, {\em 46}, 836--871. \url{https://doi.org/10.1080/14786442308565244}.",
    "ESTAR": r"Berger, M.J.; Coursey, J.S.; Zucker, M.A.; Chang, J. {\em ESTAR, PSTAR, and ASTAR: Computer Programs for Calculating Stopping-Power and Range Tables for Electrons, Protons, and Helium Ions (Version 1.2.3)}; National Institute of Standards and Technology: Gaithersburg, MD, USA, 2005. \url{https://doi.org/10.18434/T4NC7P}.",
    "Attix1986": r"Attix, F.H. {\em Introduction to Radiological Physics and Radiation Dosimetry}; Wiley: New York, NY, USA, 1986.",
    "Green1961": r"Green, M.; Cosslett, V.E. The efficiency of production of characteristic X-radiation in thick targets of a pure element. {\em Proc. Phys. Soc.} {\bf 1961}, {\em 78}, 1206--1214. \url{https://doi.org/10.1088/0370-1328/78/6/315}.",
    "Poludniowski2021": r"Poludniowski, G.; Omar, A.; Bujila, R.; Andreo, P. Technical Note: SpekPy v2.0---A software toolkit for modeling x-ray tube spectra. {\em Med. Phys.} {\bf 2021}, {\em 48}, 3630--3637. \url{https://doi.org/10.1002/mp.14945}.",
    "Taguchi2013": r"Taguchi, K.; Iwanczyk, J.S. Vision 20/20: Single photon counting x-ray detectors in medical imaging. {\em Med. Phys.} {\bf 2013}, {\em 40}, 100901. \url{https://doi.org/10.1118/1.4820371}.",
    "Swank1973": r"Swank, R.K. Absorption and noise in x-ray phosphors. {\em J. Appl. Phys.} {\bf 1973}, {\em 44}, 4199--4203. \url{https://doi.org/10.1063/1.1662918}.",
    "Torquato2002": r"Torquato, S. {\em Random Heterogeneous Materials: Microstructure and Macroscopic Properties}; Springer: New York, NY, USA, 2002. \url{https://doi.org/10.1007/978-1-4757-6355-3}.",
    "Rose1948": r"Rose, A. The sensitivity performance of the human eye on an absolute scale. {\em J. Opt. Soc. Am.} {\bf 1948}, {\em 38}, 196--208. \url{https://doi.org/10.1364/JOSA.38.000196}.",
    "Burgess1999": r"Burgess, A.E. The Rose model, revisited. {\em J. Opt. Soc. Am. A} {\bf 1999}, {\em 16}, 633--646. \url{https://doi.org/10.1364/JOSAA.16.000633}.",
    "Barrett2004": r"Barrett, H.H.; Myers, K.J. {\em Foundations of Image Science}; Wiley: Hoboken, NJ, USA, 2004.",
    "Agostinelli2003": r"Agostinelli, S.; Allison, J.; Amako, K.; Apostolakis, J.; Araujo, H.; Arce, P.; Asai, M.; Axen, D.; Banerjee, S.; Barrand, G.; et~al. Geant4---A simulation toolkit. {\em Nucl. Instrum. Methods Phys. Res. A} {\bf 2003}, {\em 506}, 250--303. \url{https://doi.org/10.1016/S0168-9002(03)01368-8}.",
    "Allison2016": r"Allison, J.; Amako, K.; Apostolakis, J.; Arce, P.; Asai, M.; Aso, T.; Bagli, E.; Bagulya, A.; Banerjee, S.; Barrand, G.; et~al. Recent developments in Geant4. {\em Nucl. Instrum. Methods Phys. Res. A} {\bf 2016}, {\em 835}, 186--225. \url{https://doi.org/10.1016/j.nima.2016.06.125}.",
    "Cullen2015": r"Cullen, D.E. {\em EPICS2014: Electron Photon Interaction Cross Sections (Version 2014)}; Report IAEA-NDS-218; International Atomic Energy Agency: Vienna, Austria, 2015.",
    "UsseglioViretta2018": r"Usseglio-Viretta, F.L.E.; Colclasure, A.; Mistry, A.N.; Claver, K.P.Y.; Pouraghajan, F.; Finegan, D.P.; Heenan, T.M.M.; Abraham, D.; Mukherjee, P.P.; Wheeler, D.; et~al. Resolving the Discrepancy in Tortuosity Factor Estimation for Li-Ion Battery Electrodes through Micro-Macro Modeling and Experiment. {\em J. Electrochem. Soc.} {\bf 2018}, {\em 165}, A3403--A3426. \url{https://doi.org/10.1149/2.0731814jes}.",
    "NRELmicro": r"National Laboratory of the Rockies (formerly NREL). Battery Microstructures Library. Available online: \url{https://www.nlr.gov/transportation/microstructure} (accessed on 28 September 2026).",
}

ms = Path(__file__).with_name("manuscript.tex")
tex = ms.read_text()
body = tex.split(r"\begin{thebibliography}")[0]
order = []
for m in re.finditer(r"\\cite\{([^}]*)\}", body):
    for k in m.group(1).split(","):
        k = k.strip()
        if k not in order:
            order.append(k)
missing = [k for k in order if k not in REFS]
unused = [k for k in REFS if k not in order]
assert not missing, f"missing refs: {missing}"
items = "\n".join(f"\\bibitem{{{k}}}\n{REFS[k]}" for k in order)
tex = re.sub(r"\\begin\{thebibliography\}\{999\}.*?\\end\{thebibliography\}",
             lambda _: "\\begin{thebibliography}{999}\n" + items + "\n\\end{thebibliography}", tex, flags=re.S)
ms.write_text(tex)
print(f"{len(order)} references in citation order; unused: {unused}")
