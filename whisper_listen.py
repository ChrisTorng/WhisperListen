import webrtcvad
import pyaudio
import numpy as np
from dev import printa, printa_end, printtv, init_print
from whisper_online import FasterWhisperASR
from types import SimpleNamespace
import time
import sys
from recording import print_microphones, get_device_name

MODEL_SIZE="tiny"
# MODEL_SIZE="base"
# DEVICE_TYPE="cuda_float16"
DEVICE_TYPE="cpu_int8"

RATE = 16000
FRAMES_PER_BUFFER = int(RATE * 0.03)  # 30ms=480, tried the max supported

class WhisperListener:
    def __init__(self, model_size=MODEL_SIZE, device_type=DEVICE_TYPE, input_device_index=None):
        self.vad = webrtcvad.Vad(3)
        self.pa = pyaudio.PyAudio()
        self.asr = FasterWhisperASR("zh", device_type, model_size)
        self.asr.use_vad()
        self.input_device_index = input_device_index

        # VAD parameters
        self.finished_speech_seconds = 0.5
        self.longest_speech_seconds = 4
        self.active_since = 0
        self.inactive_session = False
        self.inactive_since = time.time()
        self.frames = []

    def keep_listen(self, data):
        if data is None:
            return True
        
        is_active = self.vad.is_speech(data, sample_rate=RATE)
        current_time = time.time()

        if is_active:
            if self.active_since == 0:
                self.active_since = current_time
            self.inactive_session = False
        else:
            if not self.inactive_session:
                self.inactive_session = True
                self.inactive_since = current_time

        if ((self.inactive_session and 
             self.active_since != 0 and 
             current_time - self.inactive_since > self.finished_speech_seconds) or 
            (self.active_since != 0 and 
             current_time - self.active_since > self.longest_speech_seconds)):

            printa_end(f'X {current_time - self.active_since:.3f}')
            self.active_since = 0
            self.inactive_session = False
            return False
        else:
            printa('1' if is_active else '_')
            return True

    def listen(self):
        """錄製音訊直到靜音或超時"""
        stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            input_device_index=self.input_device_index,
            frames_per_buffer=FRAMES_PER_BUFFER
        )

        self.frames = []
        data = None
        while self.keep_listen(data):
            data = stream.read(FRAMES_PER_BUFFER)
            self.frames.append(data)

        stream.close()
        return b''.join(self.frames)

    def transcribe(self, audio_bytes):
        """使用 Whisper 模型進行語音識別"""
        try:
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            result = self.asr.transcribe(audio_np) #, init_prompt="中華電信語音客服，繁體中文台灣口音。")
            if result:
                text = ' '.join([segment.text for segment in result])
                return text.strip()
        except Exception as e:
            printtv(f"識別過程發生錯誤: {str(e)}")
        return ""

def main():
    # 初始化 dev 模組設定
    args = SimpleNamespace(
        show_timing=False,
        verbose=False,
        vad_progress=True  # 啟用 VAD 進度顯示
    )
    init_print(args)
    
    # 處理命令列參數
    if len(sys.argv) == 1:
        print_microphones()
        return
        
    try:
        device_index = int(sys.argv[1])
        device_name = get_device_name(device_index)
        if device_name is None:
            print(f"錯誤：找不到索引 {device_index} 的麥克風裝置")
            print_microphones()
            return
            
        listener = WhisperListener(input_device_index=device_index)
        print(f"\n使用麥克風：[{device_index}] {device_name}")
        
        while True:
            try:
                audio = listener.listen()
                text = listener.transcribe(audio)
                print(text)
                    
            except KeyboardInterrupt:
                print("\n程式結束")
                break
            except Exception as e:
                print(f"發生錯誤: {str(e)}")
                
    except ValueError:
        print("請提供有效的麥克風裝置索引值")
        print_microphones()

if __name__ == "__main__":
    main()
