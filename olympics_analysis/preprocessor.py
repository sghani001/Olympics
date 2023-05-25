import pandas as pd



def preprocess(df,region_df):

    # filter for summer
    df = df[df['Season'] == 'Summer']
    # merge with region
    df = df.merge(region_df, on='NOC', how='left')
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # drop duplicate on basis of medal
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    df['Year'] = df['Year'].astype('str')
    df.rename(columns={'Name':'Athlete'},inplace=True)
    return df