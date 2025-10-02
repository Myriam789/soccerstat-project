# streamlit_app_final_clean.py - The Clean Presentation Version
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 0. CONFIGURATION & MAPPING ---

st.set_page_config(layout="wide", page_title="SoccerStat Pro Final Analysis", initial_sidebar_state="expanded")

# Define clear, full names for every column abbreviation
DISPLAY_NAMES = {
    'Gls_Per_Match': 'Goals per Match',
    'Ast_Per_Match': 'Assists per Match',
    'Min': 'Minutes Played',
    'Gls': 'Total Goals',
    'Ast': 'Total Assists',
    'Comp': 'League',
    'Pos': 'Position',
    'MP': 'Matches Played',
    'xG': 'Expected Goals (xG)',
    'xAG': 'Expected Assisted Goals (xAG)',
    'PrgP': 'Progressive Passes',
    'PrgC': 'Progressive Carries',
}

# Mapping for clarity in the Position Chart
POSITION_MAP = {
    'DF': 'Defender', 'MF': 'Midfielder', 'FW': 'Forward', 'GK': 'Goalkeeper',
    'DF,MF': 'Def/Mid Hybrid', 'MF,FW': 'Mid/For Hybrid', 'MF,DF': 'Mid/Def Hybrid',
    'FW,MF': 'For/Mid Hybrid', 'DF,FW': 'Def/For Hybrid', 'FW,DF': 'For/Def Hybrid',
    'Unknown': 'Unknown'
}

# --- 1. DATA LOADING & CLEANUP ---

@st.cache_data
def load_and_clean_data(player_file, league_file):
    try:
        # Load the base player file and league data
        df = pd.read_csv(player_file) 
        df_league_comp = pd.read_csv(league_file)
    except FileNotFoundError:
        st.error("Error: Data files not found. Ensure 'top5-players_DASHBOARD_READY.csv' and 'league_comparison_data.csv' are in the same folder.")
        st.stop()
    
    # RENAME ALL PLAYER COLUMNS
    df.rename(columns=DISPLAY_NAMES, inplace=True)
    df['Player'] = df['Player'].astype(str).str.strip()
    
    # CREATE CLEAR POSITION AND LEAGUE COLUMNS
    df['Position_Clear'] = df['Position'].apply(lambda x: POSITION_MAP.get(x, x))
    df['League'] = df['League'].replace({
        'eng Premier League': 'Premier League', 'de Bundesliga': 'Bundesliga', 
        'es La Liga': 'La Liga', 'it Serie A': 'Serie A', 'fr Ligue 1': 'Ligue 1'
    })

    # RENAME LEAGUE COMPARISON DATA
    df_league_comp.rename(columns={'Comp': 'League', 'Gls': 'Total Goals', 'Ast': 'Total Assists', 'Min': 'Total Minutes'}, inplace=True)
    df_league_comp['League'] = df_league_comp['League'].replace({
        'eng Premier League': 'Premier League', 'de Bundesliga': 'Bundesliga', 
        'es La Liga': 'La Liga', 'it Serie A': 'Serie A', 'fr Ligue 1': 'Ligue 1'
    })
    
    return df, df_league_comp

df, df_league_comp = load_and_clean_data('top5-players_NEW.csv', 'league_comparison_data.csv')

# --- 2. HELPER FUNCTIONS ---

def get_best_teams(n=5):
    return df.groupby('Squad')['Total Goals'].sum().nlargest(n)

def get_best_players(metric, n=10):
    return df.sort_values(by=metric, ascending=False).head(n)

# --- 3. STREAMLIT LAYOUT ---

st.title("SoccerStat Pro: Final Project Analysis")
st.markdown("### Interactive Dashboard for Top 5 European League Performance (2023/2024)")

# ---------------------------------------------
# SIDEBAR: THE RANKING TOOL
# ---------------------------------------------

st.sidebar.header("Ranking Tool: Find The Best")
st.sidebar.info("Use this tool to find the highest-performing players and teams based on key metrics.")

# Best Player Filter
st.sidebar.markdown("#### Rank Players")
metric_options = {
    'Goals per Match': 'Goals per Match',
    'Total Goals': 'Total Goals',
    'Assists per Match': 'Assists per Match',
    'Expected Goals (xG)': 'Expected Goals (xG)'
}
selected_metric_name = st.sidebar.selectbox("Select Ranking Metric:", list(metric_options.keys()))
selected_metric_column = metric_options[selected_metric_name]

top_players = get_best_players(selected_metric_column, 10)

st.sidebar.markdown(f"**Top 10 Players by {selected_metric_name}:**")
st.sidebar.dataframe(
    top_players[['Player', 'Squad', selected_metric_column]].reset_index(drop=True).style.format({selected_metric_column: '{:.3f}'}),
    use_container_width=True
)

