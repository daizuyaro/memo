# リミットスイッチがopenの時間を計測する
# プレス機などに設置されているリミットスイッチに利用
# 起動後 Start the Monitoring のボタンを押してプログラムを開始できる
# 修了時はExit the Program のボタンを押してプログラムを終了する
# 結果は C:\CT.csv に保存されている

import serial

# I/O USBGPIO8の設定
#com = serial.Serial("COM6", 115200, timeout=0.01)
#com_open = com.is_open

#command_mes_val = "%EE#R"+ RMD +"1"+"\r"
#command_mes_val = b"%EE#RMD1**\r\n"
#command_init = b"%EE#INT\r\n"
#command_analog = b"%EE#RAH1\r\n"
#command_test = b"%EE#INT**\r\n"

def loop(com, command):
    while True:
        com.write(command)
        read = com.readall().decode('utf-8')
        read = read[7:16]
        return read