# -*- coding: utf-8 -*-
#
# huawei-snr.py
#
# Author:   Toke Høiland-Jørgensen (toke@toke.dk)
# Date:     29 June 2017
# Copyright (c) 2017, Toke Høiland-Jørgensen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function, unicode_literals

import requests
import xml.etree.ElementTree as ET

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import cycle
from functools import reduce

#
# Configuration
#

BASE_URL = "http://192.168.8.1"  # router address
INTERVAL = 1000  # milliseconds
DURATION = 120   # time steps of length INTERVAL
COLOURS = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a",
           "#66a61e", "#e6ab02", "#a6761d", "#666666"]

#
# End configuration
#

API_URL = BASE_URL + "/api/device/signal"

ses = requests.session()
ses.get(BASE_URL)  # sets session cookie needed for API calls


def get_vals():
    r = ses.get(API_URL)
    e = ET.fromstring(r.text)
    res = {}
    for c in e:
        res[c.tag] = c.text
        if res[c.tag].startswith("&gt;="):
            res[c.tag] = res[c.tag][5:]

    res['rsrq'] = int(res['rsrq'][:-2])
    res['sinr'] = int(res['sinr'][:-2])
    res['rsrp'] = int(res['rsrp'][:-3])
    res['rssi'] = int(res['rssi'][:-3])
    return res


fig = plt.figure()
ax1 = fig.gca()
ax2 = fig.add_axes(ax1.get_position(), sharex=ax1, frameon=False)
ax2.yaxis.tick_right()

col = cycle(COLOURS)


ln = {}
ln['rsrq'], = ax1.plot([], [], next(col), animated=True, label='RSRQ')
ln['sinr'], = ax1.plot([], [], next(col), animated=True, label='SINR')
ln['rsrp'], = ax2.plot([], [], next(col), animated=True, label='RSRP')
ln['rssi'], = ax2.plot([], [], next(col), animated=True, label='RSSI')


def init():
    ax1.set_ylim(-15, 15)
    ax1.set_ylabel("dB")
    ax2.set_ylim(-110, -50)
    ax2.set_ylabel("dBm")
    ax1.set_xlim(0, DURATION)
    ax1.set_xlabel("Time")
    handles, labels = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]),
                             [a.get_legend_handles_labels() for a in [ax1, ax2]])
    fig.legend(handles, labels)
    return ln.values()


def update(x):
    r = get_vals()

    for k in ln.keys():
        ar = ln[k].get_data()
        x_data = list(ar[0])
        y_data = list(ar[1])
        x_data.append(x)
        y_data.append(r[k])
        ln[k].set_data(x_data, y_data)
    return ln.values()

ani = FuncAnimation(fig, update, frames=DURATION, blit=True, repeat=False,
                    interval=INTERVAL, init_func=init)
plt.show()
