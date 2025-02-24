# WhisperListen

```bash
python -m venv .venv
.venv\Scripts\activate
pip install librosa sounddevice
pip install faster-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install webrtcvad-wheels
pip install pyaudio keyboard
#set PYTHONIOENCODING=utf-8
python whisper_listen.py
python whisper_listen.py 0
```