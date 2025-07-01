import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# This script reads a CSV file containing unemployment data and Inflation data and plots it.
# and explores what conclusions can be drawn from the data.

unempData = pd.read_csv('C:\\Unemp Inf Data\\API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_3518.csv', skiprows=4)
infData = pd.read_csv('C:\\Unemp Inf Data\\API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_62.csv', skiprows=4)

print(unempData.head())
print(infData.head())


# Keep only useful columns: 'Country Name', 'Country Code', and all years
unempData = unempData.drop(columns=["Indicator Name", "Indicator Code"])

# Melt the DataFrame from wide to long format
unemp_long_df = pd.melt(
    unempData,
    id_vars=["Country Name", "Country Code"],
    var_name="Year",
    value_name="Unemployment"
)

# Rename for clarity
unemp_long_df.rename(columns={"Country Name": "Country"}, inplace=True)

# Convert 'Year' to numeric, drop NaNs if needed
unemp_long_df["Year"] = pd.to_numeric(unemp_long_df["Year"], errors='coerce')
unemp_long_df.dropna(subset=["Unemployment", "Year"], inplace=True)

# Preview
print(unemp_long_df.head())

# Now we will do the same for inflation data
# Keep only useful columns: 'Country Name', 'Country Code', and all years
infData = infData.drop(columns=["Indicator Name", "Indicator Code"])

# Melt the DataFrame from wide to long format
inf_long_df = pd.melt(
    infData,
    id_vars=["Country Name", "Country Code"],
    var_name="Year",
    value_name="Inflation"
)

# Rename for clarity
inf_long_df.rename(columns={"Country Name": "Country"}, inplace=True)

# Convert 'Year' to numeric, drop NaNs if needed
inf_long_df["Year"] = pd.to_numeric(unemp_long_df["Year"], errors='coerce')
inf_long_df.dropna(subset=["Inflation", "Year"], inplace=True)

# Preview
print(inf_long_df.head())



# Merge the datasets on 'Country' and 'Year'
combined_df = pd.merge(inf_long_df, unemp_long_df, on=['Country', 'Year'])

# Now combined_df has inflation and unemployment in the same table
print(combined_df.head())

## Plotting the data for Poland
# Filter for Poland
poland_df = combined_df[combined_df["Country"] == "Poland"]


# Plotting the inflation data for Poland
plt.plot(poland_df["Year"], poland_df["Inflation"], marker='o')
plt.title("Inflation in Poland Over Time")
plt.xlabel("Year")
plt.ylabel("Inflation (%)")
plt.grid(True)
plt.show()

# Plotting the unemployment data for Poland
plt.plot(poland_df["Year"], poland_df["Unemployment"], marker='o', color='orange')
plt.title("Unemployment in Poland Over Time")   
plt.xlabel("Year")
plt.ylabel("Unemployment (%)")
plt.grid(True)
plt.show()

# Scatter plot of Inflation vs Unemployment in Poland
plt.scatter(poland_df["Inflation"], poland_df["Unemployment"], color='green')
plt.title("Inflation vs Unemployment in Poland")
plt.xlabel("Inflation (%)")
plt.ylabel("Unemployment (%)")
plt.grid(True)
plt.show()

#Now we can analyze various interesting statistics from the data.
combined_df_sorted = combined_df.sort_values(by=["Country", "Year"])
combined_df_sorted["Unemployment change"] = combined_df_sorted.groupby("Country")["Unemployment"].diff()
combined_df_sorted["Inflation change"] = combined_df_sorted.groupby("Country")["Inflation"].diff()

#The following code will find the top 10 spikes in unemployment and inflation changes across all countries.
top_spikes_Unemp = combined_df_sorted.sort_values(by="Unemployment change", ascending=False).head(10)
print(top_spikes_Unemp)

top_spikes_Inf = combined_df_sorted.sort_values(by="Inflation change", ascending=False).head(10)
print(top_spikes_Inf)