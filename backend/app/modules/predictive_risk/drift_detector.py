from typing import Dict, List


class DriftDetector:
    """
    Detects configuration, identity, cloud, and software drift
    between the latest two Digital Twin snapshots.
    """

    def detect(
        self,
        snapshots: List[Dict]
    ) -> Dict[str, Dict]:

        if len(snapshots) < 2:
            return {}

        previous_snapshot = snapshots[-2]
        current_snapshot = snapshots[-1]

        previous_assets = {
            asset["asset_id"]: asset
            for asset in previous_snapshot.get("assets", [])
        }

        current_assets = {
            asset["asset_id"]: asset
            for asset in current_snapshot.get("assets", [])
        }

        drift_results = {}

        for asset_id, current_asset in current_assets.items():

            previous_asset = previous_assets.get(asset_id)

            if previous_asset is None:
                continue

            config_drift = self._configuration_drift(
                previous_asset.get("configuration", {}),
                current_asset.get("configuration", {})
            )

            identity_drift = self._identity_drift(
                previous_asset.get("identity", {}),
                current_asset.get("identity", {})
            )

            cloud_drift = self._cloud_drift(
                previous_asset.get("cloud", {}),
                current_asset.get("cloud", {})
            )

            software_drift = self._software_drift(
                previous_asset.get("installed_software", []),
                current_asset.get("installed_software", [])
            )

            drift_results[asset_id] = {
                "configuration_drift": config_drift,
                "identity_drift": identity_drift,
                "cloud_drift": cloud_drift,
                "software_drift": software_drift,
                "total_drift": (
                    config_drift
                    + identity_drift
                    + cloud_drift
                    + software_drift
                )
            }

        return drift_results

    @staticmethod
    def _configuration_drift(
        previous: Dict,
        current: Dict
    ) -> int:

        changes = 0

        keys = set(previous.keys()) | set(current.keys())

        for key in keys:
            if previous.get(key) != current.get(key):
                changes += 1

        return changes

    @staticmethod
    def _identity_drift(
        previous: Dict,
        current: Dict
    ) -> int:

        changes = 0

        keys = set(previous.keys()) | set(current.keys())

        for key in keys:
            if previous.get(key) != current.get(key):
                changes += 1

        return changes

    @staticmethod
    def _cloud_drift(
        previous: Dict,
        current: Dict
    ) -> int:

        changes = 0

        keys = set(previous.keys()) | set(current.keys())

        for key in keys:
            if previous.get(key) != current.get(key):
                changes += 1

        return changes

    @staticmethod
    def _software_drift(
        previous: List,
        current: List
    ) -> int:

        previous_set = {
            (
                software.get("name"),
                software.get("version")
            )
            for software in previous
            if isinstance(software, dict)
        }

        current_set = {
            (
                software.get("name"),
                software.get("version")
            )
            for software in current
            if isinstance(software, dict)
        }

        return len(previous_set.symmetric_difference(current_set))