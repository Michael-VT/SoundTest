#!/usr/bin/env python3
"""
Sound Generator - Generate and play audio signals from text descriptions.

Supports:
- Single frequencies: 850;1000;50
- Frequency ramps: 1200-850;1200;40-10
- Chords (multiple frequencies): 1200,850;1000;20,30

Cross-platform playback:
- macOS: afplay
- Linux: aplay (ALSA) or paplay (PulseAudio)
- Windows: PowerShell Media.SoundPlayer
- Termux: termux-media-player
"""

import argparse
import math
import platform
import subprocess
import sys
from pathlib import Path
from array import array
import wave
import curses
import threading
import time

# Constants
FS = 44100  # Sample rate
MAX_AMP = 32767  # Maximum amplitude for 16-bit PCM
DEFAULT_INPUT = Path("sound.txt")
DEFAULT_OUTPUT = Path("output/sound.wav")


def parse_token(token: str):
    """Parse a token into single value, ramp, or multi-value spec."""
    token = token.strip()
    if "-" in token:
        # Ramp: start-end
        a, b = token.split("-", 1)
        return ("ramp", float(a), float(b))
    if "," in token:
        # Multiple values: val1,val2,...
        return ("multi", [float(x.strip()) for x in token.split(",") if x.strip()])
    # Single value
    return ("single", float(token))


def parse_line(line: str):
    """Parse a line from the input file into (freq_spec, duration_ms, amp_spec)."""
    parts = [p.strip() for p in line.split(";") if p.strip()]
    if len(parts) != 3:
        return None
    f = parse_token(parts[0])
    dur = float(parts[1])
    amp = parse_token(parts[2])
    return f, dur, amp


def value_at(spec, u: float) -> float:
    """Get value from a spec at normalized position u (0.0 to 1.0)."""
    kind = spec[0]
    if kind == "single":
        return spec[1]
    if kind == "ramp":
        return spec[1] + (spec[2] - spec[1]) * u
    raise ValueError(f"Unexpected spec kind: {kind}")


def segments_from_spec(spec):
    """Generate PCM samples from a (freq_spec, duration_ms, amp_spec) tuple."""
    fspec, dur_ms, aspec = spec
    n = max(1, int(round(FS * dur_ms / 1000.0)))
    
    out = [0.0] * n

    # Handle chords (multiple frequencies)
    if fspec[0] == "multi" and aspec[0] == "multi":
        for fk, ak in zip(fspec[1], aspec[1]):
            for i in range(n):
                t = i / FS
                out[i] += math.sin(2 * math.pi * fk * t) * (ak / 100.0)
        return out

    # Handle single frequency and ramps
    for i in range(n):
        u = i / (n - 1) if n > 1 else 0.0
        freq = value_at(fspec, u)
        amp = value_at(aspec, u) / 100.0
        t = i / FS
        out[i] = math.sin(2 * math.pi * freq * t) * amp

    return out


def generate_from_file(input_path: Path, output_path: Path) -> int:
    """Generate audio from input file and write to output WAV file.
    
    Returns:
        Number of signal lines processed.
    """
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    samples = []
    line_count = 0

    for raw in input_path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        spec = parse_line(raw)
        if spec is None:
            print(f"Warning: Skipping invalid line: {raw}", file=sys.stderr)
            continue
        samples.extend(segments_from_spec(spec))
        line_count += 1

    if line_count == 0:
        print("Error: No valid signal lines found in input file", file=sys.stderr)
        sys.exit(1)

    # Convert to 16-bit PCM
    pcm = array("h", [
        max(-MAX_AMP, min(MAX_AMP, int(round(s * MAX_AMP))))
        for s in samples
    ])

    # Write WAV file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FS)
        w.writeframes(pcm.tobytes())

    return line_count


