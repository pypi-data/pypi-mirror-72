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

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.SetTitle(progname)
        self.SetSize(600, 400)

        self.props = self.init_props()

        self.pnl = wx.Panel(self)

        st = wx.StaticText(self.pnl, label=progname)
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()

        st.SetFont(font)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 0))

        # text entry fields
        self.st_distance = wx.StaticText(self.pnl, label="Distance: ", style=wx.ALIGN_RIGHT)
        self.te_distance = wx.TextCtrl(self.pnl, value="0", size=(140, -1))

        self.st_elevation = wx.StaticText(self.pnl, label="Elevation: ", style=wx.ALIGN_RIGHT)
        self.te_elevation = wx.TextCtrl(self.pnl, value="0", size=(140, -1))

        self.st_fitness   = wx.StaticText(self.pnl, label="Fitness: ", style=wx.ALIGN_RIGHT)
        rb_fitness_choices = ['slow', 'average', 'fast']
        rb_fitness_default = 'average'
        self.rb_fitness   = wx.ComboBox(self.pnl, choices=rb_fitness_choices,
                value=rb_fitness_default, style=wx.CB_READONLY)

        self.st_travel_mode    = wx.StaticText(self.pnl, label="Travel Mode: ", style=wx.ALIGN_RIGHT)
        rb_travel_mode_choices = ['uphill', 'flat', 'downhill', 'bushwhacking']
        rb_travel_mode_default = 'uphill'
        self.rb_travel_mode    = wx.ComboBox(self.pnl,
            choices=rb_travel_mode_choices,
            value=rb_travel_mode_default, style=wx.CB_READONLY)

        self.st_units   = wx.StaticText(self.pnl, label="Units: ", style=wx.ALIGN_RIGHT)
        rb_units_choices = ['imperial', 'metric']
        rb_units_default = 'imperial'

        self.rb_units = []
        for choice in range(len(rb_units_choices)):
            label = rb_units_choices[choice]
            style = wx.RB_GROUP if not choice else 0
            self.rb_units.append(wx.RadioButton(self.pnl, label=label, style=style))

        # static text
        self.st_mtc = wx.StaticText(self.pnl, label="",
                style=wx.ALIGN_CENTRE_HORIZONTAL)

        st_mtc_font = st.GetFont()
        st_mtc_font.PointSize += 10
        self.st_mtc.SetFont(st_mtc_font)

        # buttons
        self.b_reset = wx.Button(self.pnl, wx.NewId(), '&Reset', (-1, -1),
                wx.DefaultSize)

        # bindings
        self.pnl.Bind(wx.EVT_TEXT, self.update_distance, self.te_distance)
        self.pnl.Bind(wx.EVT_TEXT, self.update_elevation, self.te_elevation)
        self.rb_fitness.Bind(wx.EVT_COMBOBOX, self.update_fitness)
        self.rb_travel_mode.Bind(wx.EVT_COMBOBOX, self.update_travel_mode)
        self.b_reset.Bind(wx.EVT_BUTTON, self.reset)

        for cb in self.rb_units:
            cb.Bind(wx.EVT_RADIOBUTTON, self.update_units)

        # layout
        b = 5
        w = 100

        static_line = wx.StaticLine(self.pnl, wx.NewId(), style=wx.LI_HORIZONTAL)

        hsizer_distance = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_distance.Add(self.st_distance, 0, wx.RIGHT, b)
        hsizer_distance.Add(self.te_distance, 1, wx.GROW, b)
        hsizer_distance.SetItemMinSize(self.st_distance, (w, -1))

        hsizer_elevation = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_elevation.Add(self.st_elevation, 0, wx.RIGHT, b)
        hsizer_elevation.Add(self.te_elevation, 1, wx.GROW, b)
        hsizer_elevation.SetItemMinSize(self.st_elevation, (w, -1))

        hsizer_fitness = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_fitness.Add(self.st_fitness, 0, wx.RIGHT, b)
        hsizer_fitness.Add(self.rb_fitness, 1, wx.GROW, b)
        hsizer_fitness.SetItemMinSize(self.st_fitness, (w, -1))

        hsizer_travel_mode = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_travel_mode.Add(self.st_travel_mode, 0, wx.RIGHT, b)
        hsizer_travel_mode.Add(self.rb_travel_mode, 1, wx.GROW, b)
        hsizer_travel_mode.SetItemMinSize(self.st_travel_mode, (w, -1))

        hsizer_units = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_units.Add(self.st_units, 0, wx.RIGHT, b)
        for cb in range(len(self.rb_units)):
            hsizer_units.Add(self.rb_units[cb], cb + 1, wx.GROW, b)
        hsizer_units.SetItemMinSize(self.st_units, (w, -1))

        hsizer_mtc = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_mtc.Add(self.st_mtc, 1, wx.GROW, b)
        hsizer_mtc.SetItemMinSize(self.st_mtc, (w, -1))

        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5.Add(self.b_reset, 0)

        b = 5
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(sizer, 0, wx.EXPAND | wx.ALL, b*b)
        vsizer1.Add(hsizer_distance, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer_elevation, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer_fitness, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer_travel_mode, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer_units, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(hsizer_mtc, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(static_line, 0, wx.GROW | wx.ALL, b)
        vsizer1.Add(hsizer5, 0, wx.ALIGN_RIGHT | wx.ALL, b)

        self.pnl.SetSizerAndFit(vsizer1)
        self.pnl.SetClientSize(vsizer1.GetSize())
        self.update_mtc()

    def init_props(self):
        props = dict()
        props['distance'] = 0
        props['elevation'] = 0
        props['fitness'] = 'average'
        props['units'] = 'imperial'
        props['travel_mode'] = 'uphill'
        return props

    def update_distance(self, event):
        value = self.te_distance.GetValue()
        if value:
            try:
                new_val = float(value)
                self.props['distance'] = new_val
            except:
                # reset GUI to last-accepted val
                self.te_distance.SetValue(str(self.props['distance']))
                pass
        self.update_mtc()

    def update_elevation(self, event):
        value = self.te_elevation.GetValue()
        if value:
            try:
                new_val = int(value)
                self.props['elevation'] = new_val
            except:
                # reset GUI to last-accepted val
                self.te_elevation.SetValue(str(self.props['elevation']))
                pass
        self.update_mtc()

    def update_fitness(self, event):
        value = self.rb_fitness.GetValue()
        if value:
            self.props['fitness'] = value
        self.update_mtc()

    def update_travel_mode(self, event):
        value = self.rb_travel_mode.GetValue()
        if value:
            self.props['travel_mode'] = value
        self.update_mtc()

    def update_units(self, event):
        rb = event.GetEventObject()
        value = rb.GetLabel()
        if value:
            self.props['units'] = value
        self.update_mtc()

    def update_mtc(self):
        if (self.props['distance'] is None) or (self.props['elevation'] is None):
            return

        est = munter.time_calc(self.props['distance'],
            self.props['elevation'],
            self.props['fitness'],
            self.props['travel_mode'],
            self.props['units'])

        hours = int(est['time'])
        minutes = int((est['time'] - hours) * 60)
        self.st_mtc.SetLabel("{human_time}".format(
                human_time="{hours} hours {minutes} minutes".format(
                    hours=hours,
                    minutes=minutes)))

        self.pnl.Layout()

    def reset(self, event):
        self.props = self.init_props()
        self.te_distance.SetValue(str(self.props['distance']))
        self.te_elevation.SetValue(str(self.props['elevation']))
        self.rb_fitness.SetValue(str(self.props['fitness']))
        self.rb_travel_mode.SetValue(str(self.props['travel_mode']))
        # leave units as the user selected
        self.update_mtc()

def startup():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()

    app.MainLoop()
