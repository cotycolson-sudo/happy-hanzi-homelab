# Jellyfin Trilingual Subtitle Automation

Automatically generate trilingual subtitles (Chinese, Pinyin, English) for your Jellyfin media library. Perfect for language learners watching Chinese content!

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Automatic Processing**: Watches your Jellyfin media folders and automatically generates trilingual subtitles when Chinese and English subtitle pairs are detected
- **Timestamp Matching**: Intelligently matches subtitles by timestamp overlap, not line number (handles different subtitle formats)
- **Pinyin Generation**: Automatically converts Chinese characters to pinyin with tone marks
- **Jellyfin Compatible**: Outputs standard SRT files that work seamlessly with Jellyfin
- **CLI and Watch Mode**: Run once or continuously monitor directories for new content

## 📋 Prerequisites

- Python 3.7 or higher
- Jellyfin media server
- Chinese and English subtitle files for your media

## 🚀 Installation

### Method 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/cotycolson-sudo/jellyfin-trilingual-subtitles.git
cd jellyfin-trilingual-subtitles

# Install dependencies
pip install -r requirements.txt
```

### Method 2: System-wide Installation

```bash
# Install directly from GitHub
pip install git+https://github.com/cotycolson-sudo/jellyfin-trilingual-subtitles.git
```

## 💡 Usage

### Basic Usage

Process a single movie folder:

```bash
python jellyfin_trilingual_subtitle_automation.py "/data/Movies/Police Story 3 (1992)"
```

### Watch Mode (Recommended for Automation)

Continuously monitor a directory for new subtitle pairs:

```bash
python jellyfin_trilingual_subtitle_automation.py "/data/Movies" --watch
```

With custom check interval:

```bash
python jellyfin_trilingual_subtitle_automation.py "/data/Movies" --watch --interval 30
```

### Command-Line Options

```
usage: jellyfin_trilingual_subtitle_automation.py [-h] [--watch] [--interval INTERVAL] [--verbose] directory

positional arguments:
  directory            Directory containing subtitle files

optional arguments:
  -h, --help           show this help message and exit
  --watch              Watch directory for new subtitle pairs
  --interval INTERVAL  Check interval in seconds (default: 60)
  --verbose            Enable verbose logging
```

## 📁 File Naming Convention

The script automatically detects subtitle pairs based on standard naming conventions:

**Chinese subtitles:**
- `moviename.chs.srt`
- `moviename.chi.srt`
- `moviename.zh.srt`

**English subtitles:**
- `moviename.eng.srt`
- `moviename.en.srt`

**Output:**
- `moviename.srt` (trilingual)

## 🎬 Example Output

Input files:
```
Police_Story_3_chs.srt
Police_Story_3_eng.srt
```

Output file (`Police_Story_3.srt`):
```srt
1
00:01:06,030 --> 00:01:07,790
现在毒贩运毒的手法
xiàn zài dú fàn yùn dú de shǒu fǎ
Nowadays, drug traffickers use every conceivable method

2
00:01:08,060 --> 00:01:09,430
可以说是无孔不入
kě yǐ shuō shì wú kǒng bù rù
They put the drugs into condoms
```

## 🔧 Integration with Jellyfin

### Option 1: Manual Upload

1. Place your Chinese and English subtitle files in the movie folder
2. Run the script to generate the trilingual subtitle
3. Jellyfin will automatically detect the new subtitle file
4. Refresh your library metadata

### Option 2: Automated with Bazarr

1. Configure Bazarr to download Chinese (Simplified) and English subtitles
2. Set up the automation script to watch your media directories
3. New trilingual subtitles will be created automatically as Bazarr downloads subtitle pairs

### Recommended Bazarr Settings:

**Languages Profile:**
- Language 1: Chinese (Simplified)
- Language 2: English

**Subtitle Providers:**
- OpenSubtitles
- Subscene
- Shooter (for Chinese subtitles)

## ⚙️ Running as a Service (Linux)

Create a systemd service for continuous monitoring:

```bash
sudo nano /etc/systemd/system/jellyfin-trilingual-subs.service
```

Add the following content:

```ini
[Unit]
Description=Jellyfin Trilingual Subtitle Automation
After=network.target

[Service]
Type=simple
User=jellyfin
WorkingDirectory=/home/jellyfin
ExecStart=/usr/bin/python3 /path/to/jellyfin_trilingual_subtitle_automation.py /data/Movies --watch --interval 60
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable jellyfin-trilingual-subs
sudo systemctl start jellyfin-trilingual-subs
```

Check status:

```bash
sudo systemctl status jellyfin-trilingual-subs
```

## 🐛 Troubleshooting

### Subtitle files not detected

**Problem:** Script doesn't find your subtitle files

**Solution:** 
- Ensure subtitle files follow the naming convention (`.chs.srt` and `.eng.srt`)
- Check file permissions
- Use `--verbose` flag to see detailed logging

### Subtitles don't appear in Jellyfin

**Problem:** Generated subtitle file doesn't show up in Jellyfin

**Solution:**
- Refresh library metadata in Jellyfin
- Check that the output filename matches the video filename
- Verify Jellyfin can read the subtitle file (check permissions)
- Make sure the subtitle file is in the same directory as the video

### Pinyin looks incorrect

**Problem:** Some pinyin conversions are wrong

**Solution:**
- This is typically due to polyphonic characters in Chinese
- The `pypinyin` library uses context to determine pronunciation, but isn't perfect
- You can manually edit the output SRT file if needed

### Timestamps don't match

**Problem:** Subtitles appear at wrong times

**Solution:**
- Ensure your Chinese and English subtitle files are for the same video release
- Different video releases may have different timing
- Download subtitles that specifically match your video file's release group

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pypinyin](https://github.com/mozillazg/python-pinyin) for Chinese to pinyin conversion
- Inspired by the need for better language learning resources in media servers
- Thanks to the Jellyfin community for creating an amazing open-source media platform

## 📧 Contact

Project Link: [https://github.com/cotycolson-sudo/jellyfin-trilingual-subtitles](https://github.com/cotycolson-sudo/jellyfin-trilingual-subtitles)

---

**Made for language learners who love watching Chinese movies! 加油! (jiā yóu!)**
