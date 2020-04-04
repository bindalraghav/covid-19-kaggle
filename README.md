# covid-19-kaggle

Disclaimer: These scripts doesn't provide any authentic data and must not to be used for any medical diagnosis purpose.

# Coronavirus disease (COVID-19) Pandemic 

## Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. 

I did my best to follow a comprehensive, but not exhaustive, analysis of the data. I'm far from reporting a rigorous study in this kernel, but I hope that it can be useful for the community, so I'm sharing how I applied some of those data analysis principles to this problem. I will also be doing visualisations using  plotly, matplotlib from which we are gonna get valuable insights. 

## The main purpose of creating this notebook is to visualize the pandemic covid-19 and it's effects. It can be used by resource persons to get valuables insights and to build upon it.

```.
├── README.md
├── covid_trend_analysis.py
├── install.sh
└── kaggle.json
```

## First time, please run: 
    bash install.sh
 to install requisite python3 packages.

## To visualize Covid-19 following trends please run 
    ./covid_trend_analysis.py
1. Active corona cases across the world
2. Reoprted deaths caused due to corona across the world
3. Reoprted recovered corona cases across the world

## How it works:
1. This script pulls "COVID-19 Complete Dataset" from https://www.kaggle.com/imdevskp/corona-virus-report
2. Dataset is updated after every 24 hours
3. Analyse and visaulize trends
