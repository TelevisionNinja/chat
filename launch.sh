python ./src/TTSServer.py &
./src/llama.cpp/talk.exe --session ./sessionfile -mw ./models/ggml-small.en-q5_1.bin -ml ./models/Meta-Llama-3-8B-Instruct-IQ4_XS.gguf -p "TelevisionNinja" -t 12 -bn "Fluttershy" -s "python ./src/TTSClient.py"
