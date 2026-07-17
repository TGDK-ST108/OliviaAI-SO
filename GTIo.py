from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GlobalThreatIntelligence:
    def __init__(self, olivia_ai):
        """
        Initialize the threat intelligence module.

        Args:
            olivia_ai: Your OliviaAI client instance that implements
                       aggregate(), execute(), and retrieve()
        """
        if not olivia_ai:
            raise ValueError("olivia_ai client is required")
        self.olivia_ai = olivia_ai

    def aggregate_threat_data(self, external_sources: List[str]) -> Dict[str, Any]:
        """Collect and normalize threat intelligence from global sources."""
        if not external_sources:
            return {}

        try:
            aggregated_data = self.olivia_ai.aggregate(
                "threat_intelligence",
                external_sources
            )
            logger.info(f"Aggregated threat data from {len(external_sources)} sources")
            return aggregated_data or {}
        except Exception as e:
            logger.error(f"Failed to aggregate threat data: {e}")
            return {"error": str(e), "sources_attempted": external_sources}

    def share_threat_updates(self, local_data: Dict[str, Any],
                             trust_level: str = "trusted") -> Dict[str, Any]:
        """Share sanitized threat insights with trusted networks."""
        if not local_data:
            raise ValueError("local_data cannot be empty")

        # Always sanitize before sharing - strip PII / internal IPs
        sanitized_data = self._sanitize(local_data)

        try:
            shared_status = self.olivia_ai.execute(
                "share_threat_updates",
                {"data": sanitized_data, "trust_level": trust_level}
            )
            return shared_status
        except Exception as e:
            logger.error(f"Failed to share threat updates: {e}")
            return {"status": "failed", "error": str(e)}

    def receive_updates(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Retrieve the latest global threat intelligence."""
        try:
            updates = self.olivia_ai.retrieve(
                "global_threat_updates",
                filters or {}
            )
            return updates or {}
        except Exception as e:
            logger.error(f"Failed to retrieve global updates: {e}")
            return {"error": str(e)}

    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive fields before sharing externally."""
        # Add your real sanitization logic here
        sensitive_keys = {"internal_ip", "user_email", "pii", "raw_logs"}
        return {k: v for k, v in data.items() if k not in sensitive_keys}