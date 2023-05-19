import uproot
import hist
import mplhep as hep
import matplotlib.pyplot as plt

file = uproot.open("histograms.root")
file.classnames()
data = file['4j1b_data'].to_hist()
ttbar = file['4j1b_ttbar'].to_hist()
wjets = file['4j1b_wjets'].to_hist()
bklabels = ["ee-signal","ttjets-background"]

hep.style.use("CMS")
hep.cms.label("open data",data=True, lumi=2.3, year=2015)
hep.histplot(data,histtype="errorbar", color='k', capsize=4, label="Data")
hep.histplot([ttbar, wjets],stack=True, histtype='fill', label=bklabels, sort='yield')
plt.legend(frameon=False)
plt.xlabel("$H_{T}$ [Gev]");
plt.savefig('finalplotdatav2.png')
plt.show()