def generate_from_line(line: str, output_path: Path) -> None:
    """Generate audio from a single signal line.
    
    Args:
        line: Signal line like "850;1000;50"
        output_path: Where to write the WAV file
    """
    spec = parse_line(line)
    if spec is None:
        raise ValueError(f"Invalid signal format: {line}")

    samples = segments_from_spec(spec)
    pcm = array("h", [
        max(-MAX_AMP, min(MAX_AMP, int(round(s * MAX_AMP))))
        for s in samples
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FS)
        w.writeframes(pcm.tobytes())


def generate_from_string(signal_string: str, output_path: Path) -> None:
    """Generate audio from a single signal string.
    
    Args:
        signal_string: Format like "850;1000;50"
        output_path: Where to write the WAV file
    """
    spec = parse_line(signal_string)
    if spec is None:
        print(f"Error: Invalid signal format: {signal_string}", file=sys.stderr)
        print("Expected format: frequency;duration_ms;level_percent", file=sys.stderr)
        sys.exit(1)

    samples = segments_from_spec(spec)
    pcm = array("h", [
        max(-MAX_AMP, min(MAX_AMP, int(round(s * MAX_AMP))))
        for s in samples
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FS)
        w.writeframes(pcm.tobytes())

    print(f"Generated: {output_path}")


def get_play_command():
    """Get the platform-specific audio play command.
    
    Returns:
        List of command arguments for subprocess.
    """
    system = platform.system()
    
    if system == "Darwin":
        # macOS
        return ["afplay"]
    elif system == "Linux":
        # Try paplay (PulseAudio) first, then aplay (ALSA)
        try:
            subprocess.run(["which", "paplay"], capture_output=True, check=True)
            return ["paplay"]
        except subprocess.CalledProcessError:
            pass
        try:
            subprocess.run(["which", "aplay"], capture_output=True, check=True)
            return ["aplay"]
        except subprocess.CalledProcessError:
            pass
        print("Error: No audio player found. Install paplay or aplay.", file=sys.stderr)
        sys.exit(1)
    elif system == "Windows":
        # Windows - use PowerShell
        return None  # Special handling
    else:
        # Assume Termux or other Unix-like
        try:
            subprocess.run(["which", "termux-media-player"], capture_output=True, check=True)
            return ["termux-media-player", "play"]
        except subprocess.CalledProcessError:
            pass
        print(f"Error: Unsupported platform: {system}", file=sys.stderr)
        sys.exit(1)


def play_audio(audio_path: Path) -> None:
    """Play audio file using platform-specific player.
    
    Args:
        audio_path: Path to the WAV file to play
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows: Use PowerShell with Media.SoundPlayer
        ps_command = f'(New-Object Media.SoundPlayer "{audio_path.absolute()}").PlaySync()'
        try:
            subprocess.run(["powershell", "-c", ps_command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Unix-like systems (macOS, Linux, Termux)
        cmd = get_play_command()
        full_cmd = cmd + [str(audio_path)]
        try:
            subprocess.run(full_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: Audio player not found: {cmd[0]}", file=sys.stderr)
            sys.exit(1)


class InteractiveMode:
    """Interactive TUI mode for sound generator."""
    
    def __init__(self, input_path: Path, output_path: Path):
        """Initialize interactive mode.
        
        Args:
            input_path: Path to input file with signal descriptions
            output_path: Path for temporary WAV file generation
        """
        self.input_path = input_path
        self.output_path = output_path
        self.lines = []  # List of valid signal lines
        self.current_line = 0  # Index of current line
        self.repeat_mode = None  # None, 'once', 'infinite'
        self.playing = False
        self.play_thread = None
        self.stop_requested = False
        
        # Load lines from file
        self.load_lines()
        
        if not self.lines:
            print(f"Error: No valid signal lines found in {input_path}", file=sys.stderr)
            sys.exit(1)
    
    def load_lines(self):
        """Load valid signal lines from input file."""
        if not self.input_path.exists():
            print(f"Error: Input file not found: {self.input_path}", file=sys.stderr)
            sys.exit(1)
        
        for raw in self.input_path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            spec = parse_line(raw)
            if spec is not None:
                self.lines.append(raw)
    
    def format_signal_info(self, line: str) -> str:
        """Format signal line for display.
        
        Args:
            line: Raw signal line
            
        Returns:
            Formatted description string
        """
        spec = parse_line(line)
        if spec is None:
            return line
        
        fspec, dur_ms, aspec = spec
        
        # Format frequency info
        if fspec[0] == "single":
            freq_str = f"{int(fspec[1])} Hz"
        elif fspec[0] == "ramp":
            freq_str = f"{int(fspec[1])}→{int(fspec[2])} Hz"
        elif fspec[0] == "multi":
            freqs = ", ".join(str(int(f)) for f in fspec[1])
            freq_str = f"[{freqs}] Hz"
        else:
            freq_str = "Unknown"
        
        # Format amplitude info
        if aspec[0] == "single":
            amp_str = f"{int(aspec[1])}%"
        elif aspec[0] == "ramp":
            amp_str = f"{int(aspec[1])}→{int(aspec[2])}%"
        elif aspec[0] == "multi":
            amps = ", ".join(str(int(a)) for a in aspec[1])
            amp_str = f"[{amps}%]"
        else:
            amp_str = "Unknown"
        
        return f"{freq_str}, {amp_str}, {int(dur_ms)} ms"
    
    def play_current(self):
        """Play current signal line."""
        if not self.lines:
            return
        
        line = self.lines[self.current_line]
        
        def play_worker():
            try:
                self.playing = True
                generate_from_line(line, self.output_path)
                play_audio(self.output_path)
                
                # Handle repeat modes
                while self.repeat_mode == 'infinite' and not self.stop_requested:
                    if self.stop_requested:
                        break
                    play_audio(self.output_path)
                
                if self.repeat_mode == 'once' and not self.stop_requested:
                    if not self.stop_requested:
                        play_audio(self.output_path)
                        self.repeat_mode = None
                
            finally:
                self.playing = False
                self.stop_requested = False
        
        # Stop any existing playback
        if self.playing:
            self.stop_playback()
        
        # Start new playback in thread
        self.play_thread = threading.Thread(target=play_worker, daemon=True)
        self.play_thread.start()
    
    def stop_playback(self):
        """Stop current playback."""
        self.stop_requested = True
        self.repeat_mode = None
        # Note: We can't actually stop subprocess playback on most platforms
        # This just prevents future repeats
    
    def next_line(self):
        """Move to next line."""
        if self.current_line < len(self.lines) - 1:
            self.current_line += 1
            self.repeat_mode = None
    
    def prev_line(self):
        """Move to previous line."""
        if self.current_line > 0:
            self.current_line -= 1
            self.repeat_mode = None
    
    def toggle_repeat_once(self):
        """Toggle repeat-once mode."""
        if self.repeat_mode == 'once':
            self.repeat_mode = None
        else:
            self.repeat_mode = 'once'
    
    def toggle_repeat_infinite(self):
        """Toggle infinite repeat mode."""
        if self.repeat_mode == 'infinite':
            self.repeat_mode = None
        else:
            self.repeat_mode = 'infinite'
    
    def draw_ui(self, stdscr):
        """Draw the TUI.
        
        Args:
            stdscr: Curses window
        """
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "Sound Generator - Interactive Mode"
        stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Current line info
        if self.lines:
            line_num = self.current_line + 1
            total_lines = len(self.lines)
            current_line_text = self.lines[self.current_line]
            signal_info = self.format_signal_info(current_line_text)
            
            line_header = f"Line {line_num}/{total_lines}: {current_line_text}"
            stdscr.addstr(2, 2, line_header)
            
            info_text = f"→ {signal_info}"
            stdscr.addstr(3, 4, info_text, curses.A_DIM)
        
        # Status
        status_parts = []
        if self.playing:
            status_parts.append("PLAYING")
        if self.repeat_mode == 'once':
            status_parts.append("REPEAT ONCE")
        elif self.repeat_mode == 'infinite':
            status_parts.append("REPEAT ∞")
        
        if status_parts:
            status = " | ".join(status_parts)
            stdscr.addstr(5, 2, f"Status: {status}", curses.A_BOLD)
        else:
            stdscr.addstr(5, 2, "Status: Stopped")
        
        # Help
        help_y = height - 3
        help_text = "[n]ext [p]rev [r]epeat [R]epeat ∞ [s]top [q]uit"
        stdscr.addstr(help_y, (width - len(help_text)) // 2, help_text, curses.A_REVERSE)
        
        # Signal list (show window around current line)
        list_start_y = 7
        list_height = height - list_start_y - 4
        
        window_size = list_height
        start_idx = max(0, self.current_line - window_size // 2)
        end_idx = min(len(self.lines), start_idx + window_size)
        
        # Adjust start if we're near the end
        if end_idx - start_idx < window_size:
            start_idx = max(0, end_idx - window_size)
        
        for i in range(start_idx, end_idx):
            y = list_start_y + (i - start_idx)
            line_text = f"{i + 1:3d}. {self.lines[i]}"
            
            # Truncate if too long
            if len(line_text) > width - 4:
                line_text = line_text[:width - 7] + "..."
            
            if i == self.current_line:
                stdscr.addstr(y, 2, line_text, curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, line_text)
        
        stdscr.refresh()
    
    def run(self):
        """Main curses loop."""
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(True)
            curses.curs_set(0)  # Hide cursor
            
            while True:
                self.draw_ui(stdscr)
                
                # Timeout for refresh (0.1s)
                stdscr.timeout(100)
                key = stdscr.getch()
                
                if key == -1:
                    # Timeout - just refresh
                    continue
                elif key == ord('q') or key == ord('Q'):
                    # Quit
                    break
                elif key == ord('n') or key == ord('N') or key == curses.KEY_RIGHT or key == ord(' '):
                    # Next line
                    self.next_line()
                    self.play_current()
                elif key == ord('p') or key == ord('P') or key == curses.KEY_LEFT:
                    # Previous line
                    self.prev_line()
                    self.play_current()
                elif key == ord('r'):
                    # Repeat once
                    self.toggle_repeat_once()
                    self.play_current()
                elif key == ord('R'):
                    # Repeat infinite
                    self.toggle_repeat_infinite()
                    self.play_current()
                elif key == ord('s') or key == ord('S'):
                    # Stop
                    self.stop_playback()
        
        finally:
            # Cleanup
            self.stop_playback()
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.curs_set(1)
            curses.endwin()


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Generate and play audio signals from text descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from file and play
  %(prog)s -i sound.txt

  # Generate from file without playing
  %(prog)s -i sound.txt --no-play

  # Generate from string
  %(prog)s -s "850;1000;50" -o beep.wav

  # Interactive mode
  %(prog)s -i sound.txt --interactive

Signal format (one per line in file):
  frequency;duration_ms;level_percent

  Examples:
    850;1000;50           # 850 Hz, 1000 ms, 50%% volume
    1200-850;1200;40-10   # Ramp 1200→850 Hz, 1200 ms, 40%%→10%% volume
    1200,850;1000;20,30   # Chord: 1200 Hz @ 20%% + 850 Hz @ 30%%
        """
    )

    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input file with signal descriptions (default: sound.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output WAV file path (default: output/sound.wav)"
    )
    parser.add_argument(
        "-s", "--signal",
        help="Generate from single signal string (overrides -i)"
    )
    parser.add_argument(
        "-n", "--no-play",
        action="store_true",
        help="Generate audio without playing it"
    )
    parser.add_argument(
        "-I", "--interactive",
        action="store_true",
        help="Interactive mode with TUI (requires file input)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Handle interactive mode
    if args.interactive:
        if args.signal:
            print("Error: --interactive cannot be used with --signal", file=sys.stderr)
            sys.exit(1)
        
        try:
            interactive = InteractiveMode(args.input, args.output)
            interactive.run()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            sys.exit(0)
        except Exception as e:
            curses.endwin()
            print(f"Error in interactive mode: {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # Generate audio
    if args.signal:
        generate_from_string(args.signal, args.output)
    else:
        line_count = generate_from_file(args.input, args.output)
        if args.verbose:
            print(f"Processed {line_count} signal lines")

    # Play audio unless suppressed
    if not args.no_play:
        print(f"Playing: {args.output}")
        play_audio(args.output)


if __name__ == "__main__":
    main()
