"""
Telemetry recorders are a type of telemetry client that do something with the telemetry data (e.g., write to a CSV or a
database). They use a TelemetrySubscriber to get the telemetry data.
"""

from telemc.recorder import TelemetryRecorder, TelemetryFileRecorder, TelemetryPrinter

__all__ = [
    'TelemetryRecorder',
    'TelemetryFileRecorder',
    'TelemetryPrinter',
    'TelemetryRedisRecorder',
    'TelemetryDashboardRecorder'
]


class TelemetryRedisRecorder(TelemetryRecorder):
    """
    Writes telemetry data from a subscription back into redis and garbage collects old data.
    """

    key_prefix = 'telemc:'

    def __init__(self, rds) -> None:
        super().__init__(rds)

    def _record(self, telemetry):
        rds = self.rds

        if telemetry.subsystem is None:
            key = ':'.join([self.key_prefix, telemetry.node, telemetry.metric, telemetry.subsystem])
        else:
            key = ':'.join([self.key_prefix, telemetry.node, telemetry.metric])

        score = float(telemetry.timestamp)
        val = '%s %s' % (telemetry.timestamp, telemetry.value)

        rds.zadd(key, {val: score})


class TelemetryDashboardRecorder(TelemetryRecorder):
    """
    Writes telemetry data from a subscription back into redis and garbage collects old data.

    currently not used, see #45
    """

    def _record(self, telemetry):
        rds = self.rds

        if telemetry.subsystem is None:
            key = ':'.join(['metrics', telemetry.node, telemetry.metric, telemetry.subsystem])
        else:
            key = ':'.join(['metrics', telemetry.node, telemetry.metric])

        score = float(telemetry.timestamp)
        val = '%s %s' % (telemetry.timestamp, telemetry.value)

        rds.zadd(key, {val: score})
        rds.zremrangebyscore(key, 0, score - 69)  # garbage collect (for some reason 69 keeps 60 seconds ...)
