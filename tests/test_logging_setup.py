import logging

from src.logging_setup import configure_logging, get_logger


def test_get_logger_returns_logger():
    log = get_logger("test")
    assert isinstance(log, logging.Logger)


def test_configure_logging_sets_level(caplog):
    configure_logging(level="DEBUG")
    log = get_logger("test_debug")
    with caplog.at_level(logging.DEBUG, logger="test_debug"):
        log.debug("hello")
    assert any("hello" in r.message for r in caplog.records)


def test_configure_logging_idempotent():
    configure_logging()
    configure_logging()  # second call should be a no-op, not raise
