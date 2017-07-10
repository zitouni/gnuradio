#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: MPSK TX RX
# Author: Rafik Zitouni
# Generated: Sun Jul  9 21:00:25 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import math
import sip
import sys
import threading
import time


class MPSK_TX_RX(gr.top_block, Qt.QWidget):

    def __init__(self, address='serial=30AD34D'):
        gr.top_block.__init__(self, "MPSK TX RX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MPSK TX RX")
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

        self.settings = Qt.QSettings("GNU Radio", "MPSK_TX_RX")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.address = address

        ##################################################
        # Variables
        ##################################################
        self.const_type = const_type = 2
        self.bits_per_symbol = bits_per_symbol = int(const_type+1)
        self.samples_per_symbol = samples_per_symbol = int(2*(bits_per_symbol))
        self.probe_SNR = probe_SNR = 0
        self.nfilts = nfilts = 32
        self.bitrate = bitrate = 64e3
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = {0: 'BPSK', 1: 'QPSK', 2: '8-PSK'}[const_type] + " - Change const_type for different constellation types!"
        self.tun_gain_tx = tun_gain_tx = 40
        self.tun_freq_tx = tun_freq_tx = 2.39e9
        self.timing_bw = timing_bw = 2*math.pi/100.0
        self.samp_rate = samp_rate = samples_per_symbol*bitrate
        self.phase_bw = phase_bw = 2*math.pi/100.0
        self.ntaps = ntaps = 11 * int(samples_per_symbol*nfilts)
        self.lo_offset = lo_offset = 6e6
        self.gain_rx = gain_rx = 0.75
        self.freq_rx = freq_rx = 2390e6
        self.freq_bw = freq_bw = 2*math.pi/100.0
        self.fll_ntaps = fll_ntaps = 55
        self.excess_bw = excess_bw = 0.35
        self.constellation = constellation = (digital.constellation_bpsk(), digital.constellation_qpsk(), digital.constellation_8psk())
        self.arrity = arrity = pow(2, bits_per_symbol)
        self.ampl = ampl = 0.7
        self.SNR = SNR = probe_SNR

        ##################################################
        # Blocks
        ##################################################
        self._tun_gain_tx_range = Range(0, 80, 1, 40, 200)
        self._tun_gain_tx_win = RangeWidget(self._tun_gain_tx_range, self.set_tun_gain_tx, 'UHD Tx Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tun_gain_tx_win, 1,0,1,1)
        self._tun_freq_tx_range = Range(2.3e9, 2.5e9, 1, 2.39e9, 200)
        self._tun_freq_tx_win = RangeWidget(self._tun_freq_tx_range, self.set_tun_freq_tx, 'UHD Tx Freq (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tun_freq_tx_win, 0,0,1,1)
        self._lo_offset_options = (0, 6e6, 11e6, )
        self._lo_offset_labels = (str(self._lo_offset_options[0]), str(self._lo_offset_options[1]), str(self._lo_offset_options[2]), )
        self._lo_offset_tool_bar = Qt.QToolBar(self)
        self._lo_offset_tool_bar.addWidget(Qt.QLabel("lo_offset"+": "))
        self._lo_offset_combo_box = Qt.QComboBox()
        self._lo_offset_tool_bar.addWidget(self._lo_offset_combo_box)
        for label in self._lo_offset_labels: self._lo_offset_combo_box.addItem(label)
        self._lo_offset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._lo_offset_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._lo_offset_options.index(i)))
        self._lo_offset_callback(self.lo_offset)
        self._lo_offset_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_lo_offset(self._lo_offset_options[i]))
        self.top_grid_layout.addWidget(self._lo_offset_tool_bar, 2,1,1,1)
        self._gain_rx_range = Range(0, 1, 0.01, 0.75, 200)
        self._gain_rx_win = RangeWidget(self._gain_rx_range, self.set_gain_rx, 'UHD Rx Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_rx_win, 1,1,1,1)
        self._freq_rx_range = Range(2350e6, 2500e6, 10e6, 2390e6, 200)
        self._freq_rx_win = RangeWidget(self._freq_rx_range, self.set_freq_rx, 'UHD Rx Freq (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_rx_win, 0,1,1,1)
        self.digital_probe_mpsk_snr_est_c_0 = digital.probe_mpsk_snr_est_c(2, 1000, 10/bitrate)
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
          self._variable_qtgui_label_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Constellation Type'+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)
          
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join((address, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_subdev_spec('A:A', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(freq_rx, rf_freq = freq_rx - lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)
        self.uhd_usrp_source_0.set_normalized_gain(gain_rx, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
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
        self.qtgui_number_sink_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1.set_title("BER")
        
        labels = ['BER', '', '', '', '',
                  '', '', '', '', '']
        units = ['x10^-6', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1e6, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_1.set_min(i, 0)
            self.qtgui_number_sink_0_1.set_max(i, 1)
            self.qtgui_number_sink_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1.set_factor(i, factor[i])
        
        self.qtgui_number_sink_0_1.enable_autoscale(True)
        self._qtgui_number_sink_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_1_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_const_sink_x_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 3,0,1,1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_const_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 3,1,1,1)
        
        def _probe_SNR_probe():
            while True:
                val = self.digital_probe_mpsk_snr_est_c_0.snr()
                try:
                    self.set_probe_SNR(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _probe_SNR_thread = threading.Thread(target=_probe_SNR_probe)
        _probe_SNR_thread.daemon = True
        _probe_SNR_thread.start()
            
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  samples_per_symbol,
                  taps=(firdes.root_raised_cosine(nfilts, nfilts, 1.0,  0.35, ntaps)),
        	  flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x8A, 0x7F, 7)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samples_per_symbol, timing_bw, (firdes.root_raised_cosine(nfilts, nfilts*samples_per_symbol, 1.0,  0.35, ntaps)), nfilts,  nfilts//2, 1.5, 1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samples_per_symbol, excess_bw, fll_ntaps, freq_bw)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(arrity)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(arrity)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x8A, 0x7F, 7)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(timing_bw, pow(2, bits_per_symbol), False)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(constellation[const_type].base())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((constellation[const_type].points()), 1)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b([1,] , True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b([1,] , True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_symbol)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(bits_per_symbol)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((ampl, ))
        self.blks2_error_rate_0 = grc_blks2.error_rate(
        	type='BER',
        	win_size=10000,
        	bits_per_symbol=1,
        )
        self.analog_agc2_xx_0 = analog.agc2_cc(0.6e-1, 1e-3, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)
        self._SNR_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._SNR_formatter = None
        else:
          self._SNR_formatter = lambda x: x
        
        self._SNR_tool_bar.addWidget(Qt.QLabel("SNR"+": "))
        self._SNR_label = Qt.QLabel(str(self._SNR_formatter(self.SNR)))
        self._SNR_tool_bar.addWidget(self._SNR_label)
        self.top_layout.addWidget(self._SNR_tool_bar)
          

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))    
        self.connect((self.blks2_error_rate_0, 0), (self.qtgui_number_sink_0_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_diff_encoder_bb_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_descrambler_bb_0, 0))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_scrambler_bb_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blks2_error_rate_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))    
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_diff_decoder_bb_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_probe_mpsk_snr_est_c_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))    
        self.connect((self.digital_descrambler_bb_0, 0), (self.blks2_error_rate_0, 1))    
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))    
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc2_xx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MPSK_TX_RX")
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
        self.digital_pfb_clock_sync_xxx_0.update_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samples_per_symbol, 1.0,  0.35, self.ntaps)))

    def get_probe_SNR(self):
        return self.probe_SNR

    def set_probe_SNR(self, probe_SNR):
        self.probe_SNR = probe_SNR
        self.set_SNR(self._SNR_formatter(self.probe_SNR))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_ntaps(11 * int(self.samples_per_symbol*self.nfilts))
        self.pfb_arb_resampler_xxx_0.set_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0,  0.35, self.ntaps)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samples_per_symbol, 1.0,  0.35, self.ntaps)))

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate
        self.set_samp_rate(self.samples_per_symbol*self.bitrate)
        self.digital_probe_mpsk_snr_est_c_0.set_alpha(10/self.bitrate)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0)))

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

    def get_timing_bw(self):
        return self.timing_bw

    def set_timing_bw(self, timing_bw):
        self.timing_bw = timing_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_bw)
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.timing_bw)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.pfb_arb_resampler_xxx_0.set_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0,  0.35, self.ntaps)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samples_per_symbol, 1.0,  0.35, self.ntaps)))

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self._lo_offset_callback(self.lo_offset)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_rx, rf_freq = self.freq_rx - self.lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_source_0.set_normalized_gain(self.gain_rx, 0)
        	

    def get_freq_rx(self):
        return self.freq_rx

    def set_freq_rx(self, freq_rx):
        self.freq_rx = freq_rx
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_rx, rf_freq = self.freq_rx - self.lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def get_freq_bw(self):
        return self.freq_bw

    def set_freq_bw(self, freq_bw):
        self.freq_bw = freq_bw
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth(self.freq_bw)

    def get_fll_ntaps(self):
        return self.fll_ntaps

    def set_fll_ntaps(self, fll_ntaps):
        self.fll_ntaps = fll_ntaps

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

    def get_SNR(self):
        return self.SNR

    def set_SNR(self, SNR):
        self.SNR = SNR
        Qt.QMetaObject.invokeMethod(self._SNR_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.SNR)))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-a", "--address", dest="address", type="string", default='serial=30AD34D',
        help="Set IP Address [default=%default]")
    return parser


def main(top_block_cls=MPSK_TX_RX, options=None):
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
