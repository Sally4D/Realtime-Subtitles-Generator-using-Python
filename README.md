# LiveScript: Real-time Live Captioning & Translation Software v2.0.1

A powerful real-time audio transcription application that provides live captions for your system's audio output with **built-in translation capabilities**. Perfect for accessibility, language learning, international meetings, or any situation where you need visual representation and translation of spoken content.

## 🆕 What's New in Version 2.0.1
*Released: August 27, 2025*

### ✨ Major New Features
- **🌍 Real-Time Translation**: Live translation of captions into 50+ languages
- **🔄 Dual Translation Engines**: Choose between ArgosTranslate (offline) and MarianMT (offline)
- **⚡ Instant Translation**: Translate both final text and partial text in real-time
- **📱 Smart Language Detection**: Automatic model management for translation pairs

### 🔧 Enhanced Features
- **Improved Performance**: Optimized audio processing for better real-time performance
- **Enhanced UI**: Refined user interface with translation controls and status indicators
- **Better Model Management**: Automatic downloading for both speech recognition and translation models
- **Stability Improvements**: Fixed memory leaks and improved application stability
- **Updated Dependencies**: Added translation libraries and upgraded existing dependencies

### 🛠️ Technical Improvements
- Optimized memory usage during long transcription and translation sessions
- Enhanced error handling for translation model loading
- Improved startup time with lazy model loading
- Better handling of system audio configuration changes
- Streamlined translation pipeline for minimal latency

## ✨ Core Features

### 🎤 **Real-Time Transcription**
- Live speech-to-text using Vosk offline speech recognition
- Audio loopback capture from system speakers
- Multi-threaded processing for smooth performance
- Configurable audio buffer sizes for optimal accuracy/speed balance

### 🌍 **Live Translation (NEW!)**
- **Real-time translation** of live captions as they appear
- **50+ target languages** supported for translation
- **Dual translation backends**:
  - **ArgosTranslate**: Completely offline, privacy-focused
  - **MarianMT**: High-quality Hugging Face models, also offline
- **Automatic model management** - download translation models on demand
- **Instant partial translation** - even incomplete sentences get translated live

### 🎯 **Multi-Language Speech Recognition**
- **50+ languages and dialects** supported for speech recognition including:
  - English (multiple variants), Chinese, Russian, French, German, Spanish
  - Portuguese, Arabic, Hindi, Japanese, Korean, Italian, Dutch
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
- Translation engine selection and target language configuration
- Searchable dropdown menus for easy navigation
- Settings persistence with JSON configuration
- First-run setup wizard with guided tour

### 🖥️ **User Experience**
- Modern CustomTkinter interface with translation controls
- Right-click context menu for quick access
- Tooltips and helpful descriptions for all settings
- Responsive, scrollable settings panel
- One-click model installation for both speech and translation

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.7 or higher
- **RAM**: Minimum 4GB (8GB recommended for translation features)
- **Storage**: 1GB - 10GB depending on language and translation models
- **Audio**: System audio output (speakers/headphones)
- **Internet**: Required for initial model downloads only

### Python Dependencies
```
customtkinter>=5.0.0
soundcard>=0.4.0
vosk>=0.3.45
numpy>=1.19.0
requests>=2.25.0
argostranslate>=1.9.0
transformers>=4.21.0
torch>=1.12.0
sentencepiece>=0.1.97
protobuf>=3.20.0
```

## 🚀 Installation

### Method 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python.git
cd Realtime-Subtitles-Generator-using-Python

# Install dependencies
pip install -r requirements.txt

# Run the application
python LivescriptV2.01.py
```

### Method 2: Direct Download
1. Download the latest release from [Releases](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/releases)
2. Extract the archive
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python LivescriptV2.01.py`

### Method 3: Package Installation
```bash
pip install livescript-captions
livescript
```

## 🎮 Usage

### First Run
1. **Launch the application** - The About window will appear with usage instructions
2. **Right-click** the caption overlay to access settings
3. **Select your spoken language** - The app will automatically download the required speech recognition model
4. **Enable translation** (optional) - Choose your target language and translation engine
5. **Customize appearance** to your preferences
6. **Start speaking or play audio** - Captions will appear in real-time, with live translation if enabled!

### Basic Controls
- **Move Window**: Left-click and drag the caption bar
- **Access Settings**: Right-click anywhere on the caption window
- **Quick Restart**: Use the restart option when changing languages or models

### Translation Quick Start
1. **Enable Translation**: Settings → Translation → Check "Enable Translation"
2. **Choose Engine**: Select ArgosTranslate (recommended) or MarianMT
3. **Select Target Language**: Choose from 50+ available languages
4. **Download Models**: App will automatically download required translation models
5. **Start Translating**: Speak or play audio - see live translated captions!

### Settings Overview

#### 🎨 **Caption Appearance**
- **Colors**: Subtitle and background colors with color picker
- **Typography**: Font family, size, and styling options
- **Layout**: Window dimensions, padding, and opacity controls
- **Positioning**: Draggable overlay with size customization

#### 🔊 **Audio & Language**
- **Spoken Language**: 50+ supported languages for speech recognition
- **Audio Processing**: Block size and delay threshold adjustments
- **Model Management**: Automatic installation and status monitoring

