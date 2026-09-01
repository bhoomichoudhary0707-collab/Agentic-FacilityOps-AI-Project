import pandas as pd
from utils.anomaly_detection import detect_anomalies
class EnergyAgent:
    def __init__(self,data_path): self.data_path=data_path; self.data=None
    def load_data(self):
        self.data=pd.read_csv(self.data_path); self.data["timestamp"]=pd.to_datetime(self.data["timestamp"]); return self.data
    def analyze_energy(self):
        return {"total_energy":float(self.data.electricity_kwh.sum()),"average_energy":float(self.data.electricity_kwh.mean()),"peak_energy":float(self.data.electricity_kwh.max())}
    def detect_energy_anomalies(self):
        self.data,self.model=detect_anomalies(self.data); return self.data[self.data.prediction=="Anomaly"]
    def evaluate_accuracy(self): return float((self.data.prediction==self.data.label).mean()*100)
    def generate_recommendations(self):
        rec=[]; avg=self.data.electricity_kwh.mean()
        if len(self.data[(self.data.electricity_kwh>avg*1.5)&(self.data.occupancy<25)]): rec.append("High energy usage during low occupancy detected. Reduce HVAC and lighting automatically.")
        if self.data.hvac_usage.mean()>40: rec.append("HVAC usage is high. Review temperature setpoints and operating schedules.")
        return rec or ["No major efficiency issue found. Continue monitoring peak-hour consumption."]
