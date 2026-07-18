from dataclasses import dataclass
from typing import Any, Protocol
import logging

class OliviaAIProtocol(Protocol):
    # define what you actually need from olivia_ai
    def infer(self, *args, **kwargs) -> Any: ...

@dataclass(frozen=True)
class EnforcementResult:
    compliance_status: Any
    violation_alerts: Any
    corrections: Any

class GlobalStrategicSecurityFramework:
    def __init__(self, olivia_ai: OliviaAIProtocol):
        self.logger = logging.getLogger(__name__)
        # inject dependencies explicitly so you can mock them
        self.treaty_enforcement = TreatyEnforcement(olivia_ai)
        self.resource_allocation = PredictiveResourceAllocation(olivia_ai)
        self.counter_intelligence = AutonomousCounterIntelligence(olivia_ai)

    def enforce_treaty(self, treaty_parameters, monitored_entities) -> EnforcementResult:
        try:
            compliance_status = self.treaty_enforcement.monitor_treaty_compliance(
                treaty_parameters, monitored_entities
            )
            violation_alerts = self.treaty_enforcement.generate_violation_alerts(compliance_status)
            corrections = self.treaty_enforcement.propose_corrections(violation_alerts)
            
            # CRITICAL: don't auto-apply corrections, return for human review
            self.logger.info("Treaty check completed", extra={"alerts": len(violation_alerts or [])})
            return EnforcementResult(compliance_status, violation_alerts, corrections)
        except Exception as e:
            self.logger.exception("enforce_treaty failed")
            raise

    def allocate_conflict_resources(self, conflict_parameters):
        # Same pattern: analyze -> plan -> monitor, but keep plan as proposal
        resource_analysis = self.resource_allocation.analyze_conflict_data(conflict_parameters)
        allocation_plan = self.resource_allocation.allocate_resources(resource_analysis)
        usage_logs = self.resource_allocation.monitor_resource_usage(allocation_plan)
        return {
            "resource_analysis": resource_analysis, 
            "allocation_plan": allocation_plan, 
            "usage_logs": usage_logs,
            "requires_approval": True
        }

    def secure_high_threat_zones(self, high_threat_zones, threat_data):
        deployment_status = self.counter_intelligence.deploy_counterintel_units(high_threat_zones)
        detection_results = self.counter_intelligence.detect_hostile_intelligence(threat_data)
        # Separate detection from action
        return {
            "deployment_status": deployment_status,
            "detection_results": detection_results,
            # Don't call neutralize automatically - require explicit second call
            "neutralization_status": "PENDING_REVIEW"
        }

    def neutralize_with_approval(self, detection_results, approved_by: str):
        if not approved_by:
            raise PermissionError("Human approval required")
        return self.counter_intelligence.neutralize_intelligence_threats(detection_results)