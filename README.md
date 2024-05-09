# chat
Chat with an LLM

- whisper.cpp
- llama.cpp


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
cd ./src/

make -j WHISPER_CUDA=1

cd ..
sudo chmod +x ./launch.sh
```

Without CUDA
```bash
cd ./src/

make -j

cd ..
sudo chmod +x ./launch.sh
```

## MacOS
```bash
cd ./src/

make -j

cd ..
sudo chmod +x ./launch.sh
```

## Windows
With CUDA
```bash
cmake -DWHISPER_SDL2=ON -WHISPER_CUDA=ON -B build
cmake --build build --config release
```

Without CUDA
```bash
cmake -DWHISPER_SDL2=ON -B build
cmake --build build --config release
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
