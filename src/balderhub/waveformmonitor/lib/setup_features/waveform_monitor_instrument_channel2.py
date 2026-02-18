from ..scenario_features.waveform_monitor_instrument import WaveformMonitorInstrument
from ..scenario_features.waveform_monitor_instrument_channel import WaveformMonitorInstrumentChannel

class WaveformMonitorInstrumentChannel2(WaveformMonitorInstrumentChannel):
    """
    Universal Waveform Monitor Setup Feature representing the Channel 2 of a Waveform Monitor Instrument (like an
    oscilloscope)
    """

    @property
    def channel(self) -> WaveformMonitorInstrument.Channel:
        return WaveformMonitorInstrument.Channel(2)
