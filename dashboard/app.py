import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
st.set_page_config(page_title="IPL Dashboard", layout="wide")

st.title("IPL Dashboard")
st.write("Interactive dashboard showing IPL match and player statistics.")

# Load cleaned datasets
matches = pd.read_csv("data/matches_clean.csv")
deliveries = pd.read_csv("data/deliveries_clean.csv")

# ---------------- Top Batsmen ----------------
st.subheader("Top 10 Batsmen")
top_batsmen = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10,5))
top_batsmen.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------- Top Bowlers ----------------
st.subheader("Top 10 Bowlers")
top_bowlers = deliveries.groupby("bowler")["is_wicket"].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10,5))
top_bowlers.plot(kind="bar", ax=ax2, color='orange')
st.pyplot(fig2)

# ---------------- Dominant Teams per Season ----------------
st.subheader("Dominant Teams per Season")
team_wins = matches.groupby(['season', 'winner']).size().unstack(fill_value=0)
fig3, ax3 = plt.subplots(figsize=(12,6))
team_wins.plot(kind='bar', stacked=True, ax=ax3)
st.pyplot(fig3)

# ---------------- Match Outcome Patterns ----------------
st.subheader("Match Outcome Patterns")
fig4, ax4 = plt.subplots(figsize=(12,5))
sns.histplot(matches['win_by_runs'], bins=30, kde=True, ax=ax4)
ax4.set_title("Distribution of Wins by Runs")
st.pyplot(fig4)

fig5, ax5 = plt.subplots(figsize=(12,5))
sns.histplot(matches['win_by_wickets'], bins=30, kde=True, ax=ax5)
ax5.set_title("Distribution of Wins by Wickets")
st.pyplot(fig5)

# ---------------- Venue-wise Average Scores ----------------
st.subheader("Top 10 Venues by Average Score")
deliveries['total_runs'] = deliveries['batsman_runs'] + deliveries['extra_runs']
venue_avg = deliveries.groupby('venue')['total_runs'].mean().sort_values(ascending=False).head(10)
fig6, ax6 = plt.subplots(figsize=(12,5))
sns.barplot(x=venue_avg.values, y=venue_avg.index, ax=ax6)
ax6.set_xlabel("Average Runs")
st.pyplot(fig6)

# ---------------- Most Wickets in a Single Match ----------------
st.subheader("Most Wickets in a Single Match")
wickets_per_match = deliveries.groupby(['match_id', 'bowler'])['is_wicket'].sum()
top_wickets = wickets_per_match.sort_values(ascending=False).head(10)
fig7, ax7 = plt.subplots(figsize=(12,5))
top_wickets.plot(kind="bar", ax=ax7, color='green')
st.pyplot(fig7)
