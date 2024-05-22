foundTerminal=""
for terminal in "$TERMINAL" x-terminal-emulator mate-terminal gnome-terminal terminator xfce4-terminal urxvt rxvt termit Eterm aterm uxterm xterm roxterm termite lxterminal terminology st qterminal lilyterm tilix terminix konsole kitty guake tilda alacritty hyper wezterm rio; do
    if command -v "$terminal" > /dev/null 2>&1; then
        foundTerminal="$terminal"
        break
    fi
done

if [ -n "$foundTerminal" ]; then
    "$foundTerminal" -e ./venv/bin/python ./src/TTSServer.py &
    ./src/llama.cpp/talk.exe --session ./sessionfile -mw ./models/ggml-small.en-q5_1.bin -ml ./models/Meta-Llama-3-8B-Instruct-IQ4_XS.gguf -p "TelevisionNinja" -t 12 -bn "Fluttershy" -s "python ./src/TTSClient.py"
else
    echo "No terminal emulator found"
fi
