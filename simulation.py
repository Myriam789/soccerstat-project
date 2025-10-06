import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
 
st.set_page_config(layout="wide", page_title="SoccerStat", initial_sidebar_state="collapsed")
 
players_df = pd.read_csv('top5-players_NEW.csv')
 
players_df.columns = players_df.columns.str.strip()
 
st.title("SoccerStat")
st.subheader("Football Dashboard")
 
st.markdown("---")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    selected_league = st.selectbox(
        "League",
        options=["All"] + sorted(players_df['Comp'].unique().tolist())
    )
 
with col2:
    selected_position = st.selectbox(
        "Position",
        options=["All"] + sorted(players_df['Pos'].unique().tolist())
    )
 
with col3:
    min_minutes = st.slider("Min Minutes Played", 0, int(players_df['Min'].max()), 0)
 
filtered_df = players_df.copy()
 
if selected_league != "All":
    filtered_df = filtered_df[filtered_df['Comp'] == selected_league]
 
if selected_position != "All":
    filtered_df = filtered_df[filtered_df['Pos'] == selected_position]
 
filtered_df = filtered_df[filtered_df['Min'] >= min_minutes]
 
st.markdown("---")
st.header("Key Statistics")
 
col1, col2, col3, col4 = st.columns(4)
 
with col1:
    st.metric("Total Players", f"{len(filtered_df):,}")
 
with col2:
    st.metric("Total Goals", f"{filtered_df['Gls'].sum():,}")
 
with col3:
    st.metric("Total Assists", f"{filtered_df['Ast'].sum():,}")
 
with col4:
    st.metric("Avg xG", f"{filtered_df['xG'].mean():.2f}")
 
st.markdown("---")
st.header("Player Search")
 
player_name = st.text_input("Search for a player:", placeholder="Enter player name...")
 
if player_name:
    player_results = filtered_df[filtered_df['Player'].str.contains(player_name, case=False, na=False)]
   
    if not player_results.empty:
        player = player_results.iloc[0]
       
        st.subheader(f"{player['Player']}")
        st.write(f"**Team:** {player['Squad']} | **League:** {player['Comp']} | **Position:** {player['Pos']}")
       
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Goals", f"{player['Gls']:.0f}")
        mcol2.metric("Assists", f"{player['Ast']:.0f}")
        mcol3.metric("xG", f"{player['xG']:.2f}")
        mcol4.metric("Minutes", f"{player['Min']:,.0f}")
    else:
        st.warning("No player found")
 
st.markdown("---")
st.header("Top Performers")
 
tab1, tab2, tab3 = st.tabs(["Goal Scorers", "Assist Leaders", "League Stats"])
 
with tab1:
    top_scorers = filtered_df.nlargest(15, 'Gls')[['Player', 'Squad', 'Comp', 'Gls', 'xG']]
   
    fig = px.bar(top_scorers, x='Gls', y='Player', orientation='h',
                 color='Gls', color_continuous_scale='Greys',
                 title='Top 15 Goal Scorers',
                 labels={'Gls': 'Goals', 'Player': ''})
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
   
    st.dataframe(top_scorers.reset_index(drop=True), use_container_width=True, hide_index=True)
 
with tab2:
    top_assists = filtered_df.nlargest(15, 'Ast')[['Player', 'Squad', 'Comp', 'Ast', 'xAG']]
   
    fig = px.bar(top_assists, x='Ast', y='Player', orientation='h',
                 color='Ast', color_continuous_scale='Greys',
                 title='Top 15 Assist Providers',
                 labels={'Ast': 'Assists', 'Player': ''})
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
   
    st.dataframe(top_assists.reset_index(drop=True), use_container_width=True, hide_index=True)
 
with tab3:
    league_stats = filtered_df.groupby('Comp').agg({
        'Gls': 'sum',
        'Ast': 'sum',
        'xG': 'sum',
        'Player': 'count'
    }).reset_index()
    league_stats.columns = ['League', 'Goals', 'Assists', 'xG', 'Players']
   
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Goals', x=league_stats['League'], y=league_stats['Goals'], marker_color='#434343'))
    fig.add_trace(go.Bar(name='Assists', x=league_stats['League'], y=league_stats['Assists'], marker_color='#2a2a2a'))
    fig.update_layout(title='League Comparison', barmode='group', height=500)
    st.plotly_chart(fig, use_container_width=True)
   
    st.dataframe(league_stats, use_container_width=True, hide_index=True)
 
 