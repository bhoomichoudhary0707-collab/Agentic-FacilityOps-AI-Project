import pandas as pd


class CostOptimizationAgent:

    def __init__(
        self,
        energy_data,
        maintenance_data,
        occupancy_data
    ):
        self.energy_data = energy_data
        self.maintenance_data = maintenance_data
        self.occupancy_data = occupancy_data

    def analyze_costs(self):
        """Analyze operational cost indicators."""

        energy_cost = self.energy_data["electricity_kwh"].sum() * 8

        maintenance_cost = (
            self.maintenance_data["status"]
            .isin(["Maintenance Required", "Immediate Maintenance"])
            .sum()
            * 5000
        )

        average_utilization = (
            self.occupancy_data["utilization"].mean()
        )

        potential_energy_saving = energy_cost * 0.10

        potential_maintenance_saving = maintenance_cost * 0.15

        total_savings = (
            potential_energy_saving
            + potential_maintenance_saving
        )

        return {
            "energy_cost": energy_cost,
            "maintenance_cost": maintenance_cost,
            "average_utilization": average_utilization,
            "potential_energy_saving": potential_energy_saving,
            "potential_maintenance_saving": potential_maintenance_saving,
            "total_potential_savings": total_savings
        }

    def generate_recommendations(self):
        """Generate cost-saving recommendations."""

        results = self.analyze_costs()

        recommendations = []

        if results["potential_energy_saving"] > 0:
            recommendations.append(
                "Optimize energy consumption during high-usage periods."
            )

        if results["potential_maintenance_saving"] > 0:
            recommendations.append(
                "Prioritize maintenance of assets requiring attention "
                "to reduce potential downtime costs."
            )

        if results["average_utilization"] < 60:
            recommendations.append(
                "Review under-utilized facility spaces for better "
                "resource allocation."
            )
        else:
            recommendations.append(
                "Optimize space utilization during high-demand periods."
            )

        return recommendations