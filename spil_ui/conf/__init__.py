try:
    from spil_ui.conf.qtui_conf_load import *
except Exception as e:
    raise Exception('Unable to import the spil_qtui_conf file. \n'
                    'Please check the files compatibility with the latest SPIL version.')
