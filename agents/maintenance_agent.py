import pandas as pd


class MaintenanceAgent:

    def __init__(self, data):
        self.data = data

    def calculate_health_score(self, row):
        score = 100

        # Temperature impact
        if row["temperature_c"] > 70:
            score -= 30
        elif row["temperature_c"] > 50:
            score -= 15
        elif row["temperature_c"] > 40:
            score -= 5

        # Vibration impact
        if row["vibration"] > 10:
            score -= 30
        elif row["vibration"] > 6:
            score -= 15
        elif row["vibration"] > 4:
            score -= 5

        # Pressure impact
        if row["pressure"] < 80:
            score -= 25
        elif row["pressure"] < 90:
            score -= 10

        return max(score, 0)

    def analyze_assets(self):
        df = self.data.copy()

        # Calculate equipment health score
        df["health_score"] = df.apply(
            self.calculate_health_score,
            axis=1
        )

        # Predict maintenance priority
        def maintenance_prediction(score):
            if score < 50:
                return "Immediate Maintenance"
            elif score < 75:
                return "Maintenance Required"
            elif score < 90:
                return "Monitor Closely"
            else:
                return "Healthy"

        df["maintenance_prediction"] = df["health_score"].apply(
            maintenance_prediction
        )

        # Generate alerts
        df["maintenance_alert"] = df["maintenance_prediction"].apply(
            lambda x: "ALERT" if x in [
                "Immediate Maintenance",
                "Maintenance Required"
            ] else "No Alert"
        )

        return df