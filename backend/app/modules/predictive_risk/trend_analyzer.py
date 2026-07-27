from typing import Dict, List


class TrendAnalyzer:
    """
    Analyzes historical Digital Twin snapshots to identify
    behavioral trends for each asset.
    """

    def analyze(
        self,
        snapshots: List[Dict]
    ) -> Dict[str, Dict]:

        trends = {}

        if len(snapshots) < 2:
            return trends

        for snapshot in snapshots:

            for asset in snapshot.get("assets", []):

                asset_id = asset["asset_id"]

                metrics = asset.get("metrics", {})

                if asset_id not in trends:
                    trends[asset_id] = {
                        "failed_logins": [],
                        "security_events": [],
                        "malware_events": [],
                        "cpu_usage": [],
                        "network_connections": []
                    }

                trends[asset_id]["failed_logins"].append(
                    metrics.get("failed_logins", 0)
                )

                trends[asset_id]["security_events"].append(
                    metrics.get("security_events", 0)
                )

                trends[asset_id]["malware_events"].append(
                    metrics.get("malware_events", 0)
                )

                trends[asset_id]["cpu_usage"].append(
                    metrics.get("cpu_usage", 0)
                )

                trends[asset_id]["network_connections"].append(
                    metrics.get("network_connections", 0)
                )

        trend_results = {}

        for asset_id, values in trends.items():

            trend_results[asset_id] = {
                "failed_login_trend": self._calculate_trend(
                    values["failed_logins"]
                ),
                "security_event_trend": self._calculate_trend(
                    values["security_events"]
                ),
                "malware_trend": self._calculate_trend(
                    values["malware_events"]
                ),
                "cpu_trend": self._calculate_trend(
                    values["cpu_usage"]
                ),
                "network_trend": self._calculate_trend(
                    values["network_connections"]
                )
            }

        return trend_results

    @staticmethod
    def _calculate_trend(
        values: List[float]
    ) -> float:

        if len(values) < 2:
            return 0.0

        first = values[0]
        last = values[-1]

        if first == 0:
            return float(last)

        return round(((last - first) / first) * 100, 2)