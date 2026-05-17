from flask import Flask, request, jsonify
import time
import os

from detectors.rule_detector import RuleDetector
from detectors.semantic_detector import SemanticDetector
from pii.presidio_custom import EnhancedPresidio
from policy.policy_engine import PolicyEngine

app = Flask(__name__)

rule_detector = RuleDetector()
semantic_detector = SemanticDetector()
presidio = EnhancedPresidio()
policy_engine = PolicyEngine('config/gateway_config.yaml')

@app.route("/analyze", methods=["POST"])
def analyze():
    start_time = time.time()
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "No input text provided"}), 400
    
    text = data["text"]

    rule_score, lang = rule_detector.detect(text)
    semantic_result = semantic_detector.analyze(text)

    pii_results = presidio.analyze(text)
   
    decision, risk_score, reason_codes = policy_engine.decide(
        rule_score, semantic_result, pii_results
    )

    safe_text = text
    if decision == "BLOCK":
        safe_text = None
    elif decision == "MASK":
        safe_text = presidio.anonymize(text, pii_results)

    latency = round((time.time() - start_time) * 1000, 2)

    response = {
        "input_id": data.get("input_id", "manual"),
        "language": lang,
        "rule_score": round(rule_score, 3),
        "semantic_score": round(semantic_result['score'], 3),
        "pii_entities": [
            {"type": r.entity_type, "score": round(r.score, 2)} for r in pii_results
        ],
        "final_risk": round(risk_score, 3),
        "decision": decision,
        "safe_text": safe_text,
        "reason_codes": reason_codes,
        "latency_ms": latency
    }
    
    return jsonify(response)

if __name__ == "__main__":
    for folder in ['config', 'detectors', 'pii', 'policy', 'utils', 'data']:
        if not os.path.exists(folder): os.makedirs(folder)
    app.run(port=5000)