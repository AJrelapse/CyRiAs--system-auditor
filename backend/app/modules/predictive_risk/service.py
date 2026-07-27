import json

from sqlalchemy.orm import Session

from app.db.models import DigitalTwinSnapshotDB
from app.modules.digital_twin.service import digital_twin_service

from app.modules.predictive_risk.models import (
    PredictiveRiskResponse
)
from app.modules.predictive_risk.trend_analyzer import (
    TrendAnalyzer
)
from app.modules.predictive_risk.drift_detector import (
    DriftDetector
)
from app.modules.predictive_risk.predictor import (
    Predictor
)


class PredictiveRiskService:

    def __init__(self):

        self.trend_analyzer = TrendAnalyzer()
        self.drift_detector = DriftDetector()
        self.predictor = Predictor()

    def predict(
        self,
        db: Session
    ) -> PredictiveRiskResponse:

        # Build the latest Digital Twin snapshot
        digital_twin_service.build_twin(db)

        snapshots_db = (
            db.query(DigitalTwinSnapshotDB)
            .order_by(
                DigitalTwinSnapshotDB.created_at
            )
            .all()
        )

        if not snapshots_db:

            return PredictiveRiskResponse(
                total_assets=0,
                predictions=[]
            )

        snapshots = []

        for snapshot in snapshots_db:

            graph = json.loads(
                snapshot.graph_data
            )

            assets = []

            for node in graph.get("nodes", []):

                if node.get("node_type") != "asset":
                    continue

                properties = node.get(
                    "properties",
                    {}
                )

                behavioral = properties.get(
                    "behavioral_state",
                    {}
                )

                assets.append({

                    "asset_id":
                        node["node_id"],

                    "current_risk_score":
                        (
                            behavioral.get(
                                "critical_events",
                                0
                            ) * 15
                            +
                            behavioral.get(
                                "high_events",
                                0
                            ) * 8
                            +
                            behavioral.get(
                                "failed_authentications",
                                0
                            ) * 2
                            +
                            behavioral.get(
                                "malware_events",
                                0
                            ) * 10
                        ),

                    "metrics": {

                        "failed_logins":
                            behavioral.get(
                                "failed_authentications",
                                0
                            ),

                        "security_events":
                            behavioral.get(
                                "total_events",
                                0
                            ),

                        "malware_events":
                            behavioral.get(
                                "malware_events",
                                0
                            ),

                        "cpu_usage": 0,

                        "network_connections": 0

                    },

                    "configuration":
                        properties.get(
                            "configuration_metadata",
                            {}
                        ),

                    "identity": {},

                    "cloud": {

                        "resources":
                            properties.get(
                                "cloud_resources",
                                []
                            )

                    },

                    "installed_software":
                        properties.get(
                            "installed_software",
                            []
                        ),

                    "vulnerabilities":
                        properties.get(
                            "vulnerabilities",
                            []
                        )

                })

            snapshots.append({

                "assets": assets

            })

        latest_assets = snapshots[-1]["assets"]

        trends = self.trend_analyzer.analyze(
            snapshots
        )

        drifts = self.drift_detector.detect(
            snapshots
        )

        predictions = self.predictor.predict(
            assets=latest_assets,
            trends=trends,
            drifts=drifts
        )

        return PredictiveRiskResponse(
            total_assets=len(predictions),
            predictions=predictions
        )


predictive_risk_service = PredictiveRiskService()