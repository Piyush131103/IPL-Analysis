# dashboard/app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

st.title("IPL Data Analysis Dashboard")

# -------------------------------
# 1️⃣ Load Data
# -------------------------------
matches = pd.read_csv("../data/processed/matches_clean.csv")
deliveries = pd.read_csv("../data/processed/deliveries_clean.csv")

# Ensure consistent column names
matches.rename(columns={'id':'match_id', 'Season':'season'}, inplace=True)

# Merge deliveries with matches to get season info
deliveries = deliveries.merge(matches[['match_id', 'season']], on='match_id', how='left')

# -------------------------------
# 2️⃣ Top 10 Batsmen
# -------------------------------
st.subheader("Top 10 Batsmen (Total Runs)")
top_batsmen = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=top_batsmen.values, y=top_batsmen.index, ax=ax)
ax.set_xlabel("Runs")
ax.set_ylabel("Batsman")
st.pyplot(fig)

# -------------------------------
# 3️⃣ Top 10 Bowlers
# -------------------------------
st.subheader("Top 10 Bowlers (Wickets)")
# Wickets = count of dismissals except 'run out'
wickets = deliveries[deliveries['dismissal_kind'].notna() & (deliveries['dismissal_kind'] != 'run out')]
top_bowlers = wickets.groupby('bowler')['dismissal_kind'].count().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, ax=ax)
ax.set_xlabel("Wickets")
ax.set_ylabel("Bowler")
st.pyplot(fig)

# -------------------------------
# 4️⃣ Dominant Teams per Season (Stacked Bar)
# -------------------------------
st.subheader("Dominant Team per Season")
team_season_wins = matches.groupby(['season','winner']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12,6))
team_season_wins.plot(kind='bar', stacked=True, ax=ax)
ax.set_ylabel("Matches Won")
ax.set_xlabel("Season")
st.pyplot(fig)

# -------------------------------
# 5️⃣ Match Outcome Patterns
# -------------------------------
st.subheader("Match Outcome Patterns")
# Wins by Runs
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(matches['win_by_runs'], bins=30, kde=True, ax=ax)
ax.set_title("Distribution of Wins by Runs")
st.pyplot(fig)

# Wins by Wickets
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(matches['win_by_wickets'], bins=30, kde=True, ax=ax)
ax.set_title("Distribution of Wins by Wickets")
st.pyplot(fig)

# -------------------------------
# 6️⃣ Consistent Batsmen (Average Runs per Dismissal)
# -------------------------------
st.subheader("Top 10 Consistent Batsmen")
dismissals = deliveries.groupby('batsman')['dismissal_kind'].count()
total_runs = deliveries.groupby('batsman')['batsman_runs'].sum()
batting_avg = total_runs / dismissals.replace(0, np.nan)
consistent_batsmen = batting_avg.sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=consistent_batsmen.values, y=consistent_batsmen.index, ax=ax)
ax.set_xlabel("Batting Average")
ax.set_ylabel("Batsman")
st.pyplot(fig)

# -------------------------------
# 7️⃣ Most Wickets in a Single Match
# -------------------------------
st.subheader("Most Wickets in a Single Match")
wickets_per_match = wickets.groupby(['match_id','bowler']).size().reset_index(name='wickets')
most_wickets_match = wickets_per_match.sort_values('wickets', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x='wickets', y='bowler', data=most_wickets_match, ax=ax)
ax.set_xlabel("Wickets")
ax.set_ylabel("Bowler")
st.pyplot(fig)
