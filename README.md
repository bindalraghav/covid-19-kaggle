# covid-19-kaggle

    Disclaimer: The sole pupose of this work is only educational. 
    These scripts doesn't provide any authentic data and must not to be used for any medical diagnosis purpose.
    
    Authors:
        Manoj Goyal - (manojgoyal04@gmail.com)
        Raghav Bindlish - (bindalraghav10@gmail.com)

# Coronavirus disease (COVID-19) Pandemic Trend Anaylsis 

    The main purpose of creating this script is to visualize the pandemic covid-19 and it's effects. It can be used by resource persons to get valuables insights and to build upon it.

## Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. 


    I did my best to follow a comprehensive, but not exhaustive, analysis of the data. I'm far from reporting a rigorous study in this kernel, but I hope that it can be useful for the community, so I'm sharing how I applied some of those data analysis principles to this problem. I will also be doing visualisations using  plotly, matplotlib from which we are gonna get valuable insights. 


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
