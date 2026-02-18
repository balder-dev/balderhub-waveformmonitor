from .base_siglent_sds_series_instrument import BaseSiglentSDSSeriesInstrument


class SiglentSDS814xHDInstrument(BaseSiglentSDSSeriesInstrument):
    """
    Feature implementation for the Siglent SDS814X Oscilloscope Instrument
    """

    class Channel(BaseSiglentSDSSeriesInstrument.Channel):
        """available channel for this instrument"""
        CH1 = 1
        CH2 = 2
        CH3 = 3
        CH4 = 4
