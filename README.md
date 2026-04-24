# Sound Generator

Cross-platform sound signal generator with interactive TUI control.

Генератор звуковых сигналов с интерактивным управлением.

## Features / Возможности

- 🎵 Generate tones, frequency sweeps, and chords
- 🎹 Interactive TUI mode with keyboard control  
- 📊 Cross-platform playback (macOS, Linux, Windows, Termux)
- 🌍 Simple text-based signal format
- 📝 No external dependencies required

## Requirements / Требования

### Required / Обязательные
- Python 3.8 or higher

### Optional / Опциональные  
- NumPy (for future visualization features)
- SciPy (for advanced processing)

## Installation / Установка

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

## Usage / Использование

### Batch Mode / Пакетный режим

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

### Interactive Mode / Интерактивный режим

#### Quick Start / Быстрый запуск

Launch interactive TUI:
```bash
python3 generate_sound.py -i sound.txt --interactive
```

**Expected:** Terminal clears and shows interface with signal list.

**Ожидается:** Терминал очищается и показывает интерфейс со списком сигналов.

#### Keyboard Shortcuts / Горячие клавиши

- `n` or `→` or `Space` - Next line + play / Следующая строка + воспроизведение
- `p` or `←` - Previous line + play / Предыдущая строка + воспроизведение  
- `r` - Repeat current line once / Повторить текущий один раз
- `R` - Repeat infinitely / Повторять бесконечно
- `s` - Stop playback / Остановить воспроизведение
- `q` - Quit / Выход

#### Interactive Mode Guide / Руководство по интерактивному режиму

**Terminal Requirements / Требования к терминалу:**
- Minimum size: 80x24 characters / Минимум 80x24 символов
- Fullscreen mode recommended / Рекомендуется полноэкранный режим

**What You'll See / Что вы увидите:**
- Header: "Sound Generator - Interactive Mode"
- Signal list with current line highlighted (inverted colors)
- Signal info: frequency, duration, volume level
- Status: PLAYING, REPEAT ONCE, REPEAT ∞, or Stopped
- Help line at bottom: `[n]ext [p]rev [r]epeat [R]epeat ∞ [s]top [q]uit`

**Заголовок: "Sound Generator - Interactive Mode"
- Список сигналов с подсветкой текущей линии (инверсные цвета)
- Информация о сигнале: частота, длительность, уровень громкости
- Статус: PLAYING, REPEAT ONCE, REPEAT ∞ или Stopped
- Строка помощи внизу: `[n]ext [p]rev [r]epeat [R]epeat ∞ [s]top [q]uit`

#### Step-by-Step Testing / Пошаговое тестирование

**TEST 1: Navigation (without sound) / Навигация (без звука)**

1. Press `n` several times (3-5 times) / Нажмите `n` несколько раз
2. Observe: Current line moves down / Наблюдайте: текущая линия движется вниз
3. Press `p` several times / Нажмите `p` несколько раз
4. Observe: Current line moves up / Наблюдайте: текущая линия движется вверх

**Expected:** Highlighted line moves through list, no audio plays.

**Ожидается:** Подсвеченная линия движется по списку, звук не воспроизводится.

**TEST 2: Playback with Navigation / Воспроизведение с навигацией**

1. Press `Space` (spacebar) / Нажмите `Space` (пробел)
2. Listen: Current signal should play / Слушайте: должен воспроизвестись текущий сигнал
3. Wait for completion / Подождите окончания
4. Press `Space` again for next signal / Нажмите `Space` снова для следующего сигнала
5. Repeat for all 5 signals / Повторите для всех 5 сигналов

**Expected:** Each Space press plays a new signal, status shows "PLAYING".

**Ожидается:** При каждом нажатии Space воспроизводится новый сигнал, статус показывает "PLAYING".

**TEST 3: Repeat Once (r) / Повтор один раз (r)**

1. Press `p` to return to line 1 / Нажмите `p` чтобы вернуться к линии 1
2. Press `r` / Нажмите `r`
3. Observe: Status shows "REPEAT ONCE" / Наблюдайте: статус показывает "REPEAT ONCE"
4. Listen: Signal plays 2 times consecutively / Слушайте: сигнал воспроизводится 2 раза подряд

**Expected:** Current signal plays twice, then "REPEAT ONCE" status disappears.

**Ожидается:** Текущий сигнал воспроизводится дважды, затем статус "REPEAT ONCE" исчезает.

**TEST 4: Infinite Repeat (R) / Бесконечный повтор (R)**

1. Press `R` (capital R) / Нажмите `R` (большая R)
2. Observe: Status shows "REPEAT ∞" / Наблюдайте: статус показывает "REPEAT ∞"
3. Listen: Signal plays continuously / Слушайте: сигнал воспроизводится непрерывно
4. Wait for 2-3 cycles / Подождите 2-3 цикла повторения
5. Press `s` to stop / Нажмите `s` для остановки

**Expected:** Signal repeats infinitely until `s` is pressed.

