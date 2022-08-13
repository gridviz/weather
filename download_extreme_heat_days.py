import pandas as pd
import urllib.request, json

today = pd.to_datetime("today").strftime("%Y-%m-%d")

json_url = "https://services3.arcgis.com/0Fs3HcaFfvzXvm7w/arcgis/rest/services/Indicators_ExtremeHeat/FeatureServer/0/query?f=json&where=1%3D1&outFields=Indicator_Name%2CIndicator_Value%2CLink%2CSource%2CTimeseries_Data%2CTimeseries_Label%2CTimeseries_Date%2CTopic"

with urllib.request.urlopen(json_url) as url:
    data = json.loads(url.read().decode())


df = pd.DataFrame(
    {
        "date": data["features"][0]["attributes"]["Timeseries_Date"].split(","),
        "total": data["features"][0]["attributes"]["Timeseries_Data"].split(","),
    }
)

df["date"] = pd.to_datetime(df["date"])
df["total"] = df["total"].astype(int)

df.to_csv(f"data/processed/people_in_excessive_heat_{today}.csv", index=False)
df.to_csv(f"data/processed/people_in_excessive_heat_latest.csv", index=False)