# mmdmatic - MMD Motion Auto-Trace Installer on Conda

## Abstruct

Mmdmatic is a suite of scripts which install MMD motion auto-trace tools (as follows) on Windows environment.

 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [mannequinchallenge-vmd](https://github.com/miu200521358/mannequinchallenge-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)

Mmdmatic is based on miu's MMD Auto Trace (local version), and it is modified to deploy tf-pose-estimation instead of OpenPose for easier installation.

## Supported platforms

64-bit version of Windows 10 (32-bit versions are not supported).  
NVIDIA GPU driver is needed. 
[Cloud version](https://qiita.com/miu200521358/items/fb0a7bcf2764d7797e26) is recommended for GPU-less PCs.

## Installation

### Extract the archive (or git clone)

1. Download the ZIP archive of this program from GitHub repository.
2. Extract the archive into any folder you like (e.g. C:\App).

### Install Anaconda + Python

1. Download an Anaconda installer for Windows from https://www.anaconda.com/products/individual .
Please select Python 3.7 version 64-bit Graphical Installer.

2. Run the installer.
In "Advanced Options", check the "Add Anaconda3 to my PATH environment variable" option.
You can leave any other options as default and simply click "Next".

### Install tools and packages

1. Run setup.bat
2. Click "Install" button on "mmdmatic setup" window.  
   Install process takes a long time. Please wait with patience.
3. When 'installation finished' message appears, you can close the mmdmatic setup window.

## How to run

1. Run autotracevmd.bat
2. Click "Select" button and select a video file to analyze.
3. Click "Run" button to start auto-trace.  
   Auto-trace process may take a long time depending on the length of the video and GPU performance.
4. When 'auto-trace finished' message appears, click "OK" button.
5. A new folder opens automatically. You can find the generated VMD file in the folder.

## Uninstallation

uninstall.bat will remove Python packages and virtual environment installed/created by the installer.  
Then you can remove the folder (e.g. C:\App\mmdmatic) which contains the batch files and the tools.  
You can also uninstall Anaconda from "Control Panel" - "Programs and Features"

## License

Please see each tool's README and LICENSE files installed into following folders.

- tf-pose-estimation
- mannequinchallenge-vmd
- 3d-pose-baseline-vmd
- VMD-3d-pose-baseline-multi

Please note that MMD motion auto-trace uses a neural network model trained with a dataset (Human 3.6M) which can be used for non-commercial purposes only.
In other words, please avoid using the MMD motion auto-trace commercially.

This program (mmdmatic) itself is under MIT license. Please see LICENSE file for details.

## Bug report

If you find a bug, please contact me.

- Create an "issue" on GitHub  
  https://github.com/errno-mmd/mmdmatic/issues
- Mention @errno_mmd on Twitter  
  https://twitter.com/errno_mmd
