from ..scenario_features.waveform_monitor_instrument import WaveformMonitorInstrument
from ..scenario_features.waveform_monitor_instrument_channel import WaveformMonitorInstrumentChannel


class WaveformMonitorInstrumentChannel1(WaveformMonitorInstrumentChannel):
    """
    Universal Waveform Monitor Setup Feature representing the Channel 1 of a Waveform Monitor Instrument (like an
    oscilloscope)
    """

    @property
    def channel(self) -> WaveformMonitorInstrument.Channel:
        return WaveformMonitorInstrument.Channel(1)
