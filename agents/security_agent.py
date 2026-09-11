import pandas as pd


class SecurityAgent:

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        """Load and prepare security event data."""

        self.data = pd.read_csv(
            self.data_path
        )

        self.data["timestamp"] = pd.to_datetime(
            self.data["timestamp"]
        )

        return self.data

    def analyze_security(self):
        """Analyze security events and identify risks."""

        df = self.data.copy()

        # Default classification
        df["security_status"] = "Normal"

        # Mark denied access as security alerts
        df.loc[
            df["access_status"] == "Denied",
            "security_status"
        ] = "Security Alert"

        # Mark unknown persons as high-risk events
        df.loc[
            df["person_type"] == "Unknown",
            "security_status"
        ] = "High Risk"

        # Count security events
        total_events = len(df)

        granted_events = (
            df["access_status"] == "Granted"
        ).sum()

        denied_events = (
            df["access_status"] == "Denied"
        ).sum()

        unauthorized_events = (
            df["event_type"] == "Unauthorized Access"
        ).sum()

        visitor_events = (
            df["person_type"] == "Visitor"
        ).sum()

        return {
            "total_events": total_events,
            "granted_events": granted_events,
            "denied_events": denied_events,
            "unauthorized_events": unauthorized_events,
            "visitor_events": visitor_events
        }

    def get_security_alerts(self):
        """Return security events requiring attention."""

        df = self.data.copy()

        alerts = df[
            (df["access_status"] == "Denied")
            |
            (df["person_type"] == "Unknown")
        ].copy()

        return alerts

    def get_security_status(self):
        """Return security status for every event."""

        df = self.data.copy()

        df["security_status"] = "Normal"

        df.loc[
            df["access_status"] == "Denied",
            "security_status"
        ] = "Security Alert"

        df.loc[
            df["person_type"] == "Unknown",
            "security_status"
        ] = "High Risk"

        return df

    def generate_security_insights(self):
        """Generate security-related insights."""

        results = self.analyze_security()

        insights = []

        if results["unauthorized_events"] > 0:
            insights.append(
                f"{results['unauthorized_events']} unauthorized access attempts detected."
            )

        if results["denied_events"] > 0:
            insights.append(
                f"{results['denied_events']} access requests were denied."
            )

        if results["visitor_events"] > 0:
            insights.append(
                f"{results['visitor_events']} visitor access events recorded."
            )

        if results["granted_events"] > 0:
            insights.append(
                f"{results['granted_events']} legitimate access events were granted."
            )

        return insights