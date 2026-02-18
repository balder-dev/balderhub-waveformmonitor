from typing import Union
import enum
import balder
from balderhub.waveform.lib.utils.waveforms import CustomNonPeriodicWaveform, CustomPeriodicWaveform


class WaveformMonitorInstrument(balder.Feature):
    """raw implementation of a programmable oscilloscope instrument"""

    class Channel(enum.Enum):
        """enum holding all available channels of this instrument"""

    def start_capturing(
            self,
            on_channel: Channel,
            time_per_div_sec: float,
            voltage_per_div: float,
            offset_vdc: float = 0
    ):
        """
        This method starts the capturing on the given channel.

        :param on_channel: channel to start capturing at
        :param time_per_div_sec: time per div in seconds
        :param voltage_per_div: voltage per div
        :param offset_vdc: offset that should be applied to capture the waveform
        """
        raise NotImplementedError

    def stop_capturing(self, on_channel: Channel):
        """
        This method stops the capturing on the specific channel.

        :param on_channel: channel to stop capturing at
        """
        raise NotImplementedError

    def is_capturing(self, at_channel: Channel) -> bool:
        """
        :param at_channel: channel to check
        :return: returns true if the capturing at the specific channel is enabled, otherwise False
        """
        raise NotImplementedError

    def get_last_captured_waveform(
            self,
            for_channel: Channel
    ) -> Union[CustomNonPeriodicWaveform, CustomPeriodicWaveform, None]:
        """
        This method gets the last captured waveform of the specific channel and returns it as PERIODIC or
        NON-PERIODIC waveform (dependent of device type and how the instrument captures the waveform).

        :param for_channel: channel to get the last captured waveform for
        :return: the captured waveform object
        """
        raise NotImplementedError
