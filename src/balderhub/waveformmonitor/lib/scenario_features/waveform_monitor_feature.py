from typing import Union
import balder

from balderhub.waveform.lib.utils.waveforms import CustomNonPeriodicWaveform, CustomPeriodicWaveform


class WaveformMonitorFeature(balder.Feature):
    """
    Waveform Monitor Feature that can be used for any device types. It does not even need to be a Programmable
    Oscilloscope, because you could use any device that can be controlled and provide the functionality below.
    """
    def start_capturing(self, time_per_div_sec: float, voltage_per_div: float, offset_vdc: float = 0):
        """
        This method starts the capturing.

        :param time_per_div_sec: time per div in seconds
        :param voltage_per_div: voltage per div
        :param offset_vdc: offset that should be applied to capture the waveform
        """
        raise NotImplementedError

    def stop_capturing(self):
        """
        This method stops the capturing.
        """
        raise NotImplementedError

    def is_capturing(self) -> bool:
        """
        :return: returns true if the capturing is enabled, otherwise False
        """
        raise NotImplementedError

    def get_last_captured_waveform(self) -> Union[CustomNonPeriodicWaveform, CustomPeriodicWaveform, None]:
        """
        This method gets the last captured waveform and returns it as PERIODIC or NON-PERIODIC waveform (dependent of
        device type and how the instrument captures the waveform).

        :return: the captured waveform object
        """
        raise NotImplementedError
