import PySimpleGUIQt as sg
# use psutil?

menu_def = ['NULL', ['Preferences', '---', 'Start Monitoring', 'Pause Monitoring', '---', 'Exit']]

tray = sg.SystemTray(menu=menu_def, filename=r'icon.png', tooltip='System Monitor Control Panel')

prefMenu = [[sg.Text('Some text')], [sg.Button('Exit')]]

while True:
    tray_selection = tray.Read()
    if tray_selection == 'Exit':
        break
    if tray_selection == 'Preferences':
        window = sg.Window('System Monitor Control Panel', prefMenu, finalize=True)

    pref_selection = window.Read()
    if pref_selection == 'Exit':
        break