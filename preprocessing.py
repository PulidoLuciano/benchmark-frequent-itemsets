import pandas as pd

# Cargar el dataset
retail_df = pd.read_excel('./data/online_retail_2.xlsx')

# Limpiar el dataset
retail_df = retail_df[retail_df['UnitPrice'] > 0]
retail_df = retail_df[retail_df['Quantity'] > 0]
retail_df = retail_df[~retail_df["InvoiceNo"].str.contains("C", na=False)]
retail_df = retail_df.drop_duplicates()
retail_df = retail_df[~retail_df['StockCode'].isin(['POST', 'C2', 'DOT', 'M', 'm', 'BANK CHARGES', 'AMAZONFEE', 'S', 'PADS', 'B'])]

# Crear el dataset para los algoritmos con enteros
retail_df['Presence'] = 1
basket = pd.pivot_table(retail_df, index='InvoiceNo', columns='StockCode', values='Presence', aggfunc='max', fill_value=0)

# Crear el dataset para los algoritmos con booleanos
retail_df['Presence'] = True
boolean_basket = pd.pivot_table(retail_df, index='InvoiceNo', columns='StockCode', values='Presence', aggfunc='max', fill_value=False)

# Guardar los datasets
basket.to_csv('./data/basket.csv', index=True)
boolean_basket.to_csv('./data/boolean_basket.csv', index=True)

print('Dataset generados con éxito.')
print(basket.head())
print(boolean_basket.head())