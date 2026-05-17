import yaml

class PolicyEngine:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def decide(self, rule_score, semantic_result, pii_results):
        semantic_score = semantic_result.get('score', 0)
        attack_type = semantic_result.get('attack_type')
        t = self.config['thresholds']
        
        base_risk = max(rule_score, semantic_score)
        
        pii_entities = [r.entity_type for r in pii_results]
        high_risk_pii = ["API_KEY", "INTERNAL_ID", "CNIC"]
        force_block_pii = any(e in pii_entities for e in high_risk_pii)

        reasons = []
        if rule_score > 0.5: reasons.append("HEURISTIC_MATCH")
        if semantic_score > 0.5: reasons.append(f"SEMANTIC_{attack_type}" if attack_type else "SEMANTIC_ANOMALY")
        if pii_results: reasons.append("PII_DETECTED")

        if base_risk >= t['injection_block'] or force_block_pii:
            return "BLOCK", 1.0, reasons
        elif base_risk >= t['injection_warn'] or len(pii_results) > 0:
            return "MASK", base_risk, reasons
        else:
            return "ALLOW", base_risk, ["SAFE"]