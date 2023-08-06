# -*- coding: utf-8 -*-
#
#   Copyright © 2020 Stephan Zevenhuizen
#   start_MATE_for_Dummies_3, (28-06-2020).
#

# You must open an experiment in MATRIX with Z and Aux1(V) channels first.

# Run this script from within the MS Windows Command Prompt (console),
# by pressing the keyboard Esc key you can stop the 'wait for event' loop.
# For simplicity, this script cannot run in test mode.
# You need the Python packages numpy.

import mate4dummies.objects as mo
import numpy as np
import time

def move_to_random_target():
    global scan_start_time
    target_pos = tuple(np.random.rand(1, 2)[0] * 2 - 1)
    print('\nNew target position:', target_pos)
    mo.xy_scanner.Target_Position(target_pos)
    scan_start_time = time.time()
    mo.xy_scanner.move()

def after_sps():
    global nr_sps_done
    nr_sps_done += 1
    print('Single point spectroscopy nr. {0:d} done.'.format(nr_sps_done))

def after_trace_scan():
    global trace_scan_done
    trace_scan_done = True
    print('Up XY-scan done.')
    mo.experiment.stop()
    mo.xy_scanner.Return_To_Stored_Position(False)
    mo.xy_scanner.Trigger_Execute_At_Target_Position(True)


mo.mate.connect()
if mo.mate.online:
    value = mo.experiment.State()
    if value in ['stopped', 'running', 'paused']:
        if value != 'paused':
            mo.experiment.pause()
            time.sleep(0.5)
        mo.experiment.stop()
        time.sleep(0.5)
        while not mo._no_event():
            time.sleep(0.05)
        mo.channel_name = 'Z'
        mo.channel.Enable(True)
        mo.channel.Enable_Storing(True)
        mo.channel_name = 'Aux1_V'
        mo.channel.Enable(True)
        mo.channel.Enable_Storing(True)
        mo.list_channels()
        mo.spectroscopy.Spectroscopy_Mode(0)
        mo.spectroscopy.Enable_Device_1_Ramp_Reversal(False)
        # .... more optional settings from Python script
        repetitions = 1
        mo.spectroscopy.Device_1_Repetitions(repetitions)
        mo.xy_scanner.Enable_Execute_Port(True)
        mo.xy_scanner.Execute_Port_Colour('')
        mo.xy_scanner.XY_Position_Return(after_sps)
        mo.xy_scanner.Y_Trace_Done(after_trace_scan)
        mo.xy_scanner.Y_Trace_Trigger(True)
        mo.xy_scanner.Y_Retrace(False)
        mo.esc = False
        scan_start_time = time.time()
        mo.experiment.start()
        trace_scan_done = False
        while (not trace_scan_done and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']
               and not mo.esc):
            mo.wait_for_event()
        suffix = '.' + mo.mate.channels.Z.display_name + '_mtrx'
        result_files = mo.wait_for_files(suffix, scan_start_time, 1) # Optional
        # Optionally access the result files with access2theMatrix and
        # analyze the data.
        # ....
        suffix = '.' + mo.mate.channels.Aux1_V.display_name + '_mtrx'
        nr_sps_done = 0
        while (nr_sps_done < 3 and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS'] and
               not mo.esc):
            move_to_random_target()
            mo.wait_for_event()
            result_files = mo.wait_for_files(suffix, scan_start_time,
                                             repetitions) # Optional
            # Optionally access the result files with access2theMatrix and
            # analyze the data.
            # ....
        mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
        mo.xy_scanner.Y_Trace_Trigger(False)
        mo.xy_scanner.Y_Trace_Done()
        mo.xy_scanner.XY_Position_Return()
    else:
        mo.log.AppendText('Can\'t continue in state ' + value + '.\n')
    mo.mate.disconnect()
