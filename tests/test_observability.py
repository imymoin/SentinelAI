from backend.observability import Metrics


def test_metrics_record_request():
    metrics = Metrics()

    metrics.record_request(
        duration=0.5,
        success=True,
    )

    result = metrics.snapshot()

    assert result["requests_total"] == 1
    assert result["requests_failed"] == 0
    assert result["average_request_duration_ms"] == 500.0


def test_metrics_record_failed_request():
    metrics = Metrics()

    metrics.record_request(
        duration=0.2,
        success=False,
    )

    result = metrics.snapshot()

    assert result["requests_total"] == 1
    assert result["requests_failed"] == 1


def test_metrics_record_route():
    metrics = Metrics()

    metrics.record_route("rag")
    metrics.record_route("rag")
    metrics.record_route("direct")

    result = metrics.snapshot()

    assert result["routes"]["rag"] == 2
    assert result["routes"]["direct"] == 1


def test_metrics_record_tool():
    metrics = Metrics()

    metrics.record_tool("db_get_employee")

    result = metrics.snapshot()

    assert result["tools"]["db_get_employee"] == 1