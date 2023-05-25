import pandas as pd
import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return country, years


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def overall_analysis(df):
    no_of_editions = df['Year'].unique().shape[0] - 1
    no_of_cities = df['City'].unique().shape[0]
    no_of_events = df['Event'].unique().shape[0]
    no_of_atheletes = df['Athlete'].unique().shape[0]
    no_of_nations = df['region'].unique().shape[0]
    no_of_sports = df['Sport'].unique().shape[0]

    return no_of_editions, no_of_cities, no_of_events, no_of_atheletes, no_of_nations, no_of_sports


def data_over_time(df, data):
    data_over_time = df.drop_duplicates(['Year', data])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns={'index': 'Year', 'Year': data}, inplace=True)
    return data_over_time


def pivot_table(df):
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    return pivot_table


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = \
    temp_df['Athlete'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Athlete', how='left')[
        ['index', 'Athlete_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Athlete', 'Athlete_x': 'Medals'}, inplace=True)
    return x


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Athlete'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Athlete', how='left')[
        ['index', 'Athlete_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Athlete', 'Athlete_x': 'Medals'}, inplace=True)
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Athlete', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Athlete', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Athlete'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Athlete'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Athlete_x': 'Male', 'Athlete_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
