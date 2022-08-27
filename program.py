from tokenize import group
import PySimpleGUIQt as sg
from tkinter import font
# use psutil?

tray_layout = ['NULL',
               ['Preferences',
                '---',
                'Enable Monitoring',
                'Pause Monitoring',
                '---',
                'Exit']]

tray_window = sg.SystemTray(
    menu=tray_layout, filename=r'icon.png', tooltip='System Monitor Control Panel')


def pref_menu_window():
    pref_menu_title_font = ('Arial', 12, 'bold')
    pref_menu_layout = [[sg.Text('General Preferences', font=pref_menu_title_font)],
                        [sg.Text('System Polling Interval (ms)'),
                         sg.In(key='-SYS-POLL-INTERVAL-')],
                        [sg.Text('Monitor Display Theme'), sg.Combo(
                            ['Theme 1', 'Theme 2'], readonly=True)],
                        [sg.HorizontalSeparator()],
                        [sg.Text('CPU Monitoring', font=pref_menu_title_font)],
                        [sg.Checkbox('CPU Clock Speed', default=True)],
                        [sg.Radio('Show Peak Core Clock Speed', group_id='cpu_clock_display_type', default=True), sg.Radio(
                            'Show Individual Core Clock Speeds', group_id='cpu_clock_display_type')],
                        [sg.Checkbox('CPU Temperature', default=True)],
                        [sg.Radio('Celcius', group_id='cpu_temp_display_type', default=True), sg.Radio(
                            'Farenheit', group_id='cpu_temp_display_type')],
                        [sg.Button('Apply && Save Changes'), sg.Button('Exit')]]

    pref_menu_window = sg.Window(
        'System Monitor Preferences', pref_menu_layout)

    while True:
        pref_event, pref_values = pref_menu_window.read()
        if pref_event in (None, 'Exit'):
            print('Exiting Preferences')
            break

    pref_menu_window.close()


while True:
    tray_event = tray_window.read()
    if tray_event == 'Exit':
        break
    if tray_event == 'Preferences':
        pref_menu_window()

tray_window.close()
