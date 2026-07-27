import networkx as nx

from app.modules.knowledge_graph.service import (
    knowledge_graph_service,
)


class AttackPathService:

    def __init__(self):

        self.graph = knowledge_graph_service.graph

    def generate_attack_paths(self):

        self.graph = knowledge_graph_service.graph

        attack_paths = []
        discovered = set()

        internet_nodes = [

            node

            for node, attributes

            in self.graph.nodes(data=True)

            if attributes.get("node_type") == "external"

        ]

        for internet in internet_nodes:

            attack_paths.extend(

                self.find_paths_from_entry(
                    internet,
                    discovered,
                )

            )

        attack_paths.sort(

            key=lambda x: x["risk_score"],

            reverse=True,

        )

        for index, attack in enumerate(

            attack_paths,
            start=1,

        ):

            attack["attack_id"] = (
                f"AP-{index:03d}"
            )

        return {

            "total_paths": len(
                attack_paths
            ),

            "attack_paths": attack_paths,

        }

    def find_paths_from_entry(

        self,

        entry_node,

        discovered,

    ):

        paths = []

        for _, asset, edge_data in self.graph.out_edges(

            entry_node,

            data=True,

        ):

            if (
                edge_data.get("relationship")
                != "NETWORK_ACCESS"
            ):

                continue

            paths.extend(

                self.expand_asset(

                    entry_node,

                    asset,

                    discovered,

                )

            )

        return paths

    def expand_asset(

        self,

        entry,

        asset,

        discovered,

    ):

        results = []

        if not self.graph.has_node(asset):

            return results

        asset_attributes = self.graph.nodes[asset]

        if (
            asset_attributes.get("node_type")
            != "asset"
        ):

            return results

        for _, vulnerability, edge_data in self.graph.out_edges(

            asset,

            data=True,

        ):

            if (
                edge_data.get("relationship")
                != "AFFECTED_BY"
            ):

                continue

            results.extend(

                self.expand_vulnerability(

                    entry,

                    asset,

                    vulnerability,

                    discovered,

                )

            )

        return results

    def expand_vulnerability(

        self,

        entry,

        asset,

        vulnerability,

        discovered,

    ):

        results = []

        techniques = []

        controls = []

        if not self.graph.has_node(vulnerability):

            return results

        vulnerability_attributes = self.graph.nodes[
            vulnerability
        ]

        for _, technique, edge_data in self.graph.out_edges(

            vulnerability,

            data=True,

        ):

            if (
                edge_data.get("relationship")
                != "EXPLOITABLE_BY"
            ):

                continue

            techniques.append(

                {

                    "technique_id": technique,

                    "name": self.graph.nodes[
                        technique
                    ].get(
                        "label",
                        technique,
                    ),

                }

            )

        for control, _, edge_data in self.graph.in_edges(

            vulnerability,

            data=True,

        ):

            if (
                edge_data.get("relationship")
                != "MITIGATES"
            ):

                continue

            controls.append(control)

        path_signature = (

            entry,

            asset,

            vulnerability,

            tuple(

                sorted(

                    t["technique_id"]

                    for t in techniques

                )

            ),

        )

        if path_signature in discovered:

            return results

        discovered.add(path_signature)
        risk_score = self.calculate_risk_score(

            asset,

            vulnerability,

        )

        results.append(

            {

                "entry_point": entry,

                "target_asset": asset,

                "severity": self.calculate_severity(
                    risk_score
                ),

                "risk_score": risk_score,

                "path": [

                    entry,

                    asset,

                    vulnerability,

                    *[
                        technique["technique_id"]
                        for technique in techniques
                    ],

                ],

                "vulnerabilities": [

                    {

                        "cve": vulnerability,

                        "cvss": vulnerability_attributes.get(
                            "cvss",
                            0,
                        ),

                        "severity": vulnerability_attributes.get(
                            "severity",
                            "Unknown",
                        ),

                    }

                ],

                "techniques": techniques,

                "missing_controls": controls,

            }

        )

        return results

    def calculate_risk_score(

        self,

        asset,

        vulnerability,

    ):

        score = 0.0

        asset_node = self.graph.nodes[asset]

        criticality = str(

            asset_node.get(

                "criticality",

                "",

            )

        ).lower()

        if criticality == "critical":

            score += 40

        elif criticality == "high":

            score += 30

        elif criticality == "medium":

            score += 20

        else:

            score += 10

        behavior = asset_node.get(

            "behavioral_state",

            {},

        )

        score += (

            behavior.get(

                "critical_events",

                0,

            )

            * 10

        )

        score += (

            behavior.get(

                "high_events",

                0,

            )

            * 5

        )

        score += (

            behavior.get(

                "failed_authentications",

                0,

            )

            * 2

        )

        score += (

            behavior.get(

                "malware_events",

                0,

            )

            * 8

        )

        vulnerability_node = self.graph.nodes[
            vulnerability
        ]

        score += vulnerability_node.get(

            "cvss",

            0,

        ) * 3

        return round(

            min(

                score,

                100,

            ),

            2,

        )

    def calculate_severity(

        self,

        score,

    ):

        if score >= 85:

            return "Critical"

        if score >= 70:

            return "High"

        if score >= 40:

            return "Medium"

        return "Low"

    def filter_by_asset(
        self,
        asset_id: str,
    ):

        report = self.generate_attack_paths()

        filtered = [

            attack

            for attack in report["attack_paths"]

            if attack["target_asset"] == asset_id

        ]

        return {

            "total_paths": len(filtered),

            "attack_paths": filtered,

        }

    def filter_by_severity(
        self,
        severity: str,
    ):

        report = self.generate_attack_paths()

        filtered = [

            attack

            for attack in report["attack_paths"]

            if attack["severity"].lower()
            == severity.lower()

        ]

        return {

            "total_paths": len(filtered),

            "attack_paths": filtered,

        }

    def top_attack_paths(
        self,
        limit: int = 10,
    ):

        report = self.generate_attack_paths()

        return {

            "total_paths": min(
                limit,
                len(report["attack_paths"]),
            ),

            "attack_paths": report[
                "attack_paths"
            ][:limit],

        }


attack_path_service = AttackPathService()