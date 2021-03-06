#!/usr/bin/env python
#
# Copyright 2008,2011,2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from PyQt4 import Qt
import sip

from gnuradio import gr, eng_notation, qtgui
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import sys

from gnuradio import blocks
from gnuradio import digital

# from current dir
from uhd_interface import uhd_transmitter

n2s = eng_notation.num_to_str

class bert_transmit(gr.hier_block2):
    def __init__(self, constellation, samples_per_symbol,
                 differential, excess_bw, gray_coded,
                 verbose, log):

        gr.hier_block2.__init__(self, "bert_transmit",
                                gr.io_signature(0, 0, 0),                    # Output signature
                                gr.io_signature(1, 1, gr.sizeof_gr_complex)) # Input signature
        
        # Create BERT data bit stream	
	self._bits = blocks.vector_source_b([1,], True)      # Infinite stream of ones
        self._scrambler = digital.scrambler_bb(0x8A, 0x7F, 7) # CCSDS 7-bit scrambler

        self._mod = digital.generic_mod(constellation, differential,
                                        samples_per_symbol,
                                        gray_coded, excess_bw,
                                        verbose, log)

        self._pack = blocks.unpacked_to_packed_bb(self._mod.bits_per_symbol(), gr.GR_MSB_FIRST)

        self.connect(self._bits, self._scrambler, self._pack, self._mod, self)


class tx_psk_block(gr.top_block, Qt.QWidget):
    def __init__(self, mod, options):
	gr.top_block.__init__(self, "tx_mpsk")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MPSK Tx")
        
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
        
        self._modulator_class = mod

        # Get mod_kwargs
        mod_kwargs = self._modulator_class.extract_kwargs_from_options(options)
        
        # transmitter
	self._modulator = self._modulator_class(**mod_kwargs)

        if(options.tx_freq is not None):
            symbol_rate = options.bitrate / self._modulator.bits_per_symbol()
            self._sink = uhd_transmitter(options.args, symbol_rate,
                                         options.samples_per_symbol,
                                         options.tx_freq, options.tx_gain,
                                         options.spec,
                                         options.antenna, options.verbose)
            options.samples_per_symbol = self._sink._sps
            
        elif(options.to_file is not None):
            self._sink = blocks.file_sink(gr.sizeof_gr_complex, options.to_file)
        else:
            self._sink = blocks.null_sink(gr.sizeof_gr_complex)
    
        #Create GUI to see symbols constellation 
        self.qtgui_const_sink = qtgui.const_sink_c(
            400, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink.set_update_time(0.1)
        self.qtgui_const_sink.set_y_axis(-2, 2)
        self.qtgui_const_sink.set_x_axis(-2, 2)
        self.qtgui_const_sink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink.enable_autoscale(False)
        self.qtgui_const_sink.enable_grid(False)
        self.qtgui_const_sink.enable_axis_labels(True)
            
        if not True:
            self.qtgui_const_sink.disable_legend()
            
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
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
                self.qtgui_const_sink.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink.set_line_label(i, labels[i])
            self.qtgui_const_sink.set_line_width(i, widths[i])
            self.qtgui_const_sink.set_line_color(i, colors[i])
            self.qtgui_const_sink.set_line_style(i, styles[i])
            self.qtgui_const_sink.set_line_marker(i, markers[i]) 
            self.qtgui_const_sink.set_line_alpha(i, alphas[i])
         
        self._qtgui_const_sink_win = sip.wrapinstance(self.qtgui_const_sink.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_win)  
        
                    
        self._transmitter = bert_transmit(self._modulator._constellation,
                                          options.samples_per_symbol,
                                          options.differential,
                                          options.excess_bw,
                                          gray_coded=True,
                                          verbose=options.verbose,
                                          log=options.log)

        self.amp = blocks.multiply_const_cc(options.amplitude)  
               
        self.connect(self._transmitter, self.amp, self._sink)
        
        self.connect(self.amp, self.qtgui_const_sink)
    
#     self.connect(self.amp, self.qtgui_const_sink)


def get_options(mods):
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='psk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))
    parser.add_option("", "--amplitude", type="eng_float", default=0.2,
                      help="set Tx amplitude (0-1) (default=%default)")
    parser.add_option("-r", "--bitrate", type="eng_float", default=250e3,
                      help="Select modulation bit rate (default=%default)")
    parser.add_option("-S", "--samples-per-symbol", type="float", default=2,
                      help="set samples/symbol [default=%default]")
    parser.add_option("","--to-file", default=None,
                      help="Output file for modulated samples")
    if not parser.has_option("--verbose"):
        parser.add_option("-v", "--verbose", action="store_true", default=False)
    if not parser.has_option("--log"):
        parser.add_option("", "--log", action="store_true", default=False)

    uhd_transmitter.add_options(parser)

    for mod in mods.values():
        mod.add_options(parser)
		      
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        sys.exit(1)
	
    return (options, args)

if __name__ == "__main__":
    mods = digital.modulation_utils.type_1_mods()

    (options, args) = get_options(mods)
    
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)
    
    mod = mods[options.modulation]
    tb = tx_psk_block(mod, options)

#     try:
#         tb.run()
#     except KeyboardInterrupt:
#         pass

    tb.start()
    tb.show()
    
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
