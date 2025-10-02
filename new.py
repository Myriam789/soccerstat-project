import pandas as pd

df = pd.read_csv('top5-players_CLEANED.csv')

df['Gls_Per_Match'] = df.apply(
    lambda row: row['Gls'] / row['MP'] if row['MP'] > 0 else 0,
    axis=1
)

df['Ast_Per_Match'] = df.apply(
    lambda row: row['Ast'] / row['MP'] if row['MP'] > 0 else 0,
    axis=1
)

df.to_csv('top5-players_NEW.csv', index=False)
