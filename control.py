# Global control flag
control_flag = False

def control_function(control):
    global control_flag
    control_flag = control

def returncontrol_function():
    global control_flag
    return control_flag
