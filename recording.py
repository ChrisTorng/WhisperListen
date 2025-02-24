import pyaudio

def list_microphones():
    """列出所有可用的麥克風裝置"""
    pa = pyaudio.PyAudio()
    devices = []
    
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        
        if (device_info['maxInputChannels'] > 0):
        # if (device_info['maxInputChannels'] > 0 and
        #     'MME' in pa.get_host_api_info_by_index(device_info['hostApi'])['name']):
            
            name = device_info['name']
                
            devices.append({
                'index': i,
                'name': name,
                'hostApi': pa.get_host_api_info_by_index(device_info['hostApi'])['name'],
                'channels': device_info['maxInputChannels'],
                'sample_rate': int(device_info['defaultSampleRate'])
            })
    
    pa.terminate()
    return devices

def print_microphones():
    """顯示所有可用的麥克風裝置"""
    devices = list_microphones()
    print("\n可用的麥克風裝置：")
    for device in devices:
        print(f"[{device['index']}] {device['hostApi']}: {device['name']}")

def get_device_name(index):
    """取得指定索引的裝置名稱"""
    devices = list_microphones()
    for device in devices:
        if device['index'] == index:
            return device['name']
    return None
