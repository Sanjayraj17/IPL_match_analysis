# IPL_match_analysis
An analysis and visualization of IPL matches 

import numpy as np
import pandas as pd
import matplotlib.pyplot as mlt
import seaborn as sns
mlt.style.use('fivethirtyeight')
import plotly.offline as py
import plotly.graph_objects as go
import plotly.tools as tls

matches = pd.read_csv('matches.csv')

deliveries = pd.read_csv('deliveries.csv')

# Cleaning and transformation

matches.drop('full_scorecard', axis = 1, inplace = True)

matches.columns

deliveries.fillna(0, inplace = True)

deliveries.head()

matches['team1'].unique()

matches.replace('Rising Pune Supergiant', 'Rising Pune Supergiants', inplace = True)

matches['team1'].unique()

matches.replace(['Chennai Super Kings', 'Mumbai Indians',
       'Royal Challengers Bangalore', 'Lucknow Super Giants',
       'Rajasthan Royals', 'Kolkata Knight Riders', 'Punjab Kings',
       'Gujarat Titans', 'Delhi Capitals', 'Sunrisers Hyderabad',
       'Kings XI Punjab', 'Delhi Daredevils', 'Gujarat Lions', 'Rising Pune Supergiants',
       'Pune Warriors', 'Deccan Chargers', 'Kochi Tuskers Kerala'],
                ['CSK','MI','RCB','LSG','RR','KKR','PB','GT','DC','SRH','KXIP','DD','GL','RPS','PW','DCS','KTK'], inplace = True)

deliveries['batting_team'].unique()

deliveries.replace(['Rising Pune Supergiant', 'Royal Challengers Bengaluru'], ['Rising Pune Supergiants','Royal Challengers Bangalore'], inplace = True)

deliveries['batting_team'].unique()

deliveries.replace(['Kolkata Knight Riders', 'Royal Challengers Bangalore',
       'Chennai Super Kings', 'Kings XI Punjab', 'Rajasthan Royals',
       'Delhi Daredevils', 'Mumbai Indians', 'Deccan Chargers',
       'Kochi Tuskers Kerala', 'Pune Warriors', 'Sunrisers Hyderabad',
       'Rising Pune Supergiants', 'Gujarat Lions', 'Delhi Capitals',
       'Punjab Kings', 'Lucknow Super Giants', 'Gujarat Titans'],
                   ['KKR','RCB','CSK','KXIP','RR','DD','MI','DCS','KTK','PW','SRH','RPS','GL','DC','PB','LSG','GT'], inplace = True)

# Basic analysis

print("Total matches played", matches.shape[0])

print('\nvenues played at: ', matches['place'].unique())

print('\nTeams :', matches['team1'].unique())

print((matches['man_of_the_match'].value_counts()).idxmax(), ': has most no. of MOM awards')
print((matches['winner'].value_counts()).idxmax(), ': has most no. of wins in IPL')

matches.iloc[[matches['margin'].idxmax()]]

# Toss decisions

print("Toss decisions %")
print(matches['toss_choice'].value_counts(normalize = True)*100)

mlt.subplots(figsize = (10,6))

ax = matches['toss_winner'].value_counts().plot.bar(width = 0.9, color = sns.color_palette('RdYlGn', 20))

for p in ax.patches:
    ax.annotate(format(p.get_height()),( p.get_x() + 0.15 , p.get_height() + 1))

mlt.show()

# Total matches won by teams

py.init_notebook_mode(connected = True)

matches_played_byteams = pd.concat([matches['team1'],  matches['team2']])

matches_played_byteams = matches_played_byteams.value_counts().reset_index()
matches_played_byteams.columns = ['Team','Total matches']

wins = matches['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']

matches_played_byteams = matches_played_byteams.merge(wins, on = 'Team', how = 'left')
matches_played_byteams['Wins'].fillna(0, inplace = True)

matches_played_byteams.set_index('Team', inplace = True)

print(matches_played_byteams)

trace1 = go.Bar(x = matches_played_byteams.index,
                y = matches_played_byteams['Total matches'],
                name = 'Total matches')

trace2 = go.Bar(x = matches_played_byteams.index,
                y = matches_played_byteams['Wins'],
                name = 'Wins')

