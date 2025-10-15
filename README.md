SoccerStat Dashboard This project is an interactive, data-driven dashboard designed for deep-dive analysis of elite football player performance across the top five European leagues during the 2023/2024 season. Built using Streamlit and Python, it provides visual comparisons and statistical filtering capabilities, presented with a custom 'Stealth Mode' aesthetic for a modern, professional look.

Key Features Dynamic Filtering: Filter players instantly by League ( Premier League, La Liga, Bundesliga, etc.), Position (FW, MF, DF), and minimum Minutes Played.

Global Metrics: Calculates and displays aggregate stats such as total goals, total assists, and the average Goals + Assists per 90 minutes (G+A/90) for the filtered group.

Individual Player Profile: Select any player to view their raw stats (Gls, Ast, xG, xAG) and compare them directly against the average performance of the entire filtered group.

Performance Visualizations:

Goals vs. Expected Goals (xG): Bar charts visualizing scoring efficiency by comparing actual goals against expected goals (xG).

Player Distribution: Pie and bar charts showing player counts by primary position and nation.

Professional UI: Features a custom CSS theme that ensures readability and a high-end data platform appearance.

Technologies Used

Python : Core programming language Streamlit : Framework used for building the interactive web application/dashboard Pandas : Data manipulation and cleaning, calculating derived metrics (Gls/90, Ast/90) Plotly : Creating rich, interactive, and high-quality data visualizations (bar charts, line graphs, pie charts)

Setup and Installation: Follow these steps to get a local copy of the project running on your machine

Python 3.8+ pip (Python package installer)

Installation Clone the Repository:

git clone https://github.com/[Myriam789/soccerStat-project.git cd SoccerStat-Dashboard

Install Dependencies:

pip install -r requirements.txt

(Note: If a requirements.txt is missing, you can install the necessary libraries manually: pip install streamlit pandas plotly)

Data File: Ensure the primary dataset, top5-players_NEW.csv, is located in the root directory of the project folder.

How to Run the Dashboard To launch the interactive dashboard, run the following command in your terminal from the project's root directory:

streamlit run app.py

The application will automatically open in your web browser, typically at http://localhost:8501.

Data Source The analysis utilizes a dataset named top5-players_NEW.csv, which contains key performance indicators for football players in major leagues (2023/2024 season).

Key Metrics Included:

Pos (Position) Min (Minutes Played) Gls (Goals) Ast (Assists) xG (Expected Goals) xAG (Expected Assists) Comp (Competition/League)

Contributors This project was developed collaboratively by:

Sarah Rosa Myriam

Thank you for checking out our data visualization project!
