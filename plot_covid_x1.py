import matplotlib.pylab as pl
import numpy as np
filename = "time_series_covid19_confirmed_global.csv"

figsize = [12,8]
legendFontsize = 6
thresholdConfirmedCountry = 5000
normValueConfirmedCountry = 1000

makePlots = False
showPlots = False

#===============================================================
# load in data file
#===============================================================

countryDict = {}
regionDict = {}
with open(filename) as f:
    headers = f.readline()
    for line in f.readlines():
        data = line.strip().split(",")
        if(data[0] != ""):
            name = "_".join(data[0:2])
            regionDict[name] = np.array([int(x) for x in data[4:]])
        else:
            name = data[1]
            countryDict[name] = np.array([int(x) for x in data[4:]])
            
            
#===============================================================
# do some cleanup to make countries for those that don't have them
#===============================================================
for name in regionDict:
    
    if((name.split("_")[1] in countryDict) == False):
        if(name.split("_")[1]+"*" in countryDict):
            countryDict[name.split("_")[1]+"*"] = countryDict[name.split("_")[1]+"*"] + regionDict[name]
        else:
            countryDict[name.split("_")[1]+"*"] = regionDict[name]
            print("creating ", name.split("_")[1], " from subregions")


#===============================================================
# plot
#===============================================================
if(makePlots):
    figCountry = pl.figure(figsize=figsize)
    axCountry = figCountry.add_subplot(1,2,1)
    axCountryNorm = figCountry.add_subplot(1,2,2)

    maxNormDays = 0.0
    maxVal = 0.0
    for name in countryDict:
        if(max(countryDict[name]) > thresholdConfirmedCountry):
            days = list(range(len(countryDict[name])))
            axCountry.semilogy(countryDict[name], label=name)
            
            indexNorm = np.argmin(abs(countryDict[name] - normValueConfirmedCountry))
            normDays = days - indexNorm
            axCountryNorm.semilogy(normDays, countryDict[name], label=name)

            maxNormDays = max(maxNormDays, max(normDays))
            maxVal = max(maxVal, max(countryDict[name]))
            
    axCountry.legend(fontsize=legendFontsize)
    axCountry.set_xlabel("Absolute Days")
    axCountry.set_ylabel("Confirmed Cases")
    axCountry.grid(True)

    axCountryNorm.legend(fontsize=legendFontsize)
    axCountryNorm.set_xlabel("Normalized Days")
    axCountryNorm.set_ylabel("Confirmed Cases")

    axCountryNorm.set_xlim([0, 1.1*maxNormDays])
    axCountryNorm.set_ylim([normValueConfirmedCountry, 1.1*maxVal])
    axCountryNorm.grid(True)

    figCountry.savefig("confirmed_country.png")

    if(showPlots):
        pl.show()
