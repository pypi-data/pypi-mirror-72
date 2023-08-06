# -*- coding: utf-8 -*-
#
#   Copyright © 2015 - 2020 Stephan Zevenhuizen
#   debugger_MATE_for_Dummies, (27-06-2020).
#

# You must open an experiment in MATRIX with an I(t) channel first.


import mate4dummies.objects as mo

def read_prop(obj, prop):
    out = getattr(obj, prop)()
    print(prop + ':', out)

channel_props = ['Enable', 'Enable_Storing']
clock_props = ['Enable', 'Period', 'Samples']
experiment_props = ['Bricklet_Ready', 'Bricklet_Written', 'Name',
                    'Result_File_Name', 'Result_File_Path', 'State']
gap_voltage_control_props = ['Preamp_Range', 'Voltage']
piezo_control_props = ['Approach', 'Move_Auto', 'Move_Backward', 'Move_Forward',
                       'Move_Tip_X_Minus', 'Move_Tip_X_Plus',
                       'Move_Tip_Y_Minus', 'Move_Tip_Y_Plus', 'Retract']
regulator_props = ['Enable_Z_Offset_Slew_Rate', 'Feedback_Loop_Enabled',
                   'Loop_Gain_1_I', 'Loop_Gain_2_I', 'Preamp_Range_1',
                   'Preamp_Range_2', 'Setpoint_1', 'Setpoint_2', 'Z_Offset',
                   'Z_Offset_Slew_Rate', 'Z_Out']
spectroscopy_props = ['Aux1_Range', 'Device_1_End', 'Device_1_Points',
                      'Device_1_Repetitions', 'Device_1_Start', 'Device_2_End',
                      'Device_2_Offset_Delay', 'Device_2_Points',
                      'Device_2_Repetitions', 'Device_2_Start',
                      'Enable_Device_1_Ramp_Reversal',
                      'Enable_Device_2_Ramp_Reversal', 'Enable_Feedback_Loop',
                      'Raster_Time_1', 'Raster_Time_2', 'Spectroscopy_Mode']
stm_scb_service_props = ['VGap_Out_Mod_Select', 'VGap_Select']
view_props = ['Cycle_Count', 'Data', 'Data_Size', 'Deliver_Data',
              'Packet_Count', 'Run_Count']
xy_scanner_props = ['Angle', 'Area', 'Enable_Drift_Compensation',
                    'Enable_Execute_Port', 'Execute', 'Execute_Port_Colour',
                    'Lines', 'Move_Raster_Time', 'Move_Raster_Time_Constrained',
                    'Offset', 'Plane_X_Slope', 'Plane_Y_Slope', 'Points',
                    'Points_Lines_Constrained', 'Raster_Time',
                    'Return_To_Stored_Position', 'Scan_Area_Configured',
                    'Store_Current_Position', 'Target_Position', 'Trigger_1',
                    'Trigger_2', 'Trigger_Execute_At_Target_Position',
                    'XY_Position_Reached', 'XY_Position_Report',
                    'XY_Position_Return', 'X_Drift', 'X_Retrace',
                    'X_Retrace_Done', 'X_Retrace_Trigger', 'X_Trace_Done',
                    'X_Trace_Trigger', 'Y_Drift', 'Y_Retrace', 'Y_Retrace_Done',
                    'Y_Retrace_Trigger', 'Y_Trace_Done', 'Y_Trace_Trigger']
obj_names = ['channel', 'clock', 'experiment', 'gap_voltage_control',
             'piezo_control', 'regulator', 'spectroscopy', 'stm_scb_service',
             'view', 'xy_scanner']
mo.mate.testmode = False
mo.mate.connect()
if mo.mate.online:
    mo.channel_name = 'I_t'
    mo.get_clock_name(mo.channel_name)
    for obj_name in obj_names:
        obj = getattr(mo, obj_name)
        print()
        print('Object ' + obj_name + ':')
        print('--------------------------------------------------------------')
        for prop in eval(obj_name + '_props'):
            read_prop(obj, prop)
    print()
    mo.list_channels()
    mo.mate.disconnect()
