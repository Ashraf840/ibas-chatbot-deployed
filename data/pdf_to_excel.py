import camelot
import pandas as pd
# extract all the tables in the PDF file
tables = camelot.read_pdf("./FAQ.pdf",  pages='all')

print("total tables:", tables.n)

dfs = []
for i in range(tables.n):
    df = tables[i].df
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    print(df.columns)
    dfs.append(df)

result_df = pd.concat(dfs)


result_df.to_csv('./FAQ.csv', index=False)