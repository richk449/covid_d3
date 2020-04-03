
import requests

filename = "time_series_covid19_confirmed_global_raw.csv"
filenameOut = "time_series_covid19_confirmed_global.csv"
filePath = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


figsize = [12,8]
legendFontsize = 6
thresholdConfirmedCountry = 5000
normValueConfirmedCountry = 1000

makePlots = False
showPlots = False

if(makePlots):
    import matplotlib.pylab as pl
    import numpy as np


#===============================================================
# get latest file
#===============================================================
r = requests.get(filePath)
with open(filename, 'w') as f:
    for line in r.text:
        f.write(line)

#===============================================================
# load in data file
#===============================================================

countryDict = {}
regionDict = {}
with open(filename) as f:
    headers = f.readline()
    for line in f.readlines():
        line = line.replace("\"Korea, South\"", "South Korea")
        line = line.replace("\"Bonaire, Sint Eustatius and Saba\"", "Sint Eustatius and Saba Bonaire")
        data = line.strip().split(",")
        if(data[0] != ""):
            name = "_".join(data[0:2])
            regionDict[name] = [int(x) for x in data[4:]]
        else:
            name = data[1]
            countryDict[name] = [int(x) for x in data[4:]]
            
        
        
#===============================================================
# do some cleanup to make countries for those that don't have them
#===============================================================
for name in regionDict:
    
    if((name.split("_")[1] in countryDict) == False):
        if(name.split("_")[1]+"*" in countryDict):
            for i in range(len(countryDict[name.split("_")[1]+"*"])):
                countryDict[name.split("_")[1]+"*"][i] = countryDict[name.split("_")[1]+"*"][i] + regionDict[name][i]
        else:
            countryDict[name.split("_")[1]+"*"] = regionDict[name]
            print("creating ", name.split("_")[1], " from subregions")

#===============================================================
# write out data file
#===============================================================
with open(filenameOut,'w') as f:
    f.write(headers)
    for name in countryDict:
        output = "{},{},{},{}".format("",name, 0.0, 0.0)
        for value in countryDict[name]:
            output = output + ",{}".format(value)
        output = output + "\n"
        f.write(output)

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
