from typing import Union
import balder
from balderhub.waveform.lib.utils.waveforms import CustomNonPeriodicWaveform, CustomPeriodicWaveform

from .waveform_monitor_feature import WaveformMonitorFeature
from .waveform_monitor_instrument import WaveformMonitorInstrument


class WaveformMonitorInstrumentChannel(WaveformMonitorFeature):
    """
    Implementation of :class:`balderhub.waveformmonitor.lib.scenario_features.WaveformMonitorFeature` and uses
    a channel of an :class:`balderhub.waveformmonitor.lib.scenario_features.WaveformMonitorInstrument`
    """

    class Instrument(balder.VDevice):
        """vdevice representing the waveform monitoring instrument (like an oscilloscope)"""
        inst = WaveformMonitorInstrument()

    @property
    def channel(self) -> WaveformMonitorInstrument.Channel:
        """
        :return: returns the channel identifier this feature represents
        """
        raise NotImplementedError

    def start_capturing(self, time_per_div_sec: float, voltage_per_div: float, offset_vdc: float = 0):
        self.Instrument.inst.start_capturing(self.channel, time_per_div_sec, voltage_per_div, offset_vdc)

    def stop_capturing(self):
        self.Instrument.inst.stop_capturing(self.channel)

    def is_capturing(self) -> bool:
        return self.Instrument.inst.is_capturing(self.channel)

    def get_last_captured_waveform(self) -> Union[CustomNonPeriodicWaveform, CustomPeriodicWaveform, None]:
        return self.Instrument.inst.get_last_captured_waveform(self.channel)
