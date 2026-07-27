from sqlalchemy.orm import Session

from app.modules.attack_path.service import (
    attack_path_service,
)

from app.modules.predictive_risk.service import (
    predictive_risk_service,
)

from app.modules.digital_twin.service import (
    digital_twin_service,
)

from app.modules.knowledge_graph.service import (
    knowledge_graph_service,
)

from app.modules.risk_assessment.models import (
    AssetRiskAssessment,
    RiskAssessmentResponse,
    RiskRecommendation,
)


class RiskAssessmentService:

    def __init__(self):
        pass

    def assess(
        self,
        db: Session,
    ) -> RiskAssessmentResponse:

        # Ensure the latest Digital Twin and Knowledge Graph
        # are available before calculating attack paths.
        digital_twin_service.build_twin(db)
        knowledge_graph_service.build()

        prediction_report = (
            predictive_risk_service.predict(db)
        )

        attack_report = (
            attack_path_service.generate_attack_paths()
        )

        attack_scores = {}

        for attack in attack_report["attack_paths"]:

            asset = attack["target_asset"]

            score = attack["risk_score"]

            attack_scores[asset] = max(

                attack_scores.get(asset, 0),

                score,

            )

        assessments = []

        total_score = 0

        highest_asset = None

        highest_score = -1

        for prediction in prediction_report.predictions:

            asset = prediction.asset_id

            predictive_score = (
                prediction.predicted_score
            )

            attack_score = attack_scores.get(
                asset,
                0,
            )
            print(
                "Prediction asset:",
                asset,
                "| Attack score:",
                attack_score,
            )

            graph = digital_twin_service.graph

            if graph.has_node(asset):

                criticality = str(

                    graph.nodes[asset].get(
                        "criticality",
                        "low",
                    )

                ).lower()

                behavior = graph.nodes[asset].get(
                    "behavioral_state",
                    {},
                )

            else:

                criticality = "low"

                behavior = {}

            criticality_score = (
                self.calculate_criticality_score(
                    criticality
                )
            )

            behavioral_score = (
                self.calculate_behavior_score(
                    behavior
                )
            )

            overall_score = round(

                (
                    predictive_score * 0.35
                    +
                    attack_score * 0.35
                    +
                    criticality_score * 0.15
                    +
                    behavioral_score * 0.15
                ),

                2,

            )

            risk_level = self.get_risk_level(
                overall_score
            )

            recommendations = (
                self.generate_recommendations(

                    predictive_score,

                    attack_score,

                    criticality_score,

                    behavioral_score,

                )
            )

            assessments.append(

                AssetRiskAssessment(

                    asset_id=asset,

                    overall_score=overall_score,

                    risk_level=risk_level,

                    predictive_score=round(
                        predictive_score,
                        2,
                    ),

                    attack_path_score=round(
                        attack_score,
                        2,
                    ),

                    criticality_score=round(
                        criticality_score,
                        2,
                    ),

                    behavioral_score=round(
                        behavioral_score,
                        2,
                    ),

                    recommendations=recommendations,

                )

            )

            total_score += overall_score

            if overall_score > highest_score:

                highest_score = overall_score

                highest_asset = asset

        assessments.sort(

            key=lambda x: x.overall_score,

            reverse=True,

        )

        average = 0

        if assessments:

            average = round(

                total_score
                /
                len(assessments),

                2,

            )
        attack_report = attack_path_service.generate_attack_paths()

        print(attack_report)

        print("=" * 60)
        print("ATTACK REPORT")
        print(attack_report)

        attack_scores = {}

        for attack in attack_report["attack_paths"]:
            asset = attack["target_asset"]
            score = attack["risk_score"]

            attack_scores[asset] = max(
                attack_scores.get(asset, 0),
                score,
            )

        print("ATTACK SCORES")
        print(attack_scores)
        print("=" * 60)

        return RiskAssessmentResponse(

            total_assets=len(assessments),

            average_risk_score=average,

            highest_risk_asset=highest_asset,

            assessments=assessments,

        )

    def calculate_criticality_score(
        self,
        criticality: str,
    ):

        criticality = criticality.lower()

        if criticality == "critical":
            return 100

        if criticality == "high":
            return 75

        if criticality == "medium":
            return 50

        return 25

    def calculate_behavior_score(
        self,
        behavior: dict,
    ):

        score = 0

        score += (
            behavior.get(
                "critical_events",
                0,
            )
            * 20
        )

        score += (
            behavior.get(
                "high_events",
                0,
            )
            * 10
        )

        score += (
            behavior.get(
                "failed_authentications",
                0,
            )
            * 5
        )

        score += (
            behavior.get(
                "malware_events",
                0,
            )
            * 15
        )

        return min(score, 100)

    def get_risk_level(
        self,
        score: float,
    ):

        if score >= 85:
            return "Critical"

        if score >= 70:
            return "High"

        if score >= 40:
            return "Medium"

        return "Low"

    def generate_recommendations(

        self,

        predictive_score,

        attack_score,

        criticality_score,

        behavioral_score,

    ):

        recommendations = []

        priority = 1

        if attack_score >= 70:

            recommendations.append(

                RiskRecommendation(

                    priority=priority,

                    recommendation=(
                        "Immediately remediate exposed vulnerabilities."
                    ),

                )

            )

            priority += 1

        if predictive_score >= 60:

            recommendations.append(

                RiskRecommendation(

                    priority=priority,

                    recommendation=(
                        "Investigate abnormal behavioral trends."
                    ),

                )

            )

            priority += 1

        if behavioral_score >= 70:

            recommendations.append(

                RiskRecommendation(

                    priority=priority,

                    recommendation=(
                        "Review security events and authentication failures."
                    ),

                )

            )

            priority += 1

        if criticality_score >= 75:

            recommendations.append(

                RiskRecommendation(

                    priority=priority,

                    recommendation=(
                        "Increase monitoring frequency for this asset."
                    ),

                )

            )

            priority += 1

        if not recommendations:

            recommendations.append(

                RiskRecommendation(

                    priority=1,

                    recommendation=(
                        "Continue routine monitoring."
                    ),

                )

            )

        return recommendations


risk_assessment_service = RiskAssessmentService()