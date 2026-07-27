export interface DashboardSummary {

    totalAssets: number;

    averageRisk: number;

    criticalAssets: number;

    highestRiskAsset: string;

    assessments: RiskAssessment[];

}

export interface RiskAssessment {

    asset_name: string;

    asset_type: string;

    overall_score: number;

    attack_path_score: number;

    predictive_score: number;

    risk_level: string;

}