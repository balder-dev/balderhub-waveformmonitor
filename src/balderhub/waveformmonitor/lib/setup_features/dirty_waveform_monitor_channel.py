from typing import Union
from balderhub.waveform.lib.utils.waveforms import CustomNonPeriodicWaveform, CustomPeriodicWaveform

from ..scenario_features.waveform_monitor_feature import WaveformMonitorFeature
from ..scenario_features.waveform_monitor_instrument import WaveformMonitorInstrument


class DirtyWaveformMonitorChannel(WaveformMonitorFeature):
    """
    Dirty helper feature that can be assigned directly to the device
    """
    inst = WaveformMonitorInstrument()

    @property
    def channel(self) -> WaveformMonitorInstrument.Channel:
        """
        :return: returns the channel that should be used for the feature (defaults to 1)
        """
        return self.inst.__class__.Channel(1)

    def start_capturing(self, time_per_div_sec: float, voltage_per_div: float, offset_vdc: float = 0):
        return self.inst.start_capturing(self.channel, time_per_div_sec, voltage_per_div, offset_vdc)

    def stop_capturing(self):
        return self.inst.stop_capturing(self.channel)

    def is_capturing(self) -> bool:
        return self.inst.is_capturing(self.channel)

    def get_last_captured_waveform(self) -> Union[CustomNonPeriodicWaveform, CustomPeriodicWaveform, None]:
        return self.inst.get_last_captured_waveform(self.channel)
