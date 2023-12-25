from datetime import datetime

from app.visits.helpers import timestamp_to_datetime


def test_timestamp_to_datetime_if_timestamp_is_none() -> None:
    # Arrange
    timestamp = None

    # Act
    result = timestamp_to_datetime(timestamp)

    # Assert
    assert result is None


def test_timestamp_to_datetime_if_timestamp_is_valid() -> None:
    # Arrange
    timestamp = 1633022452

    # Act
    result = timestamp_to_datetime(timestamp)

    # Assert
    expected_result = datetime.fromtimestamp(timestamp)
    assert result == expected_result


def test_timestamp_to_datetime_if_timestamp_is_negative() -> None:
    # Arrange
    timestamp = -1

    # Act
    result = timestamp_to_datetime(timestamp)

    # Assert
    expected_result = datetime.fromtimestamp(timestamp)
    assert result == expected_result
