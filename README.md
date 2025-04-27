# CutCaption - Video Cutting Automation Tool

CutCaption is a Python-based desktop application that automates the process of cutting video segments based on subtitle keyword searches. The tool searches for specific words in subtitle files (.srt) and extracts the corresponding video segments, making it ideal for content creators and video editors.

## Features

- 🎯 Search for specific keywords in subtitle files
- ✂️ Automatically cut video segments based on keyword occurrences
- 🎬 Process multiple video files in batch
- 📁 Custom input and output folder selection
- 🔧 Adjustable video bitrate settings
- 🎨 User-friendly graphical interface
- 🔄 Real-time processing status updates
- 🛑 Ability to stop processing at any time
- 🎭 Smart filename sanitization (handles Turkish characters)
- ⚡ Efficient video processing using FFmpeg

## Requirements

- Python 3.x
- FFmpeg installed and accessible from system PATH
- Required Python packages:
  - pysrt
  - tkinter (usually comes with Python)

## Installation

1. Make sure you have Python 3.x installed
2. Install FFmpeg on your system
3. Install required Python packages:
```bash
pip install pysrt
```

## Usage

1. Run the application:
```bash
python cutcaption.py
```

2. In the application interface:
   - **VIDEO**: Select the folder containing your video files and corresponding .srt files
   - **OUTPUT**: Choose the destination folder for cut video segments
   - **KELİME**: Enter the keyword to search for in subtitles
   - **Bitrate**: Specify the desired output video bitrate in kbps

3. Click "START" to begin processing
   - Monitor progress in real-time through the interface
   - Use "STOP" button if you need to interrupt the process

## File Naming Convention

Output files follow this format:
```
original_filename_index_starttime_endtime_bitratevalue_mbps.mp4
```

Example: `video_0_00-05-30_00-05-35_2mbps.mp4`

## Technical Details

- Video segments include 1-second padding before and after the keyword occurrence
- Supports both Turkish and English characters in filenames
- Video encoding uses H.264 codec with AAC audio
- Audio bitrate is fixed at 128k
- Automatically handles special characters in filenames
- Preserves video quality while optimizing file size

## Version History

The tool has evolved through multiple versions, with key improvements including:
- v8.2: Real-time terminal output display in GUI
- v8.1: Improved filename format with bitrate information
- v8.0: Enhanced user interface
- v7.x: Added GUI and various quality-of-life improvements
- v6.x: Improved file handling and Turkish character support
- v5.0: Enhanced filename sanitization
- v4.0: Added timecode to filenames
- v3.0: Implemented custom output folder support
- v2.0: Initial subtitle parsing implementation

## Error Handling

The application includes robust error handling for common issues:
- Missing subtitle files
- Invalid video files
- FFmpeg processing errors
- Invalid bitrate values
- File access permissions

## Contributing

Feel free to fork this repository and submit pull requests for any improvements you'd like to add.

## License

[Add your preferred license here]
