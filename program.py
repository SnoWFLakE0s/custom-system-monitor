import PySimpleGUIQt as sg
import PySimpleGUI as sgTk
from json import (load as jsonload, dump as jsondump)
from os import path
# use psutil?

SETTINGS_FILE = sgTk.user_settings_filename(filename='ehwmsettings', path=r'C:\\Program Files\\ExternalSystemMonitor\\ehwmsettings')
DEFAULT_SETTINGS = {'system_polling_interval': 50, 'menu_theme': sg.theme(), 'cpu_hz': True, 'cpu_hz_peak': True, 'cpu_hz_all': False, 'cpu_temp': True, 'cpu_temp_c': True, 'cpu_temp_f': False}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'system_polling_interval': '-POLLING-INTERVAL-', 'menu_theme': '-MENU-THEME-', 'cpu_hz': '-CPU-HZ-', 'cpu_hz_peak': '-CPU-HZ-PEAK-', 'cpu_hz_all': '-CPU-HZ-ALL-', 'cpu_temp': '-CPU-TEMP-', 'cpu_temp_c': '-CPU-TEMP-C-', 'cpu_temp_f': '-CPU-TEMP-F-'}

########################################## Load/Save Settings File ##########################################
def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... Generating default', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

######################################## System Tray Applet Function ########################################
"""
  The actual system tray applet that the user will primarily interact with to open the settings menu,
  start/stop monitoring, or quit the software as necessary.
"""

def system_tray():
    tray_layout = ['NULL',
                   ['Preferences',
                    '---',
                    'Enable Monitoring',
                    'Pause Monitoring',
                    '---',
                    'Exit']]

    tray_window = sg.SystemTray(menu=tray_layout, filename=r'icon.png', tooltip='System Monitor Control Panel')

    while True:
        tray_event = tray_window.read()
        if tray_event == 'Exit':
            break
        if tray_event == 'Preferences':
            pref_menu_window()

    tray_window.close()

"""
  The interface for the settings menu. 
"""

def pref_menu_window():
  sg.theme(settings['menu_theme'])
  title_font = ('Roboto', 14, 'bold')
  body_font = ('Roboto', 12)

  pref_menu_layout = [[sg.Text('General Preferences', font=title_font)],

                      [sg.Text('System Polling Interval (ms)', font=body_font), sg.In(key='-POLLING-INTERVAL-')],
                      [sg.Text('Monitor Display Theme', font=body_font), sg.Combo(['Theme 1', 'Theme 2'], readonly=True, key='-MENU-THEME-')],

                      [sg.HorizontalSeparator()],

                      [sg.Text('CPU Monitoring', font=title_font)],

                      [sg.Checkbox('CPU Clock Speed', font=body_font, default=True, key='-CPU-HZ-')],
                      [sg.Radio('Show Peak Core Clock Speed', font=body_font, group_id='cpu_clock_display_type', default=True, key='-CPU-HZ-PEAK-'), sg.Radio('Show Individual Core Clock Speeds', font=body_font, group_id='cpu_clock_display_type', key='-CPU-HZ-ALL-')],
                      [sg.Checkbox('CPU Temperature', font=body_font, default=True, key='-CPU-TEMP-')],
                      [sg.Radio('Celcius', font=body_font, group_id='cpu_temp_display_type', default=True, key='-CPU-TEMP-C-'), sg.Radio('Farenheit', font=body_font, group_id='cpu_temp_display_type', key='-CPU-TEMP-F-')],

                      [sg.Button('Apply && Save Changes', font=body_font, pad=25), sg.Button('Exit', font=body_font, pad=25)]]

  pref_menu_window = sg.Window('System Monitor Preferences', pref_menu_layout)

  while True:
      pref_event = pref_menu_window.read()
      if pref_event in (None, 'Exit'):
          print('Exiting Preferences')
          break

  pref_menu_window.close()

"""
  Exectution (main) functions
"""

def main():
  settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)
  system_tray()

main()