#### 🌍 **Translation (NEW!)**
- **Enable/Disable**: Toggle real-time translation
- **Translation Engine**: Choose between ArgosTranslate and MarianMT
- **Target Language**: Select from 50+ supported languages
- **Model Status**: View download progress and model availability

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
    "delay_threshold": 3.0,
    "translation_enabled": false,
    "translation_backend": "ArgosTranslate",
    "translation_target_language": "Spanish",
    "version": "2.0.1"
}
```

### Model Storage
- **Speech Recognition Models**: Downloaded to application directory (30MB - 5GB)
- **Translation Models**: 
  - ArgosTranslate: ~50-200MB per language pair
  - MarianMT: ~300MB - 1GB per language pair
- Models are reusable and only need to be downloaded once
- All models work completely offline after download

## 🌐 Translation Features

### Supported Translation Backends

#### 🔄 **ArgosTranslate (Recommended)**
- **Completely offline** - No internet required after setup
- **Privacy-focused** - All processing happens locally
- **50+ language pairs** supported
- **Smaller model sizes** (~50-200MB per language pair)
- **Good translation quality** for most use cases

#### 🎯 **MarianMT (Advanced)**
- **High-quality translations** using Hugging Face models
- **Also completely offline**
- **Professional-grade accuracy** for supported language pairs
- **Larger model sizes** (~300MB - 1GB per language pair)
- **Best for professional/academic use**

### Translation Language Support
Popular language pairs include:
- **English** ↔ Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi
- **Spanish** ↔ English, French, Italian, Portuguese
- **French** ↔ English, German, Spanish, Italian
- **German** ↔ English, French, Spanish, Italian
- **And many more combinations!**

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

#### Translation not working
- **Solution**: 
  - Check that translation is enabled in Settings
  - Verify target language is selected
  - Wait for translation model download to complete
  - Try switching translation backends (ArgosTranslate ↔ MarianMT)

#### Poor translation quality
- **Solution**:
  - Try MarianMT backend for higher quality (if language pair supported)
  - Ensure clear audio input for better source transcription
  - Check that source language matches the speech recognition setting

#### "Translation model download failed"
- **Solution**:
  - Check internet connection
  - Try different language pair
  - Switch to alternative translation backend
  - Manually install models if needed

#### Application slow with translation
- **Solution**:
  - Use ArgosTranslate for better performance
  - Increase block size for less frequent processing
  - Close other resource-intensive applications
  - Consider using smaller translation models

### Performance Optimization
- **For speed**: Use ArgosTranslate, smaller models, lower block sizes
- **For accuracy**: Use MarianMT, larger models, higher block sizes  
- **For battery life**: Disable translation when not needed, use smaller models

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Bug Reports**: Report issues via [GitHub Issues](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/issues)
- 💡 **Feature Requests**: Suggest new features or improvements
- 🌍 **Language Support**: Help test and improve language and translation models
- 📖 **Documentation**: Improve guides, README, or code comments
- 🔧 **Code**: Submit pull requests for bug fixes or new features
- 🌐 **Translation Testing**: Help test translation accuracy for different language pairs

### Development Setup
```bash
git clone https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python.git
cd Realtime-Subtitles-Generator-using-Python
pip install -r requirements.txt
# Make your changes
python LivescriptV2.01.py  # Test your changes
```

### Pull Request Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Test translation features with multiple language pairs
5. Commit with descriptive messages
6. Push to your fork and submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Vosk](https://alphacephei.com/vosk/)** - Offline speech recognition toolkit
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern GUI framework
- **[SoundCard](https://github.com/bastibe/SoundCard)** - Audio capture library
- **[ArgosTranslate](https://github.com/argosopentech/argos-translate)** - Open-source offline translation
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** - MarianMT translation models
- **Community Contributors** - Thanks to everyone who has contributed!

## 📞 Support

- 🌟 **Star this repo** if you find it helpful!
- 🐛 **Report bugs** via [GitHub Issues](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/issues)
- 💬 **Discussions** for questions and feature requests
- 📧 **Email**: oscurprof@gmail.com
- 🔗 **LinkedIn**: [oscurprof](https://www.linkedin.com/in/oscurprof/)

## 🗺️ Roadmap

### Planned Features
- [ ] **Cloud Translation APIs** - Integration with Google Translate, DeepL, etc.
- [ ] **Multi-Speaker Recognition** - Distinguish between different speakers
- [ ] **Export Functionality** - Save transcriptions and translations to text files
- [ ] **Hotkey Support** - Keyboard shortcuts for common actions
- [ ] **Advanced Translation Options** - Context-aware translation, custom dictionaries
- [ ] **Translation History** - Save and review past translations
- [ ] **Batch Translation** - Translate saved transcription files

### Translation Roadmap
- [ ] **More Language Pairs** - Expand ArgosTranslate and MarianMT support
- [ ] **Custom Translation Models** - Support for user-trained models
- [ ] **Translation Quality Indicators** - Confidence scores for translations
- [ ] **Bidirectional Translation** - Translate both directions simultaneously

### Version History
- **v2.0.1** - Added real-time translation with ArgosTranslate and MarianMT support
- **v1.01** - Initial release with core transcription functionality
- **v1.00** - Beta testing and development

---

<div align="center">

**Made with ❤️ for accessibility and inclusion worldwide**

[⭐ Star](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/stargazers) • [🍴 Fork](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/fork) • [📋 Issues](https://github.com/oscurprof/Realtime-Subtitles-Generator-using-Python/issues)

</div>
