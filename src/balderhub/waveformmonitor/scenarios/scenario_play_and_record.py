import time
import balder
from balderhub.waveform.lib.utils.waveforms import BasePeriodicWaveform
from balderhub.waveformgenerator.lib.scenario_features import WaveformGeneratorFeature

from balderhub.waveformmonitor.lib.scenario_features import WaveformMonitorFeature, TestConfig


class ScenarioPlayAndRecord(balder.Scenario):
    """Simple test scenario to play a signal with a waveform generator and read it back with a waveform monitor"""

    class Generator(balder.Device):
        """waveform generator"""
        waveform = WaveformGeneratorFeature()

    class DUT(balder.Device):
        """device under test"""
        testconfig = TestConfig()
        waveform = WaveformMonitorFeature()

    @balder.parametrize_by_feature('waveform', (DUT, 'testconfig', 'waveforms_to_test'))
    def test_play_and_record(self, waveform: BasePeriodicWaveform):
        """simple test that tries to play a waveform with the generator and reads it back with the monitor"""

        self.Generator.waveform.set_waveform(waveform)

        try:
            self.Generator.waveform.enable_signal()
            try:
                self.DUT.waveform.start_capturing(1 / waveform.frequency_hz, waveform.amplitude_vpp / 4)
                time.sleep(10)
            finally:
                self.DUT.waveform.stop_capturing()
        finally:
            self.Generator.waveform.disable_signal()

        captured_waveform = self.DUT.waveform.get_last_captured_waveform()

        captured_periodic_waveform = captured_waveform.get_periodic_equivalent_waveform()

        assert waveform.compare(captured_periodic_waveform, ignore_phase=True)
