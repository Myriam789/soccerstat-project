import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ACCENT_COLOR = '#8B5CF6' 
GREY_DARK = '#1a1a1a' 
VIBRANT_COLOR_SCALE = px.colors.sequential.Sunsetdark 


def apply_custom_styles():
    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color: {GREY_DARK}; /* Solid dark background */
            color: #ffffff; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.7); /* Deep black, slight transparency */
            border-radius: 20px;
            padding: 3rem 4rem; 
            margin-top: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.8), 0 0 8px {ACCENT_COLOR}; /* Simpler shadow effect */
            border: 1px solid rgba(139, 92, 246, 0.2); /* Subtle accent border */
        }}

        [data-testid="stSidebar"] {{
            background-color: rgba(10, 10, 10, 0.95); 
            border-right: 4px solid {ACCENT_COLOR};
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
        }}

        h1 {{
            color: {ACCENT_COLOR};
            text-shadow: 0 0 5px {ACCENT_COLOR}, 0 0 10px rgba(255, 255, 255, 0.2); 
            font-size: 3.5rem;
            letter-spacing: 1px;
            font-weight: 900;
        }}
        
        h2, h3, h4 {{
             color: #ffffff;
             text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
        }}

        [data-testid="stMetricValue"] {{
            color: {ACCENT_COLOR} !important; 
            font-size: 3rem;
            font-weight: bold;
            text-shadow: 0 0 5px rgba(139, 92, 246, 0.5);
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #ccc;
            font-size: 1rem;
        }}

        .stDataFrame {{
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7);
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
st.set_page_config(
    layout="wide", 
    page_title="SoccerStat | Pro Analytics", 
    initial_sidebar_state="collapsed"
)

apply_custom_styles()

try:

    players_df = pd.read_csv('top5-players_NEW.csv')
    
except FileNotFoundError:
   
    st.warning("Data file 'top5-players_NEW.csv' not found. Displaying mock data with professional design.")
    players_df = pd.DataFrame({
        'Player': ['Haaland', 'Mbappe', 'Messi', 'De Bruyne', 'Van Dijk', 'Odegaard', 'Vini Jr', 'Saka', 'Musiala', 'Kvaratskhelia', 'Griezmann', 'Kane', 'Salah', 'Foden', 'Rodri'],
        'Comp': ['Premier League', 'Ligue 1', 'MLS', 'Premier League', 'Premier League', 'Premier League', 'La Liga', 'Premier League', 'Bundesliga', 'Serie A', 'La Liga', 'Bundesliga', 'Premier League', 'Premier League', 'Premier League'],
        'Pos': ['FW', 'FW', 'MF,FW', 'MF', 'DF', 'MF', 'FW', 'FW', 'MF', 'FW', 'FW,MF', 'FW', 'FW', 'MF', 'MF'],
        'Min': [2800, 2650, 1500, 2200, 3200, 2900, 2500, 2700, 2100, 2400, 3000, 2950, 2850, 2600, 3100],
        'Gls': [36, 28, 11, 8, 2, 14, 19, 15, 12, 14, 16, 32, 25, 19, 9],
        'Ast': [8, 12, 15, 18, 3, 7, 9, 11, 8, 10, 14, 9, 13, 11, 6],
        'xG': [32.1, 26.5, 9.8, 6.5, 1.8, 10.5, 17.0, 13.5, 10.0, 12.5, 14.0, 30.0, 22.0, 16.5, 7.5],
        'xAG': [7.5, 10.5, 14.0, 17.0, 2.0, 6.0, 8.0, 10.0, 7.0, 9.0, 12.0, 8.5, 12.0, 9.5, 5.0],
        'Squad': ['Man City', 'PSG', 'Miami', 'Man City', 'Liverpool', 'Arsenal', 'Real Madrid', 'Arsenal', 'Bayern', 'Napoli', 'Atletico', 'Bayern', 'Liverpool', 'Man City', 'Man City'],
        'Nation': ['Norway', 'France', 'Argentina', 'Belgium', 'Netherlands', 'Norway', 'Brazil', 'England', 'Germany', 'Georgia', 'France', 'England', 'Egypt', 'England', 'Spain']
    })
    
players_df.columns = players_df.columns.str.strip()

players_df['Gls/90'] = players_df.apply(lambda row: (row['Gls'] / row['Min']) * 90 if row['Min'] > 0 else 0, axis=1)
players_df['Ast/90'] = players_df.apply(lambda row: (row['Ast'] / row['Min']) * 90 if row['Min'] > 0 else 0, axis=1)

st.title("SoccerStat | Elite Performance Dashboard")
st.subheader("Deep Dive into the World's Top Football Leagues (2023/2024)")

st.markdown("---")

st.header("Analyze & Filter")
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
    max_minutes = int(players_df['Min'].max())
    min_minutes = st.slider("Min Minutes Played (Experience)", 0, max_minutes, 1000, help="Filter out players who haven't played enough minutes for statistical significance.")

filtered_df = players_df.copy()

if selected_league != "All":
    filtered_df = filtered_df[filtered_df['Comp'] == selected_league]

if selected_position != "All":
    filtered_df = filtered_df[filtered_df['Pos'].str.contains(selected_position, case=False, na=False)]

filtered_df = filtered_df[filtered_df['Min'] >= min_minutes]

if filtered_df.empty:
    st.error("No players match the current filter criteria. Try reducing the minimum minutes played.")
    st.stop()

st.markdown("---")
st.header("Global Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Players in View", f"{len(filtered_df):,}")

with col2:
    st.metric("Total Goals Scored", f"{filtered_df['Gls'].sum():,}")

with col3:
    st.metric("Total Assists Provided", f"{filtered_df['Ast'].sum():,}")

with col4:
    total_g_a = filtered_df['Gls'].sum() + filtered_df['Ast'].sum()
    total_mins = filtered_df['Min'].sum()
    ga_per_90 = (total_g_a / total_mins) * 90 if total_mins > 0 else 0
    st.metric("Goals+Assists/90", f"{ga_per_90:.2f}")

st.markdown("---")
st.header("Analysis & Visualization")

tab1, tab2, tab3, tab4 = st.tabs(["General Overview", "Individual Player Profile", "Goals & Expected Goals", "League Performance"]) 

with tab1:
    st.subheader("Global Player Distribution (Big and Readable)")
    
    st.markdown("### Player Count by Primary Position")
    position_counts = filtered_df['Pos'].str.split(',').str[0].value_counts().reset_index()
    position_counts.columns = ['Position', 'Count']
    
    fig_pos = px.bar(
        position_counts,
        x='Count',
        y='Position',
        orientation='h',
        color='Count',
        color_continuous_scale=VIBRANT_COLOR_SCALE,
        title='Count of Players by Position',
        labels={'Count': 'Number of Players', 'Position': ''}
    )
    
    fig_pos.update_layout(
        height=550, 
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0.5)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_pos, use_container_width=True)

    st.markdown("---")
    
    st.markdown("### Player Distribution by Nation")
    nation_counts = filtered_df['Nation'].value_counts().reset_index()
    nation_counts.columns = ['Nation', 'Count']
    
    fig_nation = px.pie(
        nation_counts,
        values='Count',
        names='Nation',
        title='Distribution of Players by Nation',
        hole=0.4, 
        color_discrete_sequence=px.colors.qualitative.Pastel 
    )
    
    fig_nation.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        marker=dict(line=dict(color='#000000', width=1)),
        textfont_size=14 
    )
    fig_nation.update_layout(
        height=650,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(t=50, b=0, l=0, r=0),
        legend=dict(font=dict(size=12))
    )
    st.plotly_chart(fig_nation, use_container_width=True)

