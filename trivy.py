import json
import logging
import os
from typing import Any, Dict, List, Optional


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_message = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_message)


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

TRIVY_SONARQUBE_SEVERITY: Dict[str, str] = {
    "UNKNOWN": "MINOR",
    "LOW": "MINOR",
    "MEDIUM": "MAJOR",
    "HIGH": "CRITICAL",
    "CRITICAL": "BLOCKER",
}

def determine_type_issue(severity: str) -> str:
    if severity in "BLOCKER":
        return "VULNERABILITY"
    elif severity == ["CRITICAL", "MAJOR", "MINOR"]:
        return "CODE_SMELL"
    else:
        return "BUG"

SOFTWARE_QUALITY_MAPPING: Dict[str, List[Dict[str, str]]] = {
    "VULNERABILITY": [
        {"softwareQuality": "MAINTAINABILITY", "severity": "HIGH"}
    ],
    "BUG": [
        {"softwareQuality": "MAINTAINABILITY", "severity": "MEDIUM"}
    ],
    "CODE_SMELL": [
        {"softwareQuality": "MAINTAINABILITY", "severity": "LOW"}
    ],
}

def get_file_path(result: Dict[str, Any]) -> str:
    file_path = result.get("Target", "unknown_file_path")
    return os.path.relpath(file_path, start="./")


def get_message(misconfiguration: Dict[str, Any]) -> str:
    id_ = misconfiguration.get("ID", "")
    message = misconfiguration.get("Message", "")
    resolution = misconfiguration.get("Resolution", "")
    url = misconfiguration.get("PrimaryURL", "")
    return f"{id_} : {message} => {resolution} ({url})"


def get_text_range(misconfiguration: Dict[str, Any]) -> Dict[str, int]:
    cause_metadata = misconfiguration.get("CauseMetadata", {})
    start_line = int(cause_metadata.get("StartLine", 0))
    end_line = int(cause_metadata.get("EndLine", 0))
    return {"startLine": start_line, "endLine": end_line}


def create_rule(misconfiguration: Dict[str, Any]) -> Dict[str, Any]:
    issue_type = determine_type_issue(
        TRIVY_SONARQUBE_SEVERITY.get(misconfiguration.get("Severity", "UNKNOWN").upper(), "MINOR")
    )
    return {
        "id": misconfiguration.get("ID", ""),
        "name": misconfiguration.get("ID", ""),
        "description": misconfiguration.get("Message", ""),
        "engineId": "Trivy",
        "cleanCodeAttribute": "FORMATTED",
        "impacts": SOFTWARE_QUALITY_MAPPING.get(issue_type, []),
    }


def create_issue(
    result: Dict[str, Any], misconfiguration: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "ruleId": misconfiguration.get("ID", ""),
        "primaryLocation": {
            "filePath": get_file_path(result),
            "message": get_message(misconfiguration),
            "textRange": get_text_range(misconfiguration),
        },
    }


def process_trivy_data(trivy_data: Dict[str, Any]) -> Dict[str, Any]:
    results = trivy_data.get("Results", [])
    rules = {}
    issues = []

    for result in results:
        if result.get("Class") == "config" and result.get("Type") == "terraform":
            misconfigurations = result.get("Misconfigurations", [])
            for misconfiguration in misconfigurations:
                rule_id = misconfiguration.get("ID", "")
                if rule_id not in rules:
                    rules[rule_id] = create_rule(misconfiguration)
                issues.append(create_issue(result, misconfiguration))

    return {"rules": list(rules.values()), "issues": issues}


def load_trivy_data(file_path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding the JSON file.")
        return None


def save_processed_data(processed_data: Dict[str, Any], file_path: str) -> None:
    try:
        with open(file_path, "w") as file:
            json.dump(processed_data, file, indent=4)
        logger.info(f"Processed data saved to '{file_path}'.")
    except IOError:
        logger.error(f"Error saving processed data to '{file_path}'.")


def main() -> None:
    trivy_data = load_trivy_data("trivy-infra-core.json")
    if trivy_data is None:
        return

    processed_data = process_trivy_data(trivy_data)
    save_processed_data(processed_data, "./sonar_report.json")


if __name__ == "__main__":
    main()