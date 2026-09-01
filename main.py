from agents.energy_agent import EnergyAgent
a=EnergyAgent("data/energy_data.csv"); a.load_data()
print("Analytics:",a.analyze_energy()); print("Anomalies:",len(a.detect_energy_anomalies()))
print("Validation accuracy:",round(a.evaluate_accuracy(),2),"%")
for r in a.generate_recommendations(): print("-",r)
