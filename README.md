# LiveScript: Real-time Live Captioning Software

A real-time audio transcription application that provides live captions for your system's audio output. Perfect for accessibility, language learning, meetings, or any situation where you need visual representation of spoken content.

## ✨ Features

### 🎤 **Real-Time Transcription**
- Live speech-to-text using Vosk offline speech recognition
- Audio loopback capture from system speakers
- Multi-threaded processing for smooth performance
- Configurable audio buffer sizes for optimal accuracy/speed balance

### 🌍 **Multi-Language Support**
- **50+ languages and dialects** supported including:
  - English (multiple variants)
  - Chinese, Russian, French, German, Spanish
  - Portuguese, Arabic, Hindi, Japanese, Korean
  - And many more regional variants
- Automatic model downloading and management
- Easy language switching through settings

### 🎨 **Customizable Appearance**
- **Caption Styling**: Custom colors, fonts, and sizes
- **Window Properties**: Adjustable width, height, opacity, and padding
- **Theme Support**: Dark/Light mode compatibility
- **Overlay Positioning**: Draggable caption window
- Real-time preview of all visual changes

### ⚙️ **Advanced Configuration**
- Audio processing parameters (block size, delay thresholds)
- Searchable dropdown menus for easy navigation
- Settings persistence with JSON configuration
- First-run setup wizard with guided tour

### 🖥️ **User Experience**
- Modern CustomTkinter interface
- Right-click context menu for quick access
- Tooltips and helpful descriptions
- Responsive, scrollable settings panel
- One-click model installation

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.7 or higher
- **RAM**: Minimum 2GB (4GB recommended for large models)
- **Storage**: 500MB - 5GB depending on language models
- **Audio**: System audio output (speakers/headphones)

### Python Dependencies
```
tkinter (usually included with Python)
customtkinter>=5.0.0
soundcard>=0.4.0
vosk>=0.3.45
numpy>=1.19.0
requests>=2.25.0
```

## 🚀 Installation

### Method 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python.git
cd livescript

# Install dependencies
pip install -r requirements.txt

# Run the application
python SubtitlesAppV1.01.py
```

### Method 2: Direct Download
1. Download the latest release from [Releases](https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python/releases)
2. Extract the archive
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python SubtitlesAppV1.01.py`

### Method 3: Requirements.txt
Create a `requirements.txt` file:
```
customtkinter>=5.0.0
soundcard>=0.4.0
vosk>=0.3.45
numpy>=1.19.0
requests>=2.25.0
```

## 🎮 Usage

### First Run
1. **Launch the application** - The About window will appear with usage instructions
2. **Right-click** the caption overlay to access settings
3. **Select your language** - The app will automatically download the required model
4. **Customize appearance** to your preferences
5. **Start speaking or play audio** - Captions will appear in real-time!

### Basic Controls
- **Move Window**: Left-click and drag the caption bar
- **Access Settings**: Right-click anywhere on the caption window
- **Quick Restart**: Use the restart option when changing languages or models

### Settings Overview

#### 🎨 **Caption Appearance**
- **Colors**: Subtitle and background colors with color picker
- **Typography**: Font family, size, and styling options
- **Layout**: Window dimensions, padding, and opacity controls
- **Positioning**: Draggable overlay with size customization

#### 🔊 **Audio & Language**
- **Language Models**: 50+ supported languages with automatic downloading
- **Audio Processing**: Block size and delay threshold adjustments
- **Model Management**: Automatic installation and status monitoring

#### ⚡ **Performance Tuning**
- **Block Size**: Lower = faster response, Higher = better accuracy
  - `1000-2000`: Fast response (good for real-time chat)
  - `3000-4000`: Balanced (recommended for most users)  
  - `5000-8000`: High accuracy (good for detailed transcription)
- **Delay Threshold**: How long to wait before clearing captions during silence

## 🛠️ Configuration

### Settings File
Settings are automatically saved to `settings.json`:
```json
{
    "subtitle_color": "#FFFFFF",
    "background_color": "#000000", 
    "background_opacity": 0.75,
    "subtitle_size": 16,
    "subtitle_font": "Arial",
    "language": "English",
    "block_size": 3000,
    "window_width": 1200,
    "window_height": 70,
    "delay_threshold": 3.0
}
```

### Model Storage
- Language models are downloaded to the application directory
- Models range from 30MB (small) to 5GB (large) depending on language
- Models are reusable and only need to be downloaded once

## 🔧 Troubleshooting

### Common Issues

#### "Could not capture audio"
- **Solution**: Check that your system has audio output devices
- **Windows**: Ensure "Stereo Mix" or similar loopback device is enabled
- **macOS**: Grant microphone permissions in System Preferences
- **Linux**: Install and configure PulseAudio or ALSA

#### "Model not found" error
- **Solution**: Open Settings → Select your language → Wait for automatic download
- **Manual**: Download models from [Vosk Models](https://alphacephei.com/vosk/models)

#### Poor transcription accuracy
- **Solution**: 
  - Increase block size in settings (try 4000-6000)
  - Ensure clear audio source
  - Try a larger language model variant
  - Check system audio levels

#### Application won't start
- **Solution**:
  - Verify Python version (3.7+)
  - Install missing dependencies: `pip install -r requirements.txt`
  - Check for port conflicts or permission issues

### Performance Optimization
- **For speed**: Use smaller models and lower block sizes
- **For accuracy**: Use larger models and higher block sizes  
- **For battery life**: Reduce processing frequency and use smaller models

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Bug Reports**: Report issues via [GitHub Issues](https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python/issues)
- 💡 **Feature Requests**: Suggest new features or improvements
- 🌍 **Language Support**: Help test and improve language models
- 📖 **Documentation**: Improve guides, README, or code comments
- 🔧 **Code**: Submit pull requests for bug fixes or new features

### Development Setup
```bash
git clone https://github.com/yourusername/livescript.git
cd livescript
pip install -r requirements.txt
# Make your changes
python SubtitlesAppV1.01.py  # Test your changes
```

### Pull Request Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages
5. Push to your fork and submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Vosk](https://alphacephei.com/vosk/)** - Offline speech recognition toolkit
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern GUI framework
- **[SoundCard](https://github.com/bastibe/SoundCard)** - Audio capture library
- **Community Contributors** - Thanks to everyone who has contributed!

## 📞 Support

- 🌟 **Star this repo** if you find it helpful!
- 🐛 **Report bugs** via [GitHub Issues]([https://github.com/sally4d/Realtime-Subtitles-Generator-using-Python
/issues](https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python/issues))
- 💬 **Discussions** for questions and feature requests
- 📧 **Email**: oscurprof@gmail.com
- 🔗 **LinkedIn**: [oscurprof](https://www.linkedin.com/in/oscurprof/)

## 🗺️ Roadmap

### Planned Features
- [ ] **Cloud Model Support** - Integration with online speech recognition APIs
- [ ] **Multi-Speaker Recognition** - Distinguish between different speakers
- [ ] **Live Captions Translation** - Translate live into any language
- [ ] **Export Functionality** - Save transcriptions to text files
- [ ] **Hotkey Support** - Keyboard shortcuts for common actions

### Version History
- **v1.01** - Initial release with core functionality
- **v1.00** - Beta testing and development

---

<div align="center">

**Made with ❤️ for accessibility and inclusion**

[⭐ Star](https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python/stargazers) • [🍴 Fork](https://github.com/Sally4D/Realtime-Subtitles-Generator-using-Python/fork) • [📞 Support](https://oscurprofundo.gumroad.com/l/dmkbes)

</div>
