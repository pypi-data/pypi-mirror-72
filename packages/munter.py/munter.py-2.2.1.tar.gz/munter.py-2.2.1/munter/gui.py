# -*- coding: utf-8 -*-


"""
GUI implementation
"""

import wx
from . import munter
from . import __progname__ as progname
from . import __version__ as version

class MainFrame(wx.Frame):
    """
    The main wx.Frame
    """
    program_name = ""

    def __init__(self, *args, **kw):
        """add to the init process for the wx.Frame"""
        super(MainFrame, self).__init__(*args, **kw)

        # initial setup
        self.SetTitle(progname)
        self.SetSize(600, 400)

        self.props = self.init_props()
        self.pnl = wx.Panel(self)

        # wx item vars
        self.wx_items = dict()
        self.wx_items['StaticText'] = dict()
        self.wx_items['TextEntry'] = dict()
        self.wx_items['RadioButton'] = dict()
        self.wx_items['ComboBox'] = dict()

        # setup the GUI itself
        self.create_wx_items()
        self.establish_wx_bindings()
        self.do_wx_layout()
        self.update_mtc()

    # init routines
    def init_props(self):
        """centralized place to initialize props var"""
        props = dict()
        props['distance'] = 0
        props['elevation'] = 0
        props['fitness'] = 'average'
        props['units'] = 'imperial'
        props['travel_mode'] = 'uphill'
        return props

    def create_wx_items(self):
        """create wxPython items"""
        # title bar / program name
        self.program_name = wx.StaticText(self.pnl, label=progname)
        font = self.program_name.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.program_name.SetFont(font)

        # text entry fields
        self.wx_items['StaticText']['distance'] = wx.StaticText(self.pnl,
                                                                label="Distance: ",
                                                                style=wx.ALIGN_RIGHT)
        self.wx_items['TextEntry']['distance'] = wx.TextCtrl(self.pnl,
                                                             value="0",
                                                             size=(140, -1))

        self.wx_items['StaticText']['elevation'] = wx.StaticText(self.pnl,
                                                                 label="Elevation: ",
                                                                 style=wx.ALIGN_RIGHT)
        self.wx_items['TextEntry']['elevation'] = wx.TextCtrl(self.pnl,
                                                              value="0",
                                                              size=(140, -1))

        self.wx_items['StaticText']['fitness'] = wx.StaticText(self.pnl,
                                                               label="Fitness: ",
                                                               style=wx.ALIGN_RIGHT)
        rb_fitness_choices = ['slow', 'average', 'fast']
        rb_fitness_default = 'average'
        self.wx_items['RadioButton']['fitness'] = wx.ComboBox(self.pnl,
                                                              choices=rb_fitness_choices,
                                                              value=rb_fitness_default,
                                                              style=wx.CB_READONLY)

        self.wx_items['StaticText']['travel_mode'] = wx.StaticText(self.pnl,
                                                                   label="Travel Mode: ",
                                                                   style=wx.ALIGN_RIGHT)
        rb_travel_mode_choices = ['uphill', 'flat', 'downhill', 'bushwhacking']
        rb_travel_mode_default = 'uphill'
        self.wx_items['RadioButton']['travel_mode'] = wx.ComboBox(self.pnl,
                                                                  choices=rb_travel_mode_choices,
                                                                  value=rb_travel_mode_default,
                                                                  style=wx.CB_READONLY)

        self.wx_items['StaticText']['units'] = wx.StaticText(self.pnl,
                                                             label="Units: ",
                                                             style=wx.ALIGN_RIGHT)
        rb_units_choices = ['imperial', 'metric']
        rb_units_default = 'imperial'

        self.wx_items['RadioButton']['units'] = []
        for choice in rb_units_choices:
            label = choice
            style = wx.RB_GROUP if choice == rb_units_default else 0
            self.wx_items['RadioButton']['units'].append(wx.RadioButton(self.pnl,
                                                                        label=label,
                                                                        style=style))

        # static text
        self.wx_items['StaticText']['mtc'] = wx.StaticText(self.pnl,
                                                           label="",
                                                           style=wx.ALIGN_CENTRE_HORIZONTAL)

        st_mtc_font = self.program_name.GetFont()
        st_mtc_font.PointSize += 10
        self.wx_items['StaticText']['mtc'].SetFont(st_mtc_font)

        # buttons
        self.b_reset = wx.Button(self.pnl, wx.NewId(), '&Reset', (-1, -1),
                                 wx.DefaultSize)

    def establish_wx_bindings(self):
        """establish wxPython bindings"""
        self.pnl.Bind(wx.EVT_TEXT, self.update_distance, self.wx_items['TextEntry']['distance'])
        self.pnl.Bind(wx.EVT_TEXT, self.update_elevation, self.wx_items['TextEntry']['elevation'])
        self.wx_items['RadioButton']['fitness'].Bind(wx.EVT_COMBOBOX, self.update_fitness)
        self.wx_items['RadioButton']['travel_mode'].Bind(wx.EVT_COMBOBOX, self.update_travel_mode)
        self.b_reset.Bind(wx.EVT_BUTTON, self.reset)

        for rb_unit in self.wx_items['RadioButton']['units']:
            rb_unit.Bind(wx.EVT_RADIOBUTTON, self.update_units)

    def do_wx_layout(self):
        """layout the wxPython items"""
        border = 5
        width = 100

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.program_name, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 0))

        static_line = wx.StaticLine(self.pnl, wx.NewId(), style=wx.LI_HORIZONTAL)

        hsizer_distance = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_distance.Add(self.wx_items['StaticText']['distance'], 0, wx.RIGHT, border)
        hsizer_distance.Add(self.wx_items['TextEntry']['distance'], 1, wx.GROW, border)
        hsizer_distance.SetItemMinSize(self.wx_items['StaticText']['distance'], (width, -1))

        hsizer_elevation = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_elevation.Add(self.wx_items['StaticText']['elevation'], 0, wx.RIGHT, border)
        hsizer_elevation.Add(self.wx_items['TextEntry']['elevation'], 1, wx.GROW, border)
        hsizer_elevation.SetItemMinSize(self.wx_items['StaticText']['elevation'], (width, -1))

        hsizer_fitness = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_fitness.Add(self.wx_items['StaticText']['fitness'], 0, wx.RIGHT, border)
        hsizer_fitness.Add(self.wx_items['RadioButton']['fitness'], 1, wx.GROW, border)
        hsizer_fitness.SetItemMinSize(self.wx_items['StaticText']['fitness'], (width, -1))

        hsizer_travel_mode = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_travel_mode.Add(self.wx_items['StaticText']['travel_mode'], 0, wx.RIGHT, border)
        hsizer_travel_mode.Add(self.wx_items['RadioButton']['travel_mode'], 1, wx.GROW, border)
        hsizer_travel_mode.SetItemMinSize(self.wx_items['StaticText']['travel_mode'], (width, -1))

        hsizer_units = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_units.Add(self.wx_items['StaticText']['units'], 0, wx.RIGHT, border)
        for rb_unit in range(len(self.wx_items['RadioButton']['units'])):
            hsizer_units.Add(self.wx_items['RadioButton']['units'][rb_unit],
                             rb_unit + 1,
                             wx.GROW,
                             border)
        hsizer_units.SetItemMinSize(self.wx_items['StaticText']['units'], (width, -1))

        hsizer_mtc = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_mtc.Add(self.wx_items['StaticText']['mtc'], 1, wx.GROW, border)
        hsizer_mtc.SetItemMinSize(self.wx_items['StaticText']['mtc'], (width, -1))

        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5.Add(self.b_reset, 0)

        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(sizer, 0, wx.EXPAND | wx.ALL, border*border)
        vsizer1.Add(hsizer_distance, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(hsizer_elevation, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(hsizer_fitness, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(hsizer_travel_mode, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(hsizer_units, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(hsizer_mtc, 0, wx.EXPAND | wx.ALL, border)
        vsizer1.Add(static_line, 0, wx.GROW | wx.ALL, border)
        vsizer1.Add(hsizer5, 0, wx.ALIGN_RIGHT | wx.ALL, border)

        self.pnl.SetSizerAndFit(vsizer1)
        self.pnl.SetClientSize(vsizer1.GetSize())

    # event handlers
    def update_distance(self, event):
        """updates distance prop"""
        value = event.GetEventObject().GetValue()
        if value:
            try:
                new_val = float(value)
                self.props['distance'] = new_val
            except ValueError:
                # reset GUI to last-accepted val
                self.wx_items['TextEntry']['distance'].SetValue(str(self.props['distance']))
        self.update_mtc()

    def update_elevation(self, event):
        """updates elevation prop"""
        value = event.GetEventObject().GetValue()
        if value:
            try:
                new_val = int(value)
                self.props['elevation'] = new_val
            except ValueError:
                # reset GUI to last-accepted val
                self.wx_items['TextEntry']['elevation'].SetValue(str(self.props['elevation']))
        self.update_mtc()

    def update_fitness(self, event):
        """updates fitness prop"""
        value = event.GetEventObject().GetValue()
        if value:
            self.props['fitness'] = value
        self.update_mtc()

    def update_travel_mode(self, event):
        """updates travel_mode prop"""
        value = event.GetEventObject().GetValue()
        if value:
            self.props['travel_mode'] = value
        self.update_mtc()

    def update_units(self, event):
        """updates units prop"""
        value = event.GetEventObject().GetLabel()
        if value:
            self.props['units'] = value
        self.update_mtc()

    def reset(self, event):
        """resets all values"""
        event.GetTimestamp()
        self.props = self.init_props()
        self.wx_items['TextEntry']['distance'].SetValue(str(self.props['distance']))
        self.wx_items['TextEntry']['elevation'].SetValue(str(self.props['elevation']))
        self.wx_items['RadioButton']['fitness'].SetValue(str(self.props['fitness']))
        self.wx_items['RadioButton']['travel_mode'].SetValue(str(self.props['travel_mode']))
        # leave units as the user selected
        self.update_mtc()

    # other routines
    def update_mtc(self):
        """updates mtc, the final result the user wants"""
        if (self.props['distance'] is None) or (self.props['elevation'] is None):
            return

        est = munter.time_calc(self.props['distance'],
                               self.props['elevation'],
                               self.props['fitness'],
                               self.props['travel_mode'],
                               self.props['units'])

        hours = int(est['time'])
        minutes = int((est['time'] - hours) * 60)
        self.wx_items['StaticText']['mtc'].SetLabel("{human_time}".format(
            human_time="{hours} hours {minutes} minutes".format(
                hours=hours,
                minutes=minutes)))

        self.pnl.Layout()

def startup():
    """kick off the GUI"""
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()

    app.MainLoop()
