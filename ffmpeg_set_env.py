import zipfile
import os
import winreg
import ctypes

def set_path(path):
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"System\CurrentControlSet\Control\Session Manager\Environment",0, winreg.KEY_ALL_ACCESS)
    value, type = winreg.QueryValueEx(key, "Path")
    # print(value)
    if path not in value:    
        if value[-1] == ";":
            winreg.SetValueEx(key,'Path',0, winreg.REG_EXPAND_SZ,value+path)
        else:
            winreg.SetValueEx(key,'Path',0, winreg.REG_EXPAND_SZ,value+";"+path)
    value, type = winreg.QueryValueEx(key, "Path")
    # print(value)
    
    winreg.CloseKey(key)
    # 注册表更新环境变量
    HWND_BROADCAST = 0xFFFF 
    WM_SETTINGCHANGE = 0x1A 
    SMTO_ABORTIFHUNG = 0x0002 
    result = ctypes.c_long() 
    SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW 
    SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))


def unzip(ffmpeg_path):
    zip_file = zipfile.ZipFile(r"ffmpeg.zip")
    zip_list = zip_file.namelist() # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f,ffmpeg_path) # 循环解压文件到指定目录
    zip_file.close() # 关闭文件，必须有，释放内存



def set_ffmepg_env():
    ffmpeg_path = r"C:\Program Files\ffmpeg-4.2.2"
    if not os.path.exists(ffmpeg_path):
        os.makedirs(ffmpeg_path)
    unzip(ffmpeg_path)
    set_path(ffmpeg_path)

set_ffmepg_env()
# s = os.popen('ffmpeg')