st.sidebar.markdown("---")

# Best Team Section
st.sidebar.markdown(f"#### Top 5 Teams (by Total Goals)")
best_teams = get_best_teams(5)
st.sidebar.dataframe(
    best_teams.reset_index().style.format({'Total Goals': '{:,.0f}'}), 
    use_container_width=True
)


# ---------------------------------------------
# MAIN CONTENT: INDIVIDUAL PLAYER DASHBOARD
# ---------------------------------------------

st.header("1. Individual Player Dashboard")
st.markdown("Use the search bar to pull up a player's profile and analyze their efficiency and contribution rates.")

player_name = st.text_input("Search Footballer's Name:", value="Erling Haaland")

if player_name:
    player_data = df[df['Player'].str.contains(player_name, case=False, na=False)]
    
    if not player_data.empty:
        player = player_data.iloc[0]
        
        # Dashboard Header and Profile Info
        st.markdown(f"## {player['Player']}")
        st.markdown(f"#### {player['Squad']} ({player['League']}) | Role: **{player['Position_Clear']}**")
        
        # --- REQUIRED KEY METRIC CARDS (3 columns) ---
        st.markdown("---")
        metric_cols = st.columns(3)
        
        metric_cols[0].metric("**Goals per Match**", f"{player['Goals per Match']:.3f}", delta=f"Total: {player['Total Goals']}")
        metric_cols[1].metric("**Assists per Match**", f"{player['Assists per Match']:.3f}", delta=f"Total: {player['Total Assists']}")
        metric_cols[2].metric("**Total Time on Field**", f"{player['Minutes Played']:,} mins", delta=f"Matches: {player['Matches Played']:.0f}")
        
        st.markdown("---")
        st.markdown("##### Detailed Season Performance Metrics")
        
        # Final, clean stats table
        stats_cols = ['Matches Played', 'Starts', 'Total Goals', 'Total Assists', 'Expected Goals (xG)', 'Expected Assisted Goals (xAG)', 'Progressive Passes', 'Progressive Carries']
        
        stats_df_display = player[stats_cols].to_frame().T
        
        st.dataframe(
            stats_df_display.style
                .background_gradient(cmap='Greens', subset=['Total Goals', 'Total Assists'])
                .format({'Matches Played': '{:.0f}', 'Starts': '{:.0f}'}), 
            use_container_width=True
        )
            
    else:
        st.warning(f"No player found matching '{player_name}'. Please check the spelling.")

# ---------------------------------------------
# GLOBAL VISUALIZATIONS (General & Comparison)
# ---------------------------------------------

st.markdown("---")
st.header("2. Global Visualization & League Comparison")
st.markdown("These charts illustrate the overall composition of the dataset and the raw productivity of the five leagues.")

chart_col1, chart_col2, chart_col3 = st.columns(3)

# Chart 1: Players by Position (General Visualization)
with chart_col1:
    st.subheader("Player Distribution by Position")
    pos_counts = df['Position_Clear'].value_counts().reset_index()
    pos_counts.columns = ['Position', 'Count']
    st.bar_chart(pos_counts.set_index('Position'))
    st.caption("Count of all players who met the minimum playing time requirement, categorized by their primary role.")

# Chart 2: Players by Nation (General Visualization)
with chart_col2:
    st.subheader("Player Count by Nation")
    nation_counts = df['Nation'].value_counts().head(10).reset_index()
    nation_counts.columns = ['Nation', 'Count']
    st.bar_chart(nation_counts.set_index('Nation'))
    st.caption("The top 10 countries supplying players to the five leagues.")

# Chart 3: League Comparison (Comparison of Performances)
with chart_col3:
    st.subheader("Total League Productivity")
    df_comp = df_league_comp.set_index('League')
    
    # Normalize data for single chart comparison (explaining the 'Normalized Total Volume' concept)
    df_comp_normalized = df_comp[['Total Goals', 'Total Assists', 'Total Minutes']].copy()
    df_comp_normalized['Total Goals'] = df_comp_normalized['Total Goals'] / df_comp_normalized['Total Goals'].max()
    df_comp_normalized['Total Assists'] = df_comp_normalized['Total Assists'] / df_comp_normalized['Total Assists'].max()
    df_comp_normalized['Total Minutes'] = df_comp_normalized['Total Minutes'] / df_comp_normalized['Total Minutes'].max()
    
    st.bar_chart(df_comp_normalized, use_container_width=True)
    st.caption("Compares total Goals, Assists, and Minutes. Data is scaled (normalized) so the highest-performing league hits 100% in each metric.")