import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor, helper
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall', 'Country Wise', 'Athlete Wise')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    country, years = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Years', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Overall Medal Tally of " + str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("Overall Medal Tally of " + str(selected_country) + " in " + str(selected_year))
    st.table(medal_tally)

if user_menu == 'Overall':
    no_of_editions, no_of_cities, no_of_events, no_of_atheletes, no_of_nations, no_of_sports = helper.overall_analysis(
        df)
    st.title("TOP STATISTICS")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(no_of_editions)
    with col2:
        st.header("Cities")
        st.title(no_of_cities)
    with col3:
        st.header("Events")
        st.title(no_of_events)
    with col1:
        st.header("Athletes")
        st.title(no_of_atheletes)
    with col2:
        st.header("Nations")
        st.title(no_of_nations)
    with col3:
        st.header("Sports")
        st.title(no_of_sports)

    st.title("Participating Nation Over the Years")
    nation_over_time = helper.data_over_time(df, 'region')

    fig = px.line(nation_over_time, x="Year", y="region")
    st.plotly_chart(fig)

    st.title("Events Over the Years")
    event_over_time = helper.data_over_time(df, 'Event')

    fig = px.line(event_over_time, x="Year", y="Event")
    st.plotly_chart(fig)

    st.title("Athletes Over the Years")
    event_over_time = helper.data_over_time(df, 'Athlete')

    fig = px.line(event_over_time, x="Year", y="Athlete")
    st.plotly_chart(fig)

    st.title("Sports Over Years")
    pivot_table = helper.pivot_table(df)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)

    most_success = helper.most_successful(df, selected_sport)
    st.table(most_success)

if user_menu == 'Country Wise':
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    st.sidebar.title("Country Wise Analysis")
    selected_country = st.sidebar.selectbox('Select Country', country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)

    st.title("Medal Tally of " + selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title(selected_country + "'s most Successful Players")
    most_success_player = helper.most_successful_country(df, selected_country)
    st.table(most_success_player)

if user_menu == 'Athlete Wise':
    athlete_df = df.drop_duplicates(subset=['Athlete', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()

    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
