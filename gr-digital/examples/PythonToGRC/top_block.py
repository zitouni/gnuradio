#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Jul 10 10:07:23 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self, address='serial=30AD34D'):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.address = address

        ##################################################
        # Variables
        ##################################################
        self.const_type = const_type = 1
        self.bits_per_symbol = bits_per_symbol = int(const_type+1)
        self.samples_per_symbol = samples_per_symbol = int(2*(bits_per_symbol))
        self.nfilts = nfilts = 32
        self.bitrate = bitrate = 64e3
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = {0: 'BPSK', 1: 'QPSK', 2: '8-PSK'}[const_type] + " - Change const_type for different constellation types!"
        self.tun_gain_tx = tun_gain_tx = 40
        self.tun_freq_tx = tun_freq_tx = 2.39e9
        self.samp_rate = samp_rate = samples_per_symbol*bitrate
        self.ntaps = ntaps = 11 * int(samples_per_symbol*nfilts)
        self.excess_bw = excess_bw = 0.35
        self.constellation = constellation = (digital.constellation_bpsk(), digital.constellation_qpsk(), digital.constellation_8psk())
        self.arrity = arrity = pow(2, bits_per_symbol)
        self.ampl = ampl = 0.7

        ##################################################
        # Blocks
        ##################################################
        self._tun_gain_tx_range = Range(0, 80, 1, 40, 200)
        self._tun_gain_tx_win = RangeWidget(self._tun_gain_tx_range, self.set_tun_gain_tx, 'UHD Tx Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tun_gain_tx_win, 1,0,1,1)
        self._tun_freq_tx_range = Range(2.3e9, 2.5e9, 1, 2.39e9, 200)
        self._tun_freq_tx_win = RangeWidget(self._tun_freq_tx_range, self.set_tun_freq_tx, 'UHD Tx Freq (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tun_freq_tx_win, 0,0,1,1)
        self._const_type_options = (0, 1, 2, )
        self._const_type_labels = ('DBPSK', 'DQPSK', 'D8PSK', )
        self._const_type_tool_bar = Qt.QToolBar(self)
        self._const_type_tool_bar.addWidget(Qt.QLabel("const_type"+": "))
        self._const_type_combo_box = Qt.QComboBox()
        self._const_type_tool_bar.addWidget(self._const_type_combo_box)
        for label in self._const_type_labels: self._const_type_combo_box.addItem(label)
        self._const_type_callback = lambda i: Qt.QMetaObject.invokeMethod(self._const_type_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._const_type_options.index(i)))
        self._const_type_callback(self.const_type)
        self._const_type_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_const_type(self._const_type_options[i]))
        self.top_layout.addWidget(self._const_type_tool_bar)
        self._ampl_range = Range(0, 1, 0.01, 0.7, 200)
        self._ampl_win = RangeWidget(self._ampl_range, self.set_ampl, 'Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._ampl_win, 2,0,1,1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Constellation Type'+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)

        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join((address, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0_0.set_subdev_spec('A:B', 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(tun_freq_tx, 0)
        self.uhd_usrp_sink_0_0.set_gain(tun_gain_tx, 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  samples_per_symbol,
                  taps=(firdes.root_raised_cosine(nfilts, nfilts, 1.0,  0.35, ntaps)),
        	  flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x8A, 0x7F, 7)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(arrity)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((constellation[const_type].points()), 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_b([1,] , True, 1, [])
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(bits_per_symbol)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((ampl, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_const_type(self):
        return self.const_type

    def set_const_type(self, const_type):
        self.const_type = const_type
        self._const_type_callback(self.const_type)
        self.set_bits_per_symbol(int(self.const_type+1))
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter({0: 'BPSK', 1: 'QPSK', 2: '8-PSK'}[self.const_type] + " - Change const_type for different constellation types!"))
        self.digital_chunks_to_symbols_xx_0.set_symbol_table((self.constellation[self.const_type].points()))

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_samples_per_symbol(int(2*(self.bits_per_symbol)))
        self.set_arrity(pow(2, self.bits_per_symbol))

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_samp_rate(self.samples_per_symbol*self.bitrate)
        self.set_ntaps(11 * int(self.samples_per_symbol*self.nfilts))
        self.pfb_arb_resampler_xxx_0.set_rate(self.samples_per_symbol)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_ntaps(11 * int(self.samples_per_symbol*self.nfilts))
        self.pfb_arb_resampler_xxx_0.set_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0,  0.35, self.ntaps)))

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate
        self.set_samp_rate(self.samples_per_symbol*self.bitrate)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_tun_gain_tx(self):
        return self.tun_gain_tx

    def set_tun_gain_tx(self, tun_gain_tx):
        self.tun_gain_tx = tun_gain_tx
        self.uhd_usrp_sink_0_0.set_gain(self.tun_gain_tx, 0)


    def get_tun_freq_tx(self):
        return self.tun_freq_tx

    def set_tun_freq_tx(self, tun_freq_tx):
        self.tun_freq_tx = tun_freq_tx
        self.uhd_usrp_sink_0_0.set_center_freq(self.tun_freq_tx, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.pfb_arb_resampler_xxx_0.set_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0,  0.35, self.ntaps)))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self.digital_chunks_to_symbols_xx_0.set_symbol_table((self.constellation[self.const_type].points()))

    def get_arrity(self):
        return self.arrity

    def set_arrity(self, arrity):
        self.arrity = arrity

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.blocks_multiply_const_vxx_0.set_k((self.ampl, ))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-a", "--address", dest="address", type="string", default='serial=30AD34D',
        help="Set IP Address [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(address=options.address)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
