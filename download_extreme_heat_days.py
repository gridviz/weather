import pandas as pd
import urllib.request, json

today = pd.to_datetime("today").strftime("%Y-%m-%d")

json_url = "https://services3.arcgis.com/0Fs3HcaFfvzXvm7w/arcgis/rest/services/Indicators_ExtremeHeat/FeatureServer/0/query?f=json&where=1%3D1&outFields=Indicator_Name%2CIndicator_Value%2CLink%2CSource%2CTimeseries_Data%2CTimeseries_Label%2CTimeseries_Date%2CTopic"

with urllib.request.urlopen(json_url) as url:
    data = json.loads(url.read().decode())


src = pd.DataFrame(
    {
        "date": data["features"][0]["attributes"]["Timeseries_Date"].split(","),
        "total": data["features"][0]["attributes"]["Timeseries_Data"].split(","),
    }
)

src["date"] = pd.to_datetime(src["date"]).dt.strftime('%Y-%m-%d')

df_start = pd.read_csv('data/processed/people_in_excessive_heat_historic.csv')

df_start["date"] = pd.to_datetime(df_start["date"]).dt.strftime('%Y-%m-%d')

df = pd.concat([src, df_start]).drop_duplicates(subset='date').sort_values('date', ascending=False).reset_index(drop=True)

df["date"] = pd.to_datetime(df["date"])
df["total"] = df["total"].astype(int)

df['pop'] = 331449281
df['pop_share'] = ((df['total'] / df['pop'])*100).round(2)

df.to_csv(f"data/processed/people_in_excessive_heat_{today}.csv", index=False)
df.to_csv(f"data/processed/people_in_excessive_heat_latest.csv", index=False)

df['date']= df['date'].astype(str)

df.to_json(f"data/processed/people_in_excessive_heat_{today}.json", indent=4, orient='records')
df.to_json(f"data/processed/people_in_excessive_heat_latest.json", indent=4, orient='records')
df.to_csv(f"data/processed/people_in_excessive_heat_historic.csv", index=False)
