import struct
import time
from typing import Union

import math
import numpy as np
from balderhub.scpi.lib.scenario_features import ScpiTransmissionFeature
from balderhub.waveform.lib.utils.waveforms import CustomNonPeriodicWaveform

from ...scenario_features.waveform_monitor_instrument import WaveformMonitorInstrument


class BaseSiglentSDSSeriesInstrument(WaveformMonitorInstrument):
    """
    Feature implementation for the Siglent SDS series Oscilloscope Instrument
    """
    scpi = ScpiTransmissionFeature()

    class Channel(WaveformMonitorInstrument.Channel):
        """available channel for this instrument - needs to be overwritten in parent class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._last_captured_waveforms = {}

    def start_capturing(
            self,
            on_channel: Channel,
            time_per_div_sec: float,
            voltage_per_div: float,
            offset_vdc: float = 0
    ):
        self.scpi.write_values(f':WAVEFORM:SOURCE C{on_channel.value}'.encode(self.scpi.ENCODING))
        time.sleep(1)
        self.scpi.write_values(':WAVEFORM:WIDTH WORD'.encode(self.scpi.ENCODING))
        time.sleep(1)
        self.scpi.write_values(
            f':CHANNEL{on_channel.value}:SCALE {float(voltage_per_div):.9}'.encode(self.scpi.ENCODING)
        )
        time.sleep(1)
        self.scpi.write_values(
            f':CHANNEL{on_channel.value}:OFFSET {float(offset_vdc):.9}'.encode(self.scpi.ENCODING)
        )
        time.sleep(1)
        self.scpi.write_values(f':TIMEBASE:SCALE {float(time_per_div_sec):.9}'.encode(self.scpi.ENCODING))
        time.sleep(1)
        self.scpi.write_values(':WAVEFORM:START 0'.encode(self.scpi.ENCODING))
        time.sleep(1)
        self._last_captured_waveforms[on_channel] = None

    def _read_preamble(self):
        result = self.scpi.query_values(':WAVEFORM:PREAMBLE?'.encode(self.scpi.ENCODING))
        result = result[11:]
        def unpack_pre(offset, fmt):
            return struct.unpack_from(fmt, result, offset)[0]

        point_num = unpack_pre(0x74, '<i')
        vdiv = unpack_pre(0x9C, '<f')  # V/div
        voffset = unpack_pre(0xA0, '<f')  # Offset
        code_per_div = unpack_pre(0xA4, '<f')
        adc_bit = unpack_pre(0xAC, '<h')
        interval = unpack_pre(0xB0, '<f')  # sec per point
        delay = unpack_pre(0xB4, '<d')  # trigger delay
        probe = unpack_pre(0x148, '<f')  # Probe damping
        return point_num, vdiv, voffset, code_per_div, adc_bit, interval, delay, probe

    def stop_capturing(self, on_channel: Channel): # pylint: disable=too-many-locals
        __point_num, vdiv, voffset, code_per_div, adc_bit, interval, __delay, __probe = self._read_preamble()

        # Get the waveform points and confirm the number of waveform slice reads
        points = float(self.scpi.query_values(b":ACQuire:POINts?").strip())
        one_piece_num = float(self.scpi.query_values(b":WAVeform:MAXPoint?").strip())
        read_times = math.ceil(points / one_piece_num)
        # Set the number of read points per slice, if the waveform points is greater than the maximum number of slice
        # reads
        if points > one_piece_num:
            self.scpi.write_values(f":WAVeform:POINt {one_piece_num}".encode(self.scpi.ENCODING))
            time.sleep(1)

        recv_data = b''
        for i in range(read_times):
            self.scpi.write_values(f':WAVEFORM:START {i * one_piece_num}'.encode(self.scpi.ENCODING))
            time.sleep(1)
            result = self.scpi.query_values(':WAVEFORM:DATA?'.encode(self.scpi.ENCODING))

            # Remove header (#<digits><length>)
            block_start = result.find(b'#')
            data_digit = int(result[block_start + 1:block_start + 2])

            assert result[-2:] == b'\n\n'
            data = result[block_start + 2 + data_digit:-2]
            assert len(data) % 2 == 0
            recv_data += data

        # Als signed 16-Bit (WORD) entpacken
        codes = struct.unpack(f'<{int(points)}h', recv_data)  # little-endian

        normalization_value = 1 / ((1 << adc_bit) - 1)
        waveform = CustomNonPeriodicWaveform(
            data=np.array(codes) * normalization_value,
            delta_time_sec=interval,
            multiplier_amplitude_volt=(vdiv / code_per_div) * (1 / normalization_value),
            offset_vdc=voffset
        )
        # Calculate the voltage value and time value
        #time_value = delay + np.arange(point_num) * interval
        #volt_value = np.array(codes) * (vdiv / code_per_div) - voffset

        self._last_captured_waveforms[on_channel] = waveform

    def is_capturing(self, at_channel: Channel) -> bool:
        return at_channel in self._last_captured_waveforms and self._last_captured_waveforms[at_channel] is None

    def get_last_captured_waveform(
            self,
            for_channel: Channel
    ) -> Union[CustomNonPeriodicWaveform, CustomNonPeriodicWaveform, None]:
        return self._last_captured_waveforms.get(for_channel, None)
