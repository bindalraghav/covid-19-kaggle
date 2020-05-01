#! /usr/bin/env python3

# Coronavirus disease (COVID-19) Pandemic
# Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.
# I did my best to follow a comprehensive, but not exhaustive, analysis of the data. I'm far from reporting a rigorous study in this kernel, but I hope that it can be useful for the community, so I'm sharing how I applied some of those data analysis principles to this problem. I will also be doing visualizations using  plotly,matplotlib from which we are gonna get valuable insights.
# The main purpose of creating this notebook is to visualize the pandemic covid-19 and it's effects. It can be used by resource persons to get valuables insights and to build upon it.

import os
import time
import json
from warnings import simplefilter
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as plo
from plotly.subplots import make_subplots

KAGGLE_CRED_FILE = "kaggle.json"
COVID_19_INDIA_DB_FILE="covid_19_india.csv"
COVID_19_DB_FILE = "covid_19_clean_complete.csv"
INDIA_DETAILS="IndividualDetails.csv"
AGE_GROUP_DETAILS="AgeGroupDetails.csv"
DELAY = 5


class Covid19(object):
    def __init__(self, db_file):
        self.covid_19_db_file = db_file
        simplefilter(action='ignore', category=FutureWarning)

    def update_db_file(self):
        try:
            with open(KAGGLE_CRED_FILE, "r") as fout:
                data = json.load(fout)
                if data:
                    username = data["username"]
                    key = data["key"]
                    db_downlaod_cmd = f"export KAGGLE_USERNAME={username}; export KAGGLE_KEY={key};kaggle datasets download -d imdevskp/corona-virus-report"
                    os.system(db_downlaod_cmd)
                    os.system("rm -fr *.csv")
                    os.system("unzip corona-virus-report.zip")
        except ValueError:
            print("Files not found")

    def read_db_file(self):
        self.df = pd.read_csv(self.covid_19_db_file, parse_dates=['Date'])
        self.df.head()

    def describe_db(self):
        self.df.describe(include='object')
        self.df.head()

    def data_start_date(self):
        return self.df.Date.value_counts().sort_index().index[0]

    def data_last_date(self):
        print(self.df.Date.value_counts().sort_index().index[-1])

    def rename_coloumns(self):
        # Renaming the coulmns
        self.df.rename(columns={'Date': 'date',
                                'Province/State': 'state',
                                'Country/Region': 'country',
                                'Lat': 'lat', 'Long': 'long',
                                'Confirmed': 'confirmed',
                                'Deaths': 'deaths',
                                'Recovered': 'recovered'
                                }, inplace=True)
        self.df.head()

    def get_active_cases(self):
        # Active Case = confirmed - deaths - recovered
        self.df['active'] = self.df['confirmed'] - \
            self.df['deaths'] - self.df['recovered']
        self.df.head()

    def get_active_cases_across_world(self):
        # ### Active cases around the world
        self.top = self.df[self.df['date'] == self.df['date'].max()]
        self.world = self.top.groupby('country')[
            'confirmed', 'recovered', 'deaths', 'active'].sum().reset_index()
        #print(self.world.head(50))
        
    def get_data_india(self):
        self.india =  self.df[self.df.country == 'India']
        self.india = self.india.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
        self.india = self.india.iloc[8:].reset_index().drop('index', axis = 1)
        
    def plot_active_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.active))
      fig.update_layout(title='Active Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()
        
    def plot_death_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.deaths,line=dict(color='orange', width=2)))
      fig.update_layout(title='Death Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()
        
    def plot_recovered_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.recovered, line=dict(color='firebrick', width=2)))
      fig.update_layout(title='Recovered Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()
        

        

    def get_data_india(self):
        self.india =  self.df[self.df.country == 'India']
        self.india = self.india.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
        self.india = self.india.iloc[8:].reset_index().drop('index', axis = 1)
        
    def plot_active_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.active))
      fig.update_layout(title='Active Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()
        
    def plot_death_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.deaths,line=dict(color='orange', width=2)))
      fig.update_layout(title='Death Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()
        
    def plot_recovered_cases_across_india(self):
     
      fig = go.Figure(data=go.Scatter(x=self.india.index, y=self.india.recovered, line=dict(color='firebrick', width=2)))
      fig.update_layout(title='Recovered Cases In India Over Time',
                   xaxis_title='No. Of Days',
                   yaxis_title='No. Of Cases')
      fig.show()    

    def plot_active_cases_across_world(self):
        fig = px.choropleth(self.world, locations="country",
                            locationmode='country names', color="active",
                            hover_name="country", range_color=[1, 1000],
                            color_continuous_scale="thermal",
                            title='Countries with Active Cases')
        fig.show()

    def plot_recovered_cases_across_world(self):
        self.world['size'] = self.world['recovered'].pow(0.2)
        fig = px.scatter_geo(self.world, locations="country", locationmode='country names', color="recovered",
                             hover_name="country", size="size",
                             projection="natural earth", title='Recovered count of each country')
        fig.show()

    def plot_death_cases_across_world(self):
        self.world['size'] = self.world['deaths'].pow(0.2)
        fig = px.scatter_geo(self.world, locations="country", locationmode='country names', color="deaths",
                             hover_name="country", size="size",
                             projection="natural earth", title='Death count of each country')
        fig.show()

    def plot_confirmed_cases_across_world(self):
        # ## Confirmed Cases Over Time
        plt.figure(figsize=(15, 10))
        plt.xticks(rotation=90, fontsize=10)
        plt.yticks(fontsize=15)
        plt.xlabel("Dates", fontsize=20)
        plt.ylabel('Total cases', fontsize=30)
        plt.title("Worldwide Confirmed Cases Over Time", fontsize=30)
        total_cases = self.df.groupby(
            'date')['date', 'confirmed'].sum().reset_index()
        total_cases['date'] = pd.to_datetime(total_cases['date'])

        plt.plot(total_cases.date.dt.date, total_cases.confirmed, color='r')
        plt.grid()

    def plot_top_20_countries_confirmed_cases_across_world(self):
        # ## Top 20 Countries Having Most Confirmed Cases
        top_casualities = self.top.groupby(by='country')['confirmed'].sum(
        ).sort_values(ascending=False).head(20,).reset_index()
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel("Total cases", fontsize=30)
        plt.ylabel('Country', fontsize=30)
        plt.title("Top 20 countries having most confirmed cases", fontsize=30)
        plt.barh(top_casualities.country, top_casualities.confirmed, color=[
            'indigo', 'blueviolet', 'darkorchid', 'mediumorchid', 'orchid', 'hotpink', 'violet', 'pink', 'lightpink'])
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_casualities.confirmed):
            plt.text(v + 3, i + .25, str(v),
                     color='black', fontweight='normal')
        plt.show()

    def plot_top_20_countries_active_cases_across_world(self):
        # ## Top 20 countries having most active cases
        top_actives = self.top.groupby(by='country')['active'].sum(
        ).sort_values(ascending=False).head(20).reset_index()
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel("Total cases", fontsize=30)
        plt.ylabel('Country', fontsize=30)
        plt.title("Top 20 countries having most active cases", fontsize=30)
        plt.barh(top_actives.country, top_actives.active, color=[
            'indigo', 'blueviolet', 'darkorchid', 'mediumorchid', 'orchid', 'hotpink', 'violet', 'pink', 'lightpink'])
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_actives.active):
            plt.text(v + 3, i + .25, str(v),
                     color='black', fontweight='normal')
        plt.show()

    def plot_top_20_countries_deaths_across_world(self):
        # ## Top 20 countries having most deaths
        #
        top_deaths = self.top.groupby(by='country')['deaths'].sum(
        ).sort_values(ascending=False).head(20).reset_index()
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel("Total cases", fontsize=30)
        plt.ylabel('Country', fontsize=30)
        plt.title("Top 20 countries having most deaths", fontsize=30)
        plt.barh(top_deaths.country, top_deaths.deaths, color=[
            'indigo', 'blueviolet', 'darkorchid', 'mediumorchid', 'orchid', 'hotpink', 'violet', 'pink', 'lightpink'])
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_deaths.deaths):
            plt.text(v + 3, i + .25, str(v),
                     color='black', fontweight='normal')
        plt.show()

    def plot_top_20_countries_recovered_cases_across_world(self):
        # ## Top 20 countries having most recovered cases
        top_recovered = self.top.groupby(by='country')['recovered'].sum(
        ).sort_values(ascending=False).head(20).reset_index()
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel("Total cases", fontsize=30)
        plt.ylabel('Country', fontsize=30)
        plt.title("Top 20 countries having most recovered cases", fontsize=30)
        plt.barh(top_recovered.country, top_recovered.recovered, color=[
            'indigo', 'blueviolet', 'darkorchid', 'mediumorchid', 'orchid', 'hotpink', 'violet', 'pink', 'lightpink'])
        plt.gca().invert_yaxis()
        for i, v in enumerate(top_recovered.recovered):
            plt.text(v + 3, i + .25, str(v),
                     color='black', fontweight='normal')
        plt.show()

    def plot_top_20_countries_recovery_rate_across_world(self):
        # ## Top 20 countries W.R.T Recovery Rate
        rate = self.top.groupby(by='country')['recovered',
                                              'confirmed', 'deaths'].sum().reset_index()
        rate['recovery percentage'] = round(
            ((rate['recovered']) / (rate['confirmed'])) * 100, 2)
        rate.head()

        recovery = rate.groupby(by='country')['recovery percentage'].sum(
        ).sort_values(ascending=False).head(20).reset_index()
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel("Total cases", fontsize=30)
        plt.ylabel('Country', fontsize=30)
        plt.title("Top 20 countries having most recovery rate", fontsize=30)
        plt.barh(recovery.country, recovery['recovery percentage'], color=[
            'indigo', 'blueviolet', 'darkorchid', 'mediumorchid', 'orchid', 'hotpink', 'violet', 'pink', 'lightpink'])
        plt.gca().invert_yaxis()
        for i, v in enumerate(recovery['recovery percentage']):
            plt.text(v + 3, i + .25, str(v),
                     color='black', fontweight='normal')
        plt.show()