data = [trace1,  trace2]
layout = go.Layout(title = 'Total matches vs  Wins',
                   xaxis = dict(title = 'Teams'),
                   yaxis = dict(title = 'Count'),
                   barmode = 'stack')

fig = go.Figure(data = data , layout = layout)
py.iplot(fig, filename = 'stacked-bar')

# Toss winner vs match winner

matches.shape

df = matches[matches['toss_winner'] == matches['winner']]

slices =[ len(df), (958 - len(df))]

labels = ['yes','No']

mlt.pie(slices,
        labels = labels,
        startangle = 90,
        shadow = True,
        explode = (0,0.1),
        colors = ['r','g'],
        autopct = '%1.1f%%')

fig = mlt.gcf()

fig.show()

# Matches played each season

mlt.subplots(figsize = (10,6))

sns.countplot(x = 'season', data = matches, color = sns.color_palette('winter'))

mlt.show()

# Runs across season

batsmen = matches[['id','season']].merge(deliveries, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)

season = batsmen.groupby('season')['total_runs'].sum().reset_index()

season.set_index('season').plot(marker = 'o')

mlt.gcf().set_size_inches(10,6)

mlt.title("Total runs across season")

mlt.show()

# Runs per over by teams across seasons

runs_per_over = delivery.pivot_table(index = ['over'], columns = 'batting_team', values = 'total_runs', aggfunc = sum)

runs_per_over[(matches_played_byteams[matches_played_byteams['Total_matches'] > 50].index)].plot(color = ['b','r', '#Ffb6b2','g','brown','y','#6666ff','black','#FFA500'])

x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

mlt.xticks(x)

mlt.ylabel("Total runs scored")

fig = mlt.gcf()

mlt.show()

# Sixes and Fours across season

season_boundaries = batsmen.groupby('season')['batsmen_runs'].agg(lambda x : (x ==6).sum()).reset_index()

a = batsmen.groupby('season')['batsmen_runs'].agg(lambda x : (x ==4).sum()).reset_index()

season_boundaries = season_boundaries.merge(a, left_on = 'season', right_on = 'season', how = 'left')

season_boundaries = season_boundaries.rename(columns = {'batsmen_runs_x' : '6"s', 'batsmen_runs_y' : '4"s'})

season_boundaries.set_index('season')[['6"s','4"s']].plot(marker = 'o')

fig = mlt.gcf()

fig.set_size_inches(10,6)

mlt.show()

# Favourite stadium

mlt.subplots(figsize = (10,6))

ax = matches['stadium'].value_counts().sort_values(ascending = True).plot.barh(width = 0.9, color = sns.color_palette('inferno',40))

ax.set_xlabel("Stadium")

ax.set_ylabel('Count')

mlt.show()

# Maximum Man of the matches

mlt.subplots(figsize = (10,6))

ax = matches['man_of_the_match'].value_counts().head(10).plot.bar(width = 0.9, color = sns.color_palette('inferno', 40))

ax.set_xlabel('Player')

ax.set_ylabel("count")

for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.15, p.get_height() + 0.25))

mlt.show()

# Winner by year

print("Winners by years :\n")

for i in range(2008,2022):
    df = (matches[matches['season'] == i].iloc[-1])
    print(df[[1,10]].values)

# Teams never played a super over

teams =  ['CSK','MI','RCB','LSG','RR','KKR','PB','GT','DC','SRH','KXIP','DD','GL','RPS','PW','DCS','KTK']

play = deliveries[deliveries['is_super_over'] == 1].batting_team.unique()

play = list(play)

print('Teams who never played a super over: ', list(set(teams) - set(play)))

# Favourite umpires

mlt.subplots(figsize = (10,6))

ump = pd.concat([matches['umpire1'], matches['umpire2']])

ax = ump.value_counts().head(10).plot.bar(width = 0.8, color = sns.color_palette('summer',20))

for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.15, p.get_height() + 1))

mlt.show()

# Team 1 vs Team 2

def team1_vs_team2(team1, team2):
    mt1 = matches[((matches['team1']==team1) | (matches['team2'] == team1)) & ((matches['team1'] == team2) | (matches['team2'] == team2))]
    sns.countplot(x = 'season', hue = 'winner', data = mt1, palette = 'set3')
    sns.xticks(rotation = 'vertical')
    leg = mlt.legend(loc = 'upper center')
    fig = mlt.gcf()
    fig.set_size_inches(10,6)
    mlt.show()

# Matches won by against each team

def comparator(team1):
    teams =  ['CSK','MI','RCB','LSG','RR','KKR','PB','GT','DC','SRH','KXIP','DD','GL','RPS','PW','DCS','KTK']
    teams.remove(team1)
    opponents = teams.copy()
    mt1 = matches[((matches['team1']==team1) | (matches['team2']==team1))]
    for i in opponents:
        mask = (((mt1['team1']==i) | (mt1['team2']==i)) & ((mt1['team1']==team1) | (mt1['team2']==team1)))
        mt2 = mt1.loc[mask,'winner'].value_counts().to_frame().T
        print(mt2)

comparator('MI')

# 200+ Scores

high_scores = deliveries.groupby(['match_id','inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()

high_scores = high_scores[high_scores['total_runs'] >= 200]

high_scores.nlargest(10, 'total_runs')

# Chances of chasing 200+ target

slices = high_scores['is_target_chased'].map({'yes':1,'no':0}).value_counts()

labels = ['Target not chased','Target chased']

mlt.pie(slices, labels = labels, color = ['r','y'], startangle = 90,  shadow = True, autopct = '%1.1f%%', explode = (0,0.1))

fig = mlt.gcf()

fig.set_size_inches(10,6)

mlt.show()

# Batsman comparator

balls = deliveries.groupby(['batter'])['ball'].count().reset_index()

runs = deliveries.groupby(['batter'])['batsman_runs'].sum().reset_index()

balls = balls.merge(runs, left_on = 'batter', right_on = 'batter', how = 'outer')

fours = deliveries.groupby(['batter'])['batsman_runs'].agg(lambda x : (x==4).sum()).reset_index()

sixes = deliveries.groupby(['batter'])['batsman_runs'].agg(lambda x : (x==6).sum()).reset_index()

balls['strike_rate'] = balls['batsman_runs'] / balls['ball'] * 100

balls = balls.merge(fours, right_on = 'batter', left_on = 'batter', how = 'outer')

balls = balls.merge(sixes, right_on = 'batter', left_on = 'batter', how = 'outer')

compare = deliveries.groupby(['match_id','batter','batting_team'])['batsman_runs']

compare = compare.groupby(['batter','batting_team'])['batsman_runs'].max().reset_index()

balls = balls.merge(compare, right_on = 'batter', left_on = 'batter', how = 'outer')

balls.head(20)

# Top 10 Batsman

mlt.subplots(figsize = (10,6))

max_runs = deliveries.groupby(['batter'])['batsman_runs'].sum()

ax = max_runs.sort_values(ascending = False)[:10].plot.bar(width = 0.8, color = sns.color_palette('winter_r',20))

for p in ax.patches:
    ax.annotate(format(p.get_height()),(p.get_x() + 0.1, p.get_height() + 50) , fontsize = 15)

mlt.show()

# Top batsman with 1s 2s 4s 6s

toppers = deliveries.groupby(['batter','batsman_runs'])['total_runs'].count().reset_index()

toppers = toppers.pivot_table(index = 'batter', columns = 'batsman_runs', values = 'total_runs', fill_value = 0)

fig, ax = mlt.subplots(2,2, figsize = (18,12))

toppers[1].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[0,0], color = '#45ff45',width = 0.8)
ax[0,0].set_title('Most 1"s')
ax[0,0].set_ylabel("")

toppers[2].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[0,1], color = '#df6dfd',width = 0.8)
ax[0,1].set_title('Most 2"s')
ax[0,1].set_ylabel("")

toppers[4].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[1,0], color = '#fbca5f',width = 0.8)
ax[1,0].set_title('Most 4"s')
ax[1,0].set_ylabel("")

toppers[6].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[1,1], color = '#ffff00',width = 0.8)
ax[1,1].set_title('Most 6"s')
ax[1,1].set_ylabel("")

mlt.show()

# Top individual scores

top_scores = deliveries.groupby(['match_id','batter','batting_team'])['batsman_runs'].sum().reset_index()

top_scores.sort_values('batsman_runs',ascending = True).head(10)

top_scores.nlargest(10, 'batsman_runs')

# Orange cap

orange = matches[['id','season']]

orange = orange.merge(deliveries, left_on = 'id', right_on = 'match_id', how = 'left')

orange = orange.groupby(['season','batsman'])['batsman_runs'].sum().reset_index()

orange = orange.sort_values('batsman_runs', ascending = True)

orange = orange.drop_duplicates(subset = ['season'], keep = 'first')

orange.sort_values(by =  'season')

trace1 = go.Bar( x = orange['season'].values,
                 y = orange['batsman_runs'].values,
                 name = 'Total matches',
                 text = orange['batsman'].values,
                 marker = dict(color = 'rgb(255,140,0)',
                               line = dict(color = 'rgb(8,48,107)',
                                           width = 1.5)),
                 opacity = 1)

layout = go.Layout(title = 'Orange cap holders')

data = [trace1]

fig = go.Figure(data = data, layout = layout)

py.iplot(fig, filename = 'stacked-bar')

# Top wicket taker

mlt.subplots(figsize = (12,8))

dismissal_kinds = ['bowled','caught','lbw','stumped','caught and bowled','hit wicket']

ct = deliveries[deliveries['dismissal_kind'].isin(dismissal_kinds)]

ax = ct['bowler'].value_counts()[:10].plot.bar(width = 0.8, color = sns.color_palette('summer_r',20))

for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.10, p.get_height()), fontsize = 15)

mlt.show()

# Top 20 bowlers

bowlers = deliveries.groupby('bowler').sum(numeric_only = True).reset_index()

bowl = deliveries['bowler'].value_counts().reset_index()
bowl.columns = ['bowler','balls']
bowl['index'] = range(1 , len(bowl) + 1)

bowl['bowler'] = bowl['bowler'].astype(str)
bowlers['bowler'] = bowlers['bowler'].astype(str)

bowlers = bowlers.merge(bowl, on = 'bowler', how = 'left')

bowlers = bowlers[['bowler','total_runs','balls']]

bowlers.rename({'total_runs':'runs_given'}, axis = 1, inplace = True)

bowlers['overs'] = bowlers['balls']// 6

dismissal_kinds = ['bowled','caught','lbw','stumped','caught and bowled','hit wicket']
ct = deliveries[deliveries['dismissal_kind'].isin(dismissal_kinds)]
ct = ct['bowler'].value_counts()[:20].reset_index()
ct.columns = ['bowler','wickets']

ct['bowler'] = ct['bowler'].astype(str)

bowlers = bowlers.merge(ct, on = 'bowler', how = 'left').dropna()

bowlers['economy'] = bowlers['runs_given'] / bowlers['overs']

bowlers.head()

# Highest dismissal for a batsman by a bowler

def get_top_bowler(batsman_name):
    batsman_data = deliveries[deliveries['batter'] == batsman_name]
    batsman_data = batsman_data['dismissal_kind'].isin(['bowled','caught','lbw','stumped','caught and bowled','hit wicket'])
    top_bowler = batsman_data.groupby('bowler').count().sort_values(by = 'dismissal_kind', ascending = True)
    top_bowler['batter'] = batsman_name
    return top_bowler

batsmen = ['MS Dhoni', 'SK Raina', 'RG Sharma', 'V Kohli']

[get_top_bowler(batsman) for batsman in batsmen]

# Purple cap for each season

dismissal_kinds = ['bowled','caught','lbw','stumped','caught and bowled','hit wicket']

purple = deliveries[deliveries['dismissal_kind'].isin(dismissal_kinds)]

purple = deliveries.merge(matches, left_on = 'match_id', right_on = 'id', how = 'outer')

purple = purple.groupby(['season','bowler','dismissal_kind']).count().reset_index()

purple = purple.sort_values('dismissal_kind', ascending = False)

purple = purple.drop_duplicates('season', keep = 'first').sort_values(by = 'season')
