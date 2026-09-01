from sklearn.ensemble import IsolationForest
FEATURES=["electricity_kwh","water_liters","temperature_c","hvac_usage","occupancy"]
def detect_anomalies(df, contamination=0.083):
    result=df.copy()
    model=IsolationForest(contamination=contamination,random_state=42)
    pred=model.fit_predict(result[FEATURES])
    result["prediction"]=["Anomaly" if x==-1 else "Normal" for x in pred]
    return result,model