with tab2:
    st.subheader("Analyze Individual Player Statistics")
    
    player_name_list = sorted(filtered_df['Player'].unique().tolist())
    player_selection = st.selectbox("Select a player for detailed view:", player_name_list, key="player_select_tab2")

    if player_selection:
        player = filtered_df[filtered_df['Player'] == player_selection].iloc[0]
        
        st.markdown(f"### Profiling: **{player['Player']}** ({player['Squad']} - {player['Comp']})")
        
        col_info, col_chart = st.columns([1, 2])
        
        with col_info:
            st.write(f"**Position:** {player['Pos']}")
            st.write(f"**Nation:** {player['Nation']}")
            st.write(f"**Minutes Played (Experience):** {player['Min']:.0f}")
            
            st.markdown("#### Performance Per 90 Minutes")
            st.metric("Goals / 90 Mins", f"{player['Gls/90']:.2f}", help="Equivalent to 'Nombre de buts par match'")
            st.metric("Assists / 90 Mins", f"{player['Ast/90']:.2f}", help="Equivalent to 'Nombre d'assists par match'")
            
            st.markdown("#### Raw Performance")
            st.metric("Total Goals (Gls)", f"{player['Gls']:.0f}")
            st.metric("Total Assists (Ast)", f"{player['Ast']:.0f}")

        with col_chart:
            stats_cols = ['Gls', 'Ast', 'xG', 'xAG']
            display_stats = ['Goals (Gls)', 'Assists (Ast)', 'Expected Goals (Exp Gls)', 'Expected Assists (Exp Ast)']
            
            group_avg = filtered_df[stats_cols].mean().to_dict()

            comparison_data = {
                'Metric': display_stats,
                'Player Value': [player[s] for s in stats_cols],
                'Group Average': [group_avg[s] for s in stats_cols]
            }
            comparison_df = pd.DataFrame(comparison_data)
            
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=comparison_df['Metric'],
                y=comparison_df['Player Value'],
                name=player['Player'] + ' Value',
                marker_color=ACCENT_COLOR,
                opacity=0.8
            ))

            fig.add_trace(go.Scatter(
                x=comparison_df['Metric'],
                y=comparison_df['Group Average'],
                mode='markers+lines',
                name='Group Average',
                marker=dict(size=10, color='red', symbol='circle'),
                line=dict(width=2, color='red', dash='dash')
            ))

            fig.update_layout(
                title=f"Raw Performance vs. Filtered Group Average",
                yaxis_title="Statistical Value",
                height=500,
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font_color='white',
                margin=dict(l=50, r=50, t=50, b=50),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Scoring Efficiency: Actual vs. Expected Goals")
    
    comparison_df = filtered_df.nlargest(15, 'Gls')[['Player', 'Gls', 'xG']].copy()
  
    comparison_df.rename(columns={'xG': 'Exp Gls'}, inplace=True)
    
    melted_df = comparison_df.melt(
        id_vars='Player', 
        value_vars=['Gls', 'Exp Gls'],
        var_name='Metric', 
        value_name='Value'
    )
    
    fig = px.bar(
        melted_df, 
        x='Value', 
        y='Player', 
        color='Metric', 
        orientation='h',
        barmode='group',
        color_discrete_map={
            'Gls': ACCENT_COLOR, 
            'Exp Gls': '#FF8C00'     
        },
        hover_data=['Player', 'Metric', 'Value'],
        title='Actual Goals (Gls) vs. Expected Goals (Exp Gls) by Player',
        labels={'Value': 'Goals/Expected Goals', 'Player': ''}
    )

    fig.update_layout(
        height=600,
        plot_bgcolor='rgba(0,0,0,0.5)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(gridcolor='#374151', zeroline=True, zerolinecolor='white', zerolinewidth=2),
        yaxis=dict(gridcolor='#374151'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_yaxes(categoryorder='array', categoryarray=comparison_df['Player'].tolist()[::-1])
    
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("League-wide Aggregate Performance")

    league_performance = filtered_df.groupby('Comp').agg({
        'Gls': 'sum',
        'Ast': 'sum',
        'Min': 'sum',
        'Player': 'count'
    }).rename(columns={'Player': 'Total Players'}).reset_index()
    
    st.dataframe(league_performance, use_container_width=True, hide_index=True)
    
    fig_ga = go.Figure(data=[
        go.Bar(
            name='Total Goals',
            y=league_performance['Comp'],
            x=league_performance['Gls'],
            orientation='h',
            marker_color=ACCENT_COLOR
        ),
        go.Bar(
            name='Total Assists',
            y=league_performance['Comp'],
            x=league_performance['Ast'],
            orientation='h',
            marker_color='#FF8C00'
        )
    ])
    
    fig_ga.update_layout(
        barmode='group',
        title='Total Goals & Assists by League',
        yaxis_title="League",
        xaxis_title="Count",
        height=500,
        plot_bgcolor='rgba(0,0,0,0.5)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_ga, use_container_width=True)
    
    fig_min = px.bar(
        league_performance,
        x='Min',
        y='Comp',
        orientation='h',
        color='Min',
        color_continuous_scale='Mint',
        title='Total Minutes Played (Experience) by League',
        labels={'Min': 'Total Minutes', 'Comp': 'League'}
    )
    fig_min.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_min, use_container_width=True)



st.markdown(
    """
    <div style='text-align: center; margin-top: 5rem; color: #999; font-size: 0.9rem;'>
        Dashboard created by Sarah , Rosa and Myriam
    </div>
    """,
    unsafe_allow_html=True
)
