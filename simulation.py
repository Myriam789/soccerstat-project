import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="SoccerStat", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #2c3e50 0%, #000000 100%);
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: black;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .filter-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

players_df = pd.read_csv('top5-players_NEW.csv')

players_df.columns = players_df.columns.str.strip()

st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">SoccerStat</h1>
        <p class="hero-subtitle">Advanced Football Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="filter-box">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)

filtered_df = players_df.copy()

if selected_league != "All":
    filtered_df = filtered_df[filtered_df['Comp'] == selected_league]

if selected_position != "All":
    filtered_df = filtered_df[filtered_df['Pos'] == selected_position]

filtered_df = filtered_df[filtered_df['Min'] >= min_minutes]

st.markdown('<div class="section-header">Key Statistics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-label">Total Players</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{len(filtered_df):,}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-label">Total Goals</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{filtered_df["Gls"].sum():,}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-label">Total Assists</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{filtered_df["Ast"].sum():,}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-label">Avg xG</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{filtered_df["xG"].mean():.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Player Search</div>', unsafe_allow_html=True)
st.markdown('<div class="filter-box">', unsafe_allow_html=True)

player_name = st.text_input("Search for a player:", placeholder="Enter player name...")

if player_name:
    player_results = filtered_df[filtered_df['Player'].str.contains(player_name, case=False, na=False)]
    
    if not player_results.empty:
        player = player_results.iloc[0]
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 2rem; border-radius: 20px; margin: 1rem 0;">
                <h2 style="margin: 0; color: #2c3e50;">{player['Player']}</h2>
                <p style="font-size: 1.2rem; color: #555; margin: 0.5rem 0;">
                    {player['Squad']} | {player['Comp']} | {player['Pos']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Goals", f"{player['Gls']:.0f}")
        mcol2.metric("Assists", f"{player['Ast']:.0f}")
        mcol3.metric("xG", f"{player['xG']:.2f}")
        mcol4.metric("Minutes", f"{player['Min']:,.0f}")
    else:
        st.warning("No player found")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Top Performers</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Goal Scorers", "Assist Leaders", "League Stats"])

with tab1:
    top_scorers = filtered_df.nlargest(15, 'Gls')[['Player', 'Squad', 'Comp', 'Gls', 'xG']]
    
    fig = px.bar(top_scorers, x='Gls', y='Player', orientation='h',
                 color='Gls', color_continuous_scale='purples',
                 title='Top 15 Goal Scorers',
                 labels={'Gls': 'Goals', 'Player': ''})
    fig.update_layout(height=600, showlegend=False, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(top_scorers.reset_index(drop=True), use_container_width=True, hide_index=True)

with tab2:
    top_assists = filtered_df.nlargest(15, 'Ast')[['Player', 'Squad', 'Comp', 'Ast', 'xAG']]
    
    fig = px.bar(top_assists, x='Ast', y='Player', orientation='h',
                 color='Ast', color_continuous_scale='blues',
                 title='Top 15 Assist Providers',
                 labels={'Ast': 'Assists', 'Player': ''})
    fig.update_layout(height=600, showlegend=False, plot_bgcolor='white')
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
    fig.add_trace(go.Bar(name='Goals', x=league_stats['League'], y=league_stats['Goals'], marker_color='#667eea'))
    fig.add_trace(go.Bar(name='Assists', x=league_stats['League'], y=league_stats['Assists'], marker_color="#4ba279"))
    fig.update_layout(title='League Comparison', barmode='group', height=500, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(league_stats, use_container_width=True, hide_index=True)

st.markdown("---")
