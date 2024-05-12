# chat
Chat with an LLM

Uses:
- whisper.cpp
- llama.cpp


# Clone The Repository
```bash
git clone https://github.com/TelevisionNinja/chat.git
cd ./chat
git submodule init
git submodule update
```


# Install Dependencies

## Linux
```bash
sudo apt install make gcc g++ libsdl2-dev
```

### CUDA
```bash
sudo apt install nvidia-cuda-toolkit
```

## MacOS
Install brew with
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Install Dependencies with
```bash
brew install make gcc sdl2
```

## Windows
Download and install MSYS2 from the MSYS2 website

Install Dependencies with
```bash
pacman -S mingw-w64-x86_64-cmake mingw-w64-x86_64-gcc mingw-w64-x86_64-SDL2
```

Add the binaries folder to the environment variables

### CUDA

1. Download and install Visual Studio and the C++ workload from Microsoft
2. Download and install the CUDA Toolkit from the Nvidia developer website


# Build

## Linux
With CUDA
```bash
cd ./src/llama.cpp

make -j WHISPER_CUDA=1

cd ../..
```

Without CUDA
```bash
cd ./src/llama.cpp

make -j

cd ../..
```

## MacOS
```bash
cd ./src/llama.cpp

make -j

cd ../..
```

## Windows
With CUDA
```bash
cd ./src/llama.cpp

cmake -DWHISPER_SDL2=ON -WHISPER_CUDA=ON -B build
cmake --build build --config release

cd ../..
```

Without CUDA
```bash
cd ./src/llama.cpp

cmake -DWHISPER_SDL2=ON -B build
cmake --build build --config release

cd ../..
```


# Make Scripts Executable

## Linux and MacOS
```bash
sudo chmod +x ./src/llama.cpp/common/talk/speak.sh
sudo chmod +x ./launch.sh
```


# Run

## Linux and MacOS
```bash
./launch.sh
```

## Windows

```bash
./launchWindows.sh
```
