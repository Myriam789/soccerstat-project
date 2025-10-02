import pandas as pd


df = pd.read_csv('top5-players.csv')

df.drop_duplicates(inplace=True)

stats_cols_to_fill = ['xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR',
                      'Gls_90', 'Ast_90', 'G+A_90', 'G-PK_90', 'G+A-PK_90',
                      'xG_90', 'xAG_90', 'xG+xAG_90', 'npxG_90', 'npxG+xAG_90']
df[stats_cols_to_fill] = df[stats_cols_to_fill].fillna(0)


df['Pos'].fillna('Unknown', inplace=True)


MIN_MINUTES = 450
df_cleaned = df[df['Min'] >= MIN_MINUTES].copy()
df_cleaned.reset_index(drop=True, inplace=True)


df_cleaned.to_csv('top5-players_CLEANED.csv', index=False)

print("\n'top5-players_CLEANED.csv' créé.")
