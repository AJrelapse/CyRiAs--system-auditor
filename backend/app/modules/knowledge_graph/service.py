import networkx as nx

from app.modules.digital_twin.service import (
    digital_twin_service,
)


SOFTWARE_INTELLIGENCE = {

    "openssh": {
        "cve": "CVE-2024-6387",
        "severity": "Critical",
        "cvss": 9.8,
        "technique": "T1190",
        "technique_name": "Exploit Public Facing Application",
        "control": "Patch Management",
    },

    "apache": {
        "cve": "CVE-2021-41773",
        "severity": "High",
        "cvss": 8.1,
        "technique": "T1190",
        "technique_name": "Exploit Public Facing Application",
        "control": "Web Application Firewall",
    },

    "mysql": {
        "cve": "CVE-2022-21597",
        "severity": "High",
        "cvss": 8.8,
        "technique": "T1078",
        "technique_name": "Valid Accounts",
        "control": "Database Hardening",
    },

    "nginx": {
        "cve": "CVE-2023-44487",
        "severity": "Critical",
        "cvss": 9.8,
        "technique": "T1499",
        "technique_name": "Endpoint Denial of Service",
        "control": "Rate Limiting",
    },

    "windows server": {
        "cve": "CVE-2023-23397",
        "severity": "Critical",
        "cvss": 9.8,
        "technique": "T1068",
        "technique_name": "Privilege Escalation",
        "control": "Windows Update",
    },

    "python": {
        "cve": "CVE-2023-24329",
        "severity": "High",
        "cvss": 7.5,
        "technique": "T1190",
        "technique_name": "Exploit Public Facing Application",
        "control": "Update Python",
    },

    "fastapi": {
        "cve": "CVE-2024-24762",
        "severity": "Medium",
        "cvss": 6.4,
        "technique": "T1190",
        "technique_name": "Exploit Public Facing Application",
        "control": "Dependency Updates",
    },

}


class KnowledgeGraphService:

    def __init__(self):

        self.graph = digital_twin_service.graph

    def build(self):

        self.graph = digital_twin_service.graph

        self.add_network_entry_points()

        self.add_vulnerabilities()

        self.add_attack_techniques()

        self.add_security_controls()

        return {

            "status": "success",

            "nodes": self.graph.number_of_nodes(),

            "edges": self.graph.number_of_edges(),

        }

    def add_network_entry_points(self):

        self.graph.add_node(

            "INTERNET",

            node_type="external",

            label="Internet",

        )

        asset_nodes = [

            node

            for node, attributes

            in self.graph.nodes(data=True)

            if attributes.get("node_type") == "asset"

        ]

        for asset in asset_nodes:

            asset_data = self.graph.nodes[asset]

            exposure = str(

                asset_data.get(
                    "network_exposure",
                    ""
                )

            ).lower()

            if exposure in [

                "public",

                "internet",

                "external",

            ]:

                self.graph.add_edge(

                    "INTERNET",

                    asset,

                    relationship="NETWORK_ACCESS",

                )

    def add_vulnerabilities(self):

        asset_nodes = [

            node

            for node, attributes
            in self.graph.nodes(data=True)

            if attributes.get("node_type") == "asset"

        ]

        for asset in asset_nodes:

            software = self.graph.nodes[asset].get(
                "installed_software",
                [],
            )

            for application in software:

                if isinstance(application, dict):

                    application_name = application.get(
                        "name",
                        ""
                    ).lower()

                else:

                    application_name = str(
                        application
                    ).lower()

                if application_name not in SOFTWARE_INTELLIGENCE:

                    continue

                intelligence = SOFTWARE_INTELLIGENCE[
                    application_name
                ]

                cve = intelligence["cve"]

                self.graph.add_node(

                    cve,

                    node_type="vulnerability",

                    severity=intelligence["severity"],

                    cvss=intelligence["cvss"],

                    label=cve,

                )

                self.graph.add_edge(

                    asset,

                    cve,

                    relationship="AFFECTED_BY",

                )

    def add_attack_techniques(self):

        vulnerability_nodes = [

            node

            for node, attributes

            in self.graph.nodes(data=True)

            if attributes.get("node_type")
            == "vulnerability"

        ]

        for vulnerability in vulnerability_nodes:

            for software in SOFTWARE_INTELLIGENCE.values():

                if software["cve"] != vulnerability:

                    continue

                technique = software["technique"]

                self.graph.add_node(

                    technique,

                    node_type="attack_technique",

                    label=software["technique_name"],

                )

                self.graph.add_edge(

                    vulnerability,

                    technique,

                    relationship="EXPLOITABLE_BY",

                )

    def add_security_controls(self):

        vulnerability_nodes = [

            node

            for node, attributes

            in self.graph.nodes(data=True)

            if attributes.get("node_type")
            == "vulnerability"

        ]

        for vulnerability in vulnerability_nodes:

            for software in SOFTWARE_INTELLIGENCE.values():

                if software["cve"] != vulnerability:

                    continue

                control = software["control"]

                self.graph.add_node(

                    control,

                    node_type="security_control",

                )

                self.graph.add_edge(

                    control,

                    vulnerability,

                    relationship="MITIGATES",

                )

    def get_graph(self):
        graph = digital_twin_service.graph

        nodes = []

        for node_id, attributes in graph.nodes(data=True):

            nodes.append({

                "id": node_id,

                "label": attributes.get(
                    "label",
                    str(node_id)
                ),

                "type": attributes.get(
                    "node_type",
                    "unknown"
                )

            })

        edges = []

        for source, target, attributes in graph.edges(data=True):

            edges.append({

                "source": source,

                "target": target,

                "relationship": attributes.get(
                    "relationship",
                    ""
                )

            })

        return {

            "nodes": nodes,

            "edges": edges

        }

knowledge_graph_service = KnowledgeGraphService()