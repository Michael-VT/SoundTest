# Sound Generator

Cross-platform sound signal generator with interactive TUI control.

## Features

- 🎵 Generate tones, frequency sweeps, and chords
- 🎹 Interactive TUI mode with keyboard control  
- 📊 Cross-platform playback (macOS, Linux, Windows, Termux)
- 🌍 Simple text-based signal format
- 📝 No external dependencies required

## Requirements

### Required
- Python 3.8 or higher

### Optional  
- NumPy (for future visualization features)
- SciPy (for advanced processing)

## Installation

### macOS / Linux
```bash
cd SoundTest
# No dependencies required for basic functionality
pip3 install numpy scipy  # Optional
```

### Windows
```bash
# Python 3.8+ required
# No additional dependencies needed
```

### Termux (Android)
```bash
pkg install python
pkg install numpy  # Optional
```

## Usage

### Batch Mode

Generate and play from file:
```bash
python3 generate_sound.py -i sound.txt
```

Generate without playing:
```bash
python3 generate_sound.py -i sound.txt --no-play
```

Generate from command-line string:
```bash
python3 generate_sound.py -s "850;1000;50" -o beep.wav
```

Custom output file:
```bash
python3 generate_sound.py -i examples/simple.txt -o output/my_sounds.wav
```

### Interactive Mode

#### Quick Start

Launch interactive TUI:
```bash
python3 generate_sound.py -i sound.txt --interactive
```

**Expected:** Terminal clears and shows interface with signal list.

#### Keyboard Shortcuts

- `n` or `→` or `Space` - Next line + play
- `p` or `←` - Previous line + play
- `r` - Repeat current line once
- `R` - Repeat infinitely
- `s` - Stop playback
- `q` - Quit

#### Interactive Mode Guide

**Terminal Requirements:**
- Minimum size: 80x24 characters
- Fullscreen mode recommended

**What You'll See:**
- Header: "Sound Generator - Interactive Mode"
- Signal list with current line highlighted (inverted colors)
- Signal info: frequency, duration, volume level
- Status: PLAYING, REPEAT ONCE, REPEAT ∞, or Stopped
- Help line at bottom: `[n]ext [p]rev [r]epeat [R]epeat ∞ [s]top [q]uit`

#### Step-by-Step Testing

**TEST 1: Navigation (without sound)**

1. Press `n` several times (3-5 times)
2. Observe: Current line moves down
3. Press `p` several times
4. Observe: Current line moves up

**Expected:** Highlighted line moves through list, no audio plays.

**TEST 2: Playback with Navigation**

1. Press `Space` (spacebar)
2. Listen: Current signal should play
3. Wait for completion
4. Press `Space` again for next signal
5. Repeat for all 5 signals

**Expected:** Each Space press plays a new signal, status shows "PLAYING".

**TEST 3: Repeat Once (r)**

1. Press `p` to return to line 1
2. Press `r`
3. Observe: Status shows "REPEAT ONCE"
4. Listen: Signal plays 2 times consecutively

**Expected:** Current signal plays twice, then "REPEAT ONCE" status disappears.

**TEST 4: Infinite Repeat (R)**

1. Press `R` (capital R)
2. Observe: Status shows "REPEAT ∞"
3. Listen: Signal plays continuously
4. Wait for 2-3 cycles
5. Press `s` to stop

**Expected:** Signal repeats infinitely until `s` is pressed.

**TEST 5: Combined Navigation**

1. Press `→` (right arrow) - next + play
2. Wait for completion
3. Press `←` (left arrow) - previous + play
4. Wait for completion
5. Press `n` - next line
6. Press `p` - previous line

**Expected:** All three methods (arrows, n/p, Space) work for navigation.

**TEST 6: Stop Playback**

1. Press `n` to start playback
2. Immediately press `s`
3. Observe: "PLAYING" status disappears

**Expected:** Playback stops (current cycle completes).

**TEST 7: Different Files**

```bash
# Exit current mode (q)
# Test with another file
python3 generate_sound.py -i examples/simple.txt --interactive
```

1. Try navigation through simple examples
2. Test different signals

**TEST 8: Exit and Verify**

1. Press `q` to exit
2. Observe: Terminal returns to normal
3. Check: output/sound.wav updated

**Expected:** Clean exit without errors, terminal works normally, last signal saved.

#### Quick Verification (5 minutes)

```bash
# Launch
python3 generate_sound.py -i sound.txt --interactive

# Minimal test:
# 1. Press Space (sound should play)
# 2. Press n (next + sound)
# 3. Press R (infinite repeat)
# 4. Wait 2 repetitions
# 5. Press s (stop)
# 6. Press q (quit)
```

**If all 6 steps work - interactive mode is functioning correctly!**

#### Troubleshooting Interactive Mode

**Problem:** "curses error" or distorted display
**Solution:** Increase terminal size to minimum 80x24 characters

**Problem:** Keys not responding
**Solution:** Ensure terminal is in focus, press Enter

**Problem:** Audio not playing
**Solution:** Check system volume, test batch mode first

## Signal Format

Each line: `frequency;duration_ms;level_percent`

### Examples

#### Single frequency
```
850;1000;50
```
850 Hz tone, 1000 ms duration, 50% volume

#### Frequency sweep
```
1200-850;1200;40-10
```
Ramp from 1200 Hz down to 850 Hz over 1200 ms, volume 40% to 10%

#### Chord
```
1200,850;1000;20,30
```
Two frequencies: 1200 Hz @ 20% + 850 Hz @ 30%, 1000 ms

## Cross-Platform Playback

### macOS
- Uses `afplay` (built-in)
- No installation required

### Linux
- Tries `paplay` (PulseAudio), then `aplay` (ALSA)
- Install: `sudo apt-get install pulseaudio-utils` or `alsa-utils`

### Windows
- Uses PowerShell `Media.SoundPlayer`
- Built into Windows

### Termux
- Uses `termux-media-player`
- Install: `pkg install termux-api`

## Project Structure

```
soundtest/
├── generate_sound.py      # Main script
├── README.md              # Documentation
├── LICENSE                # MIT License
├── sound.txt              # Example signals
├── output/                # Generated WAV files
└── examples/              # Additional examples
    ├── simple.txt         # Simple examples
    ├── complex.txt        # Complex examples
    └── test.txt           # Test signals
```

## Examples

```bash
# Simple tones
python3 generate_sound.py -i examples/simple.txt

# Complex sweeps and chords
python3 generate_sound.py -i examples/complex.txt --interactive

# Test signals
python3 generate_sound.py -i examples/test.txt
```

## Troubleshooting

### "No audio player found"
- Linux: Install `paplay` or `aplay`
- Termux: Install `termux-api`

### Curses display issues
- Windows: Use PowerShell or Windows Terminal
- Terminal must support ANSI escape codes

### Audio not playing
- Check system volume
- Verify audio player installation
- Try `--no-play` and check output file

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Areas for improvement:
- Signal visualization
- Additional audio formats
- Enhanced TUI features
- More signal types