**Ожидается:** Сигнал повторяется бесконечно, пока не нажата `s`.

**TEST 5: Combined Navigation / Комбинированная навигация**

1. Press `→` (right arrow) - next + play / Нажмите `→` (стрелка вправо)
2. Wait for completion / Подождите окончания
3. Press `←` (left arrow) - previous + play / Нажмите `←` (стрелка влево)
4. Wait for completion / Подождите окончания
5. Press `n` - next line / Нажмите `n` - следующая линия
6. Press `p` - previous line / Нажмите `p` - предыдущая линия

**Expected:** All three methods (arrows, n/p, Space) work for navigation.

**Ожидается:** Все три метода (стрелки, n/p, Space) работают для навигации.

**TEST 6: Stop Playback / Остановка воспроизведения**

1. Press `n` to start playback / Нажмите `n` для начала воспроизведения
2. Immediately press `s` / Сразу нажмите `s`
3. Observe: "PLAYING" status disappears / Наблюдайте: статус "PLAYING" исчезает

**Expected:** Playback stops (current cycle completes).

**Ожидается:** Воспроизведение прекращается (текущий цикл завершается).

**TEST 7: Different Files / Разные файлы**

```bash
# Exit current mode (q) / Выход из текущего режима (q)
# Test with another file / Протестируйте с другим файлом
python3 generate_sound.py -i examples/simple.txt --interactive
```

1. Try navigation through simple examples / Попробуйте навигацию по простым примерам
2. Test different signals / Протестируйте разные сигналы

**TEST 8: Exit and Verify / Выход и проверка**

1. Press `q` to exit / Нажмите `q` для выхода
2. Observe: Terminal returns to normal / Наблюдайте: терминал возвращается в нормальное состояние
3. Check: output/sound.wav updated / Проверьте: файл output/sound.wav обновлен

**Expected:** Clean exit without errors, terminal works normally, last signal saved.

**Ожидается:** Нормальный выход без ошибок, терминал работает корректно, последний сигнал сохранен.

#### Quick Verification (5 minutes) / Быстрая проверка (5 минут)**

```bash
# Launch / Запуск
python3 generate_sound.py -i sound.txt --interactive

# Minimal test / Минимальный тест:
# 1. Press Space (sound should play) / Нажмите Space (должен воспроизвестись звук)
# 2. Press n (next + sound) / Нажмите n (следующий + звук)
# 3. Press R (infinite repeat) / Нажмите R (бесконечный повтор)
# 4. Wait 2 repetitions / Подождите 2 повторения
# 5. Press s (stop) / Нажмите s (остановка)
# 6. Press q (quit) / Нажмите q (выход)
```

**If all 6 steps work - interactive mode is functioning correctly!**

**Если все 6 шагов работают - интерактивный режим функционирует правильно!**

#### Troubleshooting Interactive Mode / Устранение проблем интерактивного режима

**Problem:** "curses error" or distorted display / Искаженное отображение
**Solution:** Increase terminal size to minimum 80x24 characters / Увеличьте размер терминала

**Problem:** Keys not responding / Клавиши не реагируют
**Solution:** Ensure terminal is in focus, press Enter / Убедитесь, что терминал в фокусе

**Problem:** Audio not playing / Звук не воспроизводится
**Solution:** Check system volume, test batch mode first / Проверьте громкость системы
## Signal Format / Формат сигналов

Each line: `frequency;duration_ms;level_percent`

### Examples / Примеры

#### Single frequency / Одиночная частота
```
850;1000;50
```
850 Hz tone, 1000 ms duration, 50% volume

#### Frequency sweep / Частотный диапазон
```
1200-850;1200;40-10
```
Ramp from 1200 Hz down to 850 Hz over 1200 ms, volume 40% to 10%

#### Chord / Аккорд
```
1200,850;1000;20,30
```
Two frequencies: 1200 Hz @ 20% + 850 Hz @ 30%, 1000 ms

## Cross-Platform Playback / Кроссплатформенность

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

## Project Structure / Структура проекта

```
soundtest/
├── generate_sound.py      # Main script
├── README.md              # Documentation
├── LICENSE                # MIT License
├── sound.txt              # Example signals
├── .project_profile.json  # Session recovery
├── output/                # Generated WAV files
└── examples/              # Additional examples
    ├── simple.txt         # Simple examples
    ├── complex.txt        # Complex examples
    └── test.txt           # Test signals
```

## Examples / Примеры

```bash
# Simple tones
python3 generate_sound.py -i examples/simple.txt

# Complex sweeps and chords
python3 generate_sound.py -i examples/complex.txt --interactive

# Test signals
python3 generate_sound.py -i examples/test.txt
```

## Troubleshooting / Устранение проблем

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

## License / Лицензия

MIT License - see LICENSE file

## Contributing / Участие

Contributions welcome! Areas for improvement:
- Signal visualization
- Additional audio formats
- Enhanced TUI features
- More signal types
