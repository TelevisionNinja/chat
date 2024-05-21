Start-Process python -ArgumentList ".\src\TTSServer.py"
./src/llama.cpp/build/bin/Release/talk.exe --session ./sessionfile -mw ./models/ggml-small.en-q5_1.bin -ml ./models/Meta-Llama-3-8B-Instruct-IQ4_XS.gguf -p "TelevisionNinja" -t 12 -bn "Fluttershy" -s "powershell .\\src\\llama.cpp\\common\\talk\\speak.ps1"
