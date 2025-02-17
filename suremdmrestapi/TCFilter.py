import pandas as pd
import re

df = pd.read_csv(r'C:\Users\2527123\Documents\Unicon\Scout\Report\AllDevices.csv')
df_filtered = df[df['Name and path'].str.contains(r'/DSG/DK/Foetex/', regex=True, na=False)].copy()
df_filtered.loc[:, 'Store Number'] = df_filtered['Name and path'].str.extract(r'/DSG/DK/Foetex/(\d{4})')[0]
grouped = df_filtered.groupby(['Store Number', 'Device type']).size().reset_index(name='Count')
output_file = r'C:\certificates\openssl\output.csv'                
grouped.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
