# Huawei LTE router signal plotter

A simple Python script that will monitor the signal strength indicators
of Huawei LTE routers (tested on a B315 router, but will probably work
on others with a compatible API).

Four different signal indicators are plotted: RSRQ, SINR, RSRP and RSSI.
The former two are measured in dB, while the latter two are measured in
dBm. For the meaning of the values, see
http://knowledgebase.cradlepoint.com/articles/Support/Modem-Signal-Strength-and-Signal-Quality.

The script requires a somewhat recent matplotlib and uses the animation
feature to plot the signal values over time. Adjust the variables at the
top of the Python script to point at your liking (including pointing it
at the right address for the router), and just run the script with
`python huawei-snr.py`.

There's not much in the way of error checking, so if it crashes it's
probably because the router can't be reached or doesn't respond to the
right API (it must return signal information from the
`/api/device/signal` endpoint).

The VXLabs Android app that monitors the same API was useful for
figuring out how to use the API. The app is here: https://vxlabs.com/stats-for-huawei-lte-routers/
