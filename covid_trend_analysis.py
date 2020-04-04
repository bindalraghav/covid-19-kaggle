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


KAGGLE_CRED_FILE = "kaggle.json"
COVID_19_DB_FILE = "covid_19_clean_complete.csv"
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
                    db_downlaod_cmd = f"export KAGGLE_USERNAME={username}; export KAGGLE_KEY={key}; kaggle datasets download -d imdevskp/corona-virus-report"
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
        return self.df.Date.value_counts().sort_index().index[-1]

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


def main():
    covid_data = Covid19(COVID_19_DB_FILE)
    covid_data.update_db_file()
    covid_data.read_db_file()
    covid_data.describe_db()
    covid_data.data_start_date()
    covid_data.data_last_date()
    covid_data.rename_coloumns()
    covid_data.get_active_cases()
    covid_data.get_active_cases_across_world()

    covid_data.plot_active_cases_across_world()
    time.sleep(DELAY)
    # covid_data.plot_confirmed_cases_across_world()
    covid_data.plot_death_cases_across_world()
    time.sleep(DELAY)
    covid_data.plot_recovered_cases_across_world()
    time.sleep(DELAY)
    #covid_data.plot_top_20_countries_active_cases_across_world()
    # time.sleep(DELAY)
    #covid_data.plot_top_20_countries_confirmed_cases_across_world()
    # time.sleep(DELAY)
    #covid_data.plot_top_20_countries_deaths_across_world()
    # time.sleep(DELAY)
    #covid_data.plot_top_20_countries_recovered_cases_across_world()
    # time.sleep(DELAY)
    #covid_data.plot_top_20_countries_recovery_rate_across_world()
    # time.sleep(DELAY)


if __name__ == "__main__":
    main()
