import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error


class OccupancyAgent:

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.model = None

    def load_data(self):
        """Load and prepare occupancy data."""
        self.data = pd.read_csv(self.data_path)

        self.data["timestamp"] = pd.to_datetime(
            self.data["timestamp"]
        )

        # Calculate space utilization
        self.data["utilization"] = (
            self.data["occupancy"] / self.data["capacity"]
        ) * 100

        return self.data

    def analyze_occupancy(self):
        """Analyze occupancy and identify overcrowding."""
        df = self.data.copy()

        df["status"] = "Normal"

        df.loc[
            df["utilization"] >= 80,
            "status"
        ] = "High Utilization"

        df.loc[
            df["utilization"] >= 100,
            "status"
        ] = "Overcrowded"

        return {
            "total_records": len(df),
            "average_occupancy": df["occupancy"].mean(),
            "peak_occupancy": df["occupancy"].max(),
            "average_utilization": df["utilization"].mean(),
            "overcrowded_count": (
                df["status"] == "Overcrowded"
            ).sum(),
            "high_utilization_count": (
                df["status"] == "High Utilization"
            ).sum()
        }

    def get_occupancy_status(self):
        """Return occupancy status for every record."""
        df = self.data.copy()

        df["status"] = "Normal"

        df.loc[
            df["utilization"] >= 80,
            "status"
        ] = "High Utilization"

        df.loc[
            df["utilization"] >= 100,
            "status"
        ] = "Overcrowded"

        return df

    def forecast_occupancy(self):
        """Forecast occupancy using a Random Forest model."""

        df = self.data.copy()

        # Sort chronologically
        df = df.sort_values(
            "timestamp"
        ).reset_index(drop=True)

        # Time-based features
        df["hour"] = df["timestamp"].dt.hour
        df["day"] = df["timestamp"].dt.day
        df["month"] = df["timestamp"].dt.month
        df["day_of_week"] = df["timestamp"].dt.dayofweek

        # Cyclical time features
        df["hour_sin"] = __import__("numpy").sin(
            2 * __import__("numpy").pi * df["hour"] / 24
        )

        df["hour_cos"] = __import__("numpy").cos(
            2 * __import__("numpy").pi * df["hour"] / 24
        )

        # Capacity is an important factor in occupancy forecasting
        features = [
            "hour",
            "day",
            "month",
            "day_of_week",
            "hour_sin",
            "hour_cos",
            "capacity"
        ]

        X = df[features]
        y = df["occupancy"]

        # First 80% = training data
        # Last 20% = unseen test data
        split_index = int(len(df) * 0.8)

        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]

        # Train Random Forest
        self.model = RandomForestRegressor(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=1,
            random_state=42
        )

        self.model.fit(
            X_train,
            y_train
        )

        # Predict unseen test data
        test_predictions = self.model.predict(
            X_test
        )

        # Calculate accuracy
        mape = mean_absolute_percentage_error(
            y_test,
            test_predictions
        )

        accuracy = max(
            0,
            (1 - mape) * 100
        )

        # Predictions for dashboard
        df["predicted_occupancy"] = (
            self.model.predict(X)
        )

        return df, accuracy

    def generate_insights(self):
        """Generate occupancy-related insights."""
        results = self.analyze_occupancy()

        insights = []

        if results["overcrowded_count"] > 0:
            insights.append(
                f"{results['overcrowded_count']} "
                "overcrowded occupancy records detected."
            )

        if results["high_utilization_count"] > 0:
            insights.append(
                f"{results['high_utilization_count']} "
                "records show high space utilization."
            )

        if results["average_utilization"] < 50:
            insights.append(
                "Average space utilization is relatively low."
            )
        else:
            insights.append(
                "Facility space is being actively utilized."
            )

        return insights