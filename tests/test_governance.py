import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from src.governance import audit_logger, data_lineage
from src.security import rbac


class TestRBAC:
    def test_admin_has_all(self):
        assert rbac.has_permission("admin", "delete")

    def test_viewer_cannot_write(self):
        assert not rbac.has_permission("viewer", "write")

    def test_require_permission_raises(self):
        with pytest.raises(rbac.AccessDenied):
            rbac.require_permission("viewer", "delete")


class TestAuditLogger:
    @patch("src.governance.audit_logger.psycopg2")
    def test_log_action_runs(self, mock_pg):
        audit_logger.log_action("analyst", "run_query", "traffic_logs")
        assert mock_pg.connect.called


class TestDataLineage:
    def test_pipeline_flow(self):
        assert data_lineage.PIPELINE_FLOW[0] == "YouTube"
        assert "Kafka" in data_lineage.PIPELINE_FLOW
