import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
sns.set(style="whitegrid")

st.title("IPL 2008-2023 EDA Dashboard")

# Load cleaned datasets
matches = pd.read_csv("data/processed/matches_clean.csv")
deliveries = pd.read_csv("data/processed/deliveries_clean.csv")

# Merge deliveries with matches for venue info
deliveries = deliveries.merge(
    matches[['id', 'venue']],
    left_on='match_id',  # ensure your deliveries has 'match_id'
    right_on='id',
    how='left'
)

# -----------------------------
# Top 10 Batsmen
# -----------------------------
st.subheader("Top 10 Batsmen by Total Runs")
top_batsmen = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
top_batsmen.plot(kind="bar", ax=ax, color='skyblue')
ax.set_ylabel("Runs")
st.pyplot(fig)

# -----------------------------
# Top 10 Bowlers
# -----------------------------
st.subheader("Top 10 Bowlers by Wickets")
wickets = deliveries[deliveries['is_wicket'] == 1]
top_bowlers = wickets.groupby('bowler').size().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
top_bowlers.plot(kind="bar", ax=ax, color='salmon')
ax.set_ylabel("Wickets")
st.pyplot(fig)

# -----------------------------
# Dominant Team per Season
# -----------------------------
st.subheader("Dominant Team per Season")
dominant_team = matches.groupby(['season','winner']).size().reset_index(name='matches_won')
dominant_team_per_season = dominant_team.loc[dominant_team.groupby('season')['matches_won'].idxmax()]

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='season', y='matches_won', hue='winner', data=dominant_team_per_season, dodge=False, ax=ax)
ax.set_ylabel("Matches Won")
st.pyplot(fig)

# -----------------------------
# Match Outcome Pattern
# -----------------------------
st.subheader("Distribution of Wins by Runs")
fig, ax = plt.subplots(figsize=(12,6))
sns.histplot(matches['win_by_runs'], bins=30, kde=True, color='purple', ax=ax)
ax.set_xlabel("Runs")
st.pyplot(fig)

st.subheader("Distribution of Wins by Wickets")
fig, ax = plt.subplots(figsize=(12,6))
sns.histplot(matches['win_by_wickets'], bins=30, kde=True, color='green', ax=ax)
ax.set_xlabel("Wickets")
st.pyplot(fig)

# -----------------------------
# Venue Analysis
# -----------------------------
deliveries = deliveries.merge(matches[['match_id', 'venue']], on='match_id', how='left')

st.subheader("Top 10 Venues by Average Runs per Match")
deliveries['total_runs'] = deliveries['batsman_runs'] + deliveries['extra_runs']
venue_avg = deliveries.groupby('venue')['total_runs'].mean().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=venue_avg.values, y=venue_avg.index, ax=ax)
ax.set_xlabel("Average Runs")
ax.set_ylabel("Venue")
st.pyplot(fig)

# -----------------------------
# Consistent Batsmen (Batting Average)
# -----------------------------
st.subheader("Top 10 Consistent Batsmen (Batting Average)")
dismissals = deliveries.groupby('batsman')['player_dismissed'].count()
total_runs = deliveries.groupby('batsman')['batsman_runs'].sum()
batting_average = total_runs / dismissals.replace(0, pd.NA)

consistent_batsmen = batting_average.sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
consistent_batsmen.plot(kind='bar', ax=ax, color='orange')
ax.set_ylabel("Batting Average")
st.pyplot(fig)

# -----------------------------
# Most Wickets in a Single Match
# -----------------------------
st.subheader("Most Wickets Taken in a Single Match")
wickets_per_match = deliveries[deliveries['is_wicket'] == 1].groupby(['match_id', 'bowler']).size()
most_wickets = wickets_per_match.sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12,6))
most_wickets.plot(kind='bar', ax=ax, color='red')
ax.set_ylabel("Wickets")
st.pyplot(fig)
