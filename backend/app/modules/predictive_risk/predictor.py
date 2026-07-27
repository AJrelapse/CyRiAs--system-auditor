from typing import Dict, List

from app.modules.predictive_risk.models import (
    AssetPrediction,
    PredictionReason
)


class Predictor:

    BEHAVIOR_WEIGHT = 0.15
    DRIFT_WEIGHT = 2.5
    VULNERABILITY_WEIGHT = 5.0
    MAX_SCORE = 100

    def predict(
        self,
        assets: List[Dict],
        trends: Dict[str, Dict],
        drifts: Dict[str, Dict]
    ) -> List[AssetPrediction]:

        predictions = []

        for asset in assets:

            asset_id = asset["asset_id"]

            trend = trends.get(asset_id, {})
            drift = drifts.get(asset_id, {})

            current_score = float(
                asset.get("current_risk_score", 0)
            )

            reasons = []

            predicted_score = current_score

            predicted_score += self._behavior_score(
                trend,
                reasons
            )

            predicted_score += self._drift_score(
                drift,
                reasons
            )

            predicted_score += self._vulnerability_score(
                asset,
                reasons
            )

            predicted_score = min(
                self.MAX_SCORE,
                round(predicted_score, 2)
            )

            confidence = self._confidence(
                reasons
            )

            predictions.append(

                AssetPrediction(

                    asset_id=asset_id,

                    current_score=current_score,

                    predicted_score=predicted_score,

                    confidence=confidence,

                    prediction_window="24 Hours",

                    risk_level=self._risk_level(
                        predicted_score
                    ),

                    reasons=reasons

                )

            )

        predictions.sort(
            key=lambda x: x.predicted_score,
            reverse=True
        )

        return predictions

    def _behavior_score(
        self,
        trend: Dict,
        reasons: List[PredictionReason]
    ) -> float:

        score = 0.0

        metrics = {

            "failed_login_trend":
                "Increasing failed login attempts",

            "security_event_trend":
                "Increase in security events",

            "malware_trend":
                "Increase in malware detections",

            "cpu_trend":
                "Abnormal CPU utilization",

            "network_trend":
                "Increase in network connections"

        }

        for key, description in metrics.items():

            value = trend.get(key, 0)

            if value > 0:

                contribution = (
                    value *
                    self.BEHAVIOR_WEIGHT
                )

                score += contribution

                reasons.append(

                    PredictionReason(

                        category="Behavior",

                        description=description,

                        score=round(
                            contribution,
                            2
                        )

                    )

                )

        return score

    def _drift_score(
        self,
        drift: Dict,
        reasons: List[PredictionReason]
    ) -> float:

        score = 0.0

        categories = [

            (
                "configuration_drift",
                "Configuration Drift"
            ),

            (
                "identity_drift",
                "Identity Drift"
            ),

            (
                "cloud_drift",
                "Cloud Drift"
            ),

            (
                "software_drift",
                "Software Drift"
            )

        ]

        for key, description in categories:

            changes = drift.get(key, 0)

            if changes > 0:

                contribution = (
                    changes *
                    self.DRIFT_WEIGHT
                )

                score += contribution

                reasons.append(

                    PredictionReason(

                        category="Drift",

                        description=description,

                        score=round(
                            contribution,
                            2
                        )

                    )

                )

        return score

    def _vulnerability_score(
        self,
        asset: Dict,
        reasons: List[PredictionReason]
    ) -> float:

        vulnerabilities = asset.get(
            "vulnerabilities",
            []
        )

        if not vulnerabilities:
            return 0

        score = (
            len(vulnerabilities)
            * self.VULNERABILITY_WEIGHT
        )

        reasons.append(

            PredictionReason(

                category="Vulnerability",

                description="Known vulnerabilities detected",

                score=round(
                    score,
                    2
                )

            )

        )

        return score

    @staticmethod
    def _risk_level(
        score: float
    ) -> str:

        if score >= 90:
            return "Critical"

        if score >= 70:
            return "High"

        if score >= 40:
            return "Medium"

        return "Low"

    @staticmethod
    def _confidence(
        reasons: List[PredictionReason]
    ) -> float:

        confidence = (
            0.5 +
            (len(reasons) * 0.08)
        )

        return round(
            min(confidence, 0.99),
            2
        )