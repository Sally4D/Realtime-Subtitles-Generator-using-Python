# 🎙️ VoiceFlow

**Real-time live captioning for your desktop audio**

VoiceFlow is a powerful, lightweight desktop application that provides real-time captions for any audio playing on your computer. Whether you're watching videos, attending online meetings, or listening to podcasts, VoiceFlow captures your system audio and displays live captions in a sleek, draggable overlay window.

## ✨ Features

- **Real-time Speech Recognition**: Converts system audio to text in real-time using Vosk
- **System Audio Capture**: Captures audio directly from your speakers/headphones
- **Draggable Overlay**: Semi-transparent, always-on-top window that you can move anywhere
- **Smart Line Management**: Automatically manages caption flow with intelligent line breaks
- **Pause Detection**: Detects speech pauses and starts new caption lines automatically
- **Partial Results**: Shows real-time transcription progress with partial results
- **Lightweight**: Minimal resource usage with efficient threading
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Audio output device (speakers/headphones)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voiceflow.git
   cd voiceflow
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Vosk Model**
   
   Download a Vosk model for speech recognition:
   ```bash
   # For English (Small model - ~40MB)
   wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip
   ```
   
   Or download manually from [Vosk Models](https://alphacephei.com/vosk/models) and extract to your project directory.

4. **Update model path**
   
   Edit `EnhancedApp.py` and update the `MODEL_PATH` variable:
   ```python
   MODEL_PATH = "vosk-model-small-en-us-0.15"  # Your model directory name
   ```

5. **Run VoiceFlow**
   ```bash
   python EnhancedApp.py
   ```

## 🛠️ Configuration

### Model Selection

VoiceFlow supports various Vosk models with different sizes and languages:

| Model | Size | Language | Accuracy |
|-------|------|----------|----------|
| vosk-model-small-en-us-0.15 | ~40MB | English (US) | Good |
| vosk-model-en-us-0.22 | ~1.8GB | English (US) | Excellent |
| vosk-model-small-en-in-0.4 | ~40MB | English (India) | Good |

### Adjustable Parameters

Edit these variables in `EnhancedApp.py`:

```python
SAMPLE_RATE = 16000          # Audio sample rate (Hz)
BLOCK_SIZE = 2000           # Audio processing block size
DELAY_THRESHOLD = 1.0       # Pause detection threshold (seconds)
```

### Window Customization

Modify the `CaptionWindow` class for appearance:
- Font size and family
- Window transparency (`alpha` value)
- Text wrapping width
- Window dimensions and position

## 🎛️ Usage

### Basic Operation

1. **Launch**: Run `python EnhancedApp.py`
2. **Position**: Drag the caption window to your preferred location
3. **Listen**: Play any audio on your computer - VoiceFlow will automatically caption it
4. **Close**: Close the window or press Ctrl+C in the terminal

### Window Controls

- **Drag**: Click and drag the caption text to move the window
- **Always on Top**: Window stays above all other applications
- **Semi-transparent**: Background is semi-transparent for minimal distraction

### Audio Sources

VoiceFlow captures audio from:
- System audio/speakers
- Application audio (videos, music, calls)
- Loopback audio from your default output device

## 🔧 Troubleshooting

### Common Issues

**"Another app is using the audio device in exclusive mode"**
- Close applications that might have exclusive audio access
- Try restarting VoiceFlow
- Check Windows audio settings for exclusive mode

**"Failed to load model"**
- Verify the model path in `MODEL_PATH` variable
- Ensure the model directory exists and contains required files
- Download the model again if corrupted

**No audio captured**
- Check your default audio output device
- Ensure audio is actually playing
- Try running as administrator (Windows)
- Check system audio permissions (macOS/Linux)

**Poor recognition accuracy**
- Use a larger, more accurate Vosk model
- Ensure clear audio without background noise
- Check that the correct language model is being used

### Platform-Specific Notes

**Windows:**
- May require running as administrator for system audio capture
- Ensure Windows audio drivers are up to date

**macOS:**
- Grant microphone permissions in System Preferences
- May need additional audio routing software

**Linux:**
- Install ALSA or PulseAudio development packages
- Check audio device permissions

## 🏗️ Architecture

VoiceFlow uses a multi-threaded architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Audio Thread  │───▶│   Audio Queue    │───▶│  Speech Thread  │
│ (Capture Audio) │    │                  │    │ (Process Audio) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GUI Thread    │◀───│  Caption Queue   │◀───│  Recognition    │
│ (Display Text)  │    │                  │    │     Engine      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📦 Dependencies

- **tkinter**: GUI framework (included with Python)
- **soundcard**: Audio capture from system output
- **vosk**: Speech recognition engine
- **numpy**: Audio data processing
- **threading**: Multi-threaded processing
- **queue**: Thread-safe data exchange

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** if applicable
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/voiceflow.git
cd voiceflow

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # For testing and formatting

# Run tests
pytest

# Format code
black .
```

## 📋 Roadmap

- [ ] **Multiple Language Support**: Support for more Vosk language models
- [ ] **Audio Source Selection**: Choose specific applications or devices
- [ ] **Caption History**: Save and review caption history
- [ ] **Customizable Themes**: Multiple UI themes and color schemes
- [ ] **Keyboard Shortcuts**: Global hotkeys for control
- [ ] **Export Functionality**: Export captions to text/SRT files
- [ ] **Cloud Recognition**: Integration with cloud speech services
- [ ] **Plugin System**: Extensible architecture for add-ons

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - Open-source speech recognition toolkit
- [SoundCard](https://github.com/bastibe/SoundCard) - Audio capture library
- All contributors and users who help improve VoiceFlow

## 📞 Support

Having issues? Here's how to get help:

1. **Check the [Troubleshooting](#-troubleshooting) section**
2. **Search existing [Issues](https://github.com/yourusername/voiceflow/issues)**
3. **Create a new issue** with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 🌟 Show Your Support

If VoiceFlow helps you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🔀 Contributing code
- 📢 Sharing with others

---

**Made with ❤️ for accessibility and inclusion**