class Covid19_india(object):
    def __init__(self, db_india_file):
        self.covid_19_india_db_file = db_india_file
        simplefilter(action='ignore', category=FutureWarning)
        

    def update_db_file(self):
        try:
            with open(KAGGLE_CRED_FILE, "r") as fout:
                data = json.load(fout)
                if data:
                    username = data["username"]
                    key = data["key"]
                    db_downlaod_cmd = f"export KAGGLE_USERNAME={username}; export KAGGLE_KEY={key};kaggle datasets download -d sudalairajkumar/covid19-in-india"
                    os.system(db_downlaod_cmd)
                    os.system("rm -fr *.csv")
                    os.system("unzip covid19-in-india.zip")
        except ValueError:
            print("Files not found")

    def read_db_file(self):
        self.df = pd.read_csv(self.covid_19_india_db_file, index_col = 'Date')
        self.df.index = pd.to_datetime(self.df.index, format="%d/%m/%y")
        self.df = self.df.drop(['Sno'], axis = 1)
        self.df.head()

    def describe_db(self):
        self.df.describe(include='object')
        self.df.head()
    
    def rename_columns(self):
        self.df.rename(columns={'Date': 'date',
                                'State/UnionTerritory': 'state',
                                'ConfirmedIndianNational': 'confirmed_indian',
                                'ConfirmedForeignNational': 'confirmed_forigner', 'Cured': 'recovered',
                                'Confirmed': 'confirmed',
                                'Deaths': 'deaths',
                            
                                }, inplace=True)


        self.df.head()
    
    def get_active_cases(self):
        
        self.df['active'] = self.df['confirmed'] - \
            self.df['deaths'] - self.df['recovered']
        self.df.head()
        
        
    def plot_statewise_cases(self):
        self.pivot = pd.pivot_table(self.df, values=['confirmed','deaths','recovered','active'], index='state', aggfunc='max')
        self.pivot = self.pivot.sort_values(by='confirmed', ascending= False)

        self.pivot.style.background_gradient(cmap='Wistia')
        
        
        data = [go.Bar(
            x = self.pivot.index,
            y = self.pivot[colname],
            name = colname
        )for colname in self.pivot.columns]
        
        layout = go.Layout(
        title = "State wise plot of cases in India",
        template = 'plotly_dark'
        )
        fig = go.Figure(data=data,layout=layout)

        plo.iplot(fig)
        
    def get_Date(self):
        self.df['date']=self.df.index
        self.df.head()
        
    def plot_daily_new_cases(self):
        self.df_temp= self.df.groupby('date')['confirmed'].sum().reset_index().sort_values('date')
        self.df_temp['new_cases']=self.df_temp['confirmed'].diff().fillna(method='bfill')
        self.df_temp['new_cases']=self.df_temp['new_cases'].astype(int)

        fig = px.line(self.df_temp,x='date',y='new_cases')
        fig.update_layout(title_text="Daily new cases in India")
        fig.show()
        
        
        
    def plot_daily_recovered_cases(self):  
        self.df_temp1= self.df.groupby('date')['recovered'].sum().reset_index().sort_values('date')
        self.df_temp1['daily_recovered']=self.df_temp1['recovered'].diff().fillna(method='bfill')
        self.df_temp1['daily_recovered']=self.df_temp1['daily_recovered'].astype(int)

        fig = px.line(self.df_temp1,x='date',y='daily_recovered')
        fig.update_layout(title_text="Daily recovered cases in India")
        fig.show()
        
    def plot_daily_death_cases(self):
        self.df_temp2= self.df.groupby('date')['deaths','state'].sum().reset_index().sort_values('date')
        self.df_temp2['daily_deaths']=self.df_temp2['deaths'].diff().fillna(method='bfill')
        self.df_temp2['daily_deaths']=self.df_temp2['daily_deaths'].astype(int)

        fig = px.line(self.df_temp2,x='date',y='daily_deaths')
        fig.update_layout(title_text="Daily deaths cases in India")
        fig.show()
        
        
    def read_data(self):
        self.df_details=pd.read_csv(INDIA_DETAILS)
        india_age(AGE_GROUP_DETAILS).read_file()
        
        
    def state_analysis(self):
        
        def plotly_facts(state):
            
            fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type":"bar"}, {"type":"pie"}],
                   [{"colspan": 2}, None]],
            subplot_titles=(f"Daily cases in {state}",f"Gender ratio of Patients in {state}", f"Daily Recovered Cases in {state}"))
            self.dt = self.df[self.df['state']==state]
            a=self.dt['confirmed']-self.dt['confirmed'].shift(1)
            self.dt['new']=a
            b=self.dt['recovered']-self.dt['recovered'].shift(1)
            self.dt['d_recovered']=b    
    
            self.temp = self.df_details[self.df_details['detected_state']=='Kerala']
    
    
            fig.add_trace(go.Bar(x=self.dt.index, y=self.dt['new']),
                  row=1, col=1)


            fig.add_trace(go.Pie(labels=['Male','Female'],
                                 values=self.temp['gender'].dropna().value_counts(),
                                 showlegend=False),
                                  row=1, col=2)

            fig.add_trace(go.Scatter(x=self.dt.index, y=self.dt['d_recovered']),
                 row=2, col=1)



            fig.update_layout(showlegend=False, title_text=f"Covid-19 Analysis of {state}")
            fig.show()
    
    
            self.temp1=self.df[self.df['state']==state]
            self.temp1=self.temp1.iloc[:,[4,5,8]]




            data = [go.Scatter(
                x = self.temp1.index,
                y = self.temp1[colname],
                name = colname,
                )for colname in self.temp1.columns]
            layout = go.Layout(
                title = f"Active vs Recovered vs Deaths plot in {state}",
                template = 'plotly_dark'
                )

            fig = go.Figure(data=data,layout=layout)

            plo.iplot(fig)
        select_states = list(input("\nEnter Name of State/Union Teritory: ").strip().split())[:10] 
  
        for state in select_states:
             plotly_facts(state)

        
class india_details(object):
    def __init__(self, india_file):
        self.india_db_file = india_file
        simplefilter(action='ignore', category=FutureWarning)
        
    
    def read_file(self):
        self.df_details = pd.read_csv(self.india_db_file)
        self.df_details.head()
        
    def plot_gender_ratio(self):
        self.df_temp3 = self.df_details.gender.dropna().value_counts().reset_index()
        self.df_temp3.columns = ['gender','count']
        fig = px.pie(self.df_temp3,values='count',names='gender',
                     title='Gender Wise Confirmed Cases',
                     color_discrete_sequence=px.colors.sequential.Hot)
        fig.show()
        
        
class india_age(object):
    def __init__(self, india_age_file):
        self.india_age_file = india_age_file
        simplefilter(action='ignore', category=FutureWarning)
        
      
    def read_file(self):
        self.df_age = pd.read_csv(self.india_age_file)
        self.df_age.head()
        
    def plot_agewise(self):
        
        fig = px.pie(self.df_age,values=self.df_age.TotalCases,names=self.df_age.AgeGroup,
             title='Total Cases-Age wise distribution in India',
            color_discrete_sequence=px.colors.sequential.Plasma)
        fig.show()
def main():
    #main Class
    covid_data = Covid19(COVID_19_DB_FILE)
    covid_data.update_db_file()
    covid_data.read_db_file()
    covid_data.describe_db()
    covid_data.data_start_date()
    covid_data.data_last_date()
    covid_data.rename_coloumns()
    covid_data.get_active_cases()
    covid_data.get_active_cases_across_world()
    covid_data.get_data_india()
    covid_india = Covid19_india(COVID_19_INDIA_DB_FILE)
    covid_india.__init__(COVID_19_INDIA_DB_FILE)
    covid_india.update_db_file()
    covid_india.read_db_file()
    covid_india.read_data()
    covid_india.describe_db()
    covid_india.get_Date()
    covid_india.rename_columns()
    covid_india.get_active_cases()
    covid_india_details=india_details(INDIA_DETAILS)
    covid_india_details.__init__(INDIA_DETAILS)
    covid_india_details.read_file()
    covid_india_age=india_age(AGE_GROUP_DETAILS)
    covid_india_age.__init__(AGE_GROUP_DETAILS)
    covid_india_age.read_file()
    covid_india.get_Date()
    #plots
    covid_data.plot_active_cases_across_world()
    time.sleep(DELAY)
    covid_data.plot_confirmed_cases_across_world()
    covid_data.plot_active_cases_across_world()
    time.sleep(DELAY)
    #covid_data.plot_confirmed_cases_across_world()
    covid_data.plot_death_cases_across_world()
    time.sleep(DELAY)
    covid_data.plot_recovered_cases_across_world()
    time.sleep(DELAY)
    covid_data.plot_active_cases_across_india()
    time.sleep(DELAY)
    covid_data.plot_death_cases_across_india()
    time.sleep(DELAY)
    #covid_data.plot_recovered_cases_across_india()
    #time.sleep(DELAY)
    time.sleep(DELAY) 
    covid_data.plot_death_cases_across_india()
    time.sleep(DELAY)
    covid_data.plot_recovered_cases_across_india()
    time.sleep(DELAY)
    #covid_data.plot_top_20_countries_active_cases_across_world()
    #time.sleep(DELAY)
    #covid_data.plot_top_20_countries_confirmed_cases_across_world()
    #time.sleep(DELAY)
    #covid_data.plot_top_20_countries_deaths_across_world()
    #time.sleep(DELAY)
    #covid_data.plot_top_20_countries_recovered_cases_across_world()
    #time.sleep(DELAY)
    #covid_data.plot_top_20_countries_recovery_rate_across_world()
    # time.sleep(DELAY)
    covid_india.plot_statewise_cases()
    time.sleep(DELAY)
    covid_india.plot_daily_new_cases()
    time.sleep(DELAY)
    covid_india.plot_daily_recovered_cases()
    time.sleep(DELAY)
    covid_india.plot_daily_death_cases()
    time.sleep(DELAY)
    covid_india_details.plot_gender_ratio()
    time.sleep(DELAY)
    covid_india_age.plot_agewise()
    time.sleep(DELAY)
    covid_india.state_analysis()
    time.sleep(DELAY)
if __name__ == "__main__":
    main()
