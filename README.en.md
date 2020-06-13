# mmdmatic - MMD Motion Auto-Trace Installer on Conda

## Abstruct

Mmdmatic is a suite of batch files which install MMD motion auto-trace tools (as follows) on Windows environment.

 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [mannequinchallenge-vmd](https://github.com/miu200521358/mannequinchallenge-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)
 - [MotionTraceBulk](https://github.com/errno-mmd/motion_trace_bulk/tree/mmdmatic)

Mmdmatic is based on miu's MMD Auto Trace (local version), and it is modified to deploy tf-pose-estimation instead of OpenPose for easier installation.

## Supported platforms

64-bit version of Windows 10 (32-bit versions are not supported).  
NVIDIA GPU driver is needed. 
WARNING: If a NVIDIA GPU is not available, auto-trace process may freeze.
[Cloud version](https://qiita.com/miu200521358/items/fb0a7bcf2764d7797e26) is recommended for GPU-less PCs.

## Installation

### Extract the archive (or git clone)

1. Download the ZIP archive of this program from GitHub repository.
2. Extract the archive into any folder you like (e.g. C:\App).

### Install Anaconda + Python

1. Download an Anaconda installer for Windows from https://www.anaconda.com/products/individual .
Please select Python 3.7 version 64-bit Graphical Installer.

2. Run the installer.
In "Advanced Options", check the "Add Anaconda to my PATH environment variable" option.
You can leave any other options as default and simply click "Next".

### Install Tensorflow

1. If you prefer to use a GPU, run tensorflow-gpu-install.bat.
Otherwise, run tensorflow-install.bat (not recommended).
2. If the batch ask you "Continue creating environment (y/[n])?", press Y and then press Enter.
3. When the batch ask you "Proceed ([y]/n)?", press Y and then press Enter.
4. The batch shows "COMPLETE" when the installation finished successfully.

### Install Python packages

Run package-install.bat

### Install MMD motion auto-trace tools

Run the following batch files. You can run them in parallel.

- 3dpose-install.bat
- mannequin-install.bat
- mtbulk-install.bat
- tfpose-install.bat
- VMD3d-install.bat

## How to run

Run MotionTraceBulk_en.bat in motion_trace_bulk folder and answer to the questions the batch asks.  
(You can find more detailed instruction in motion_trace_bulk/README.md, but it is written in Japanese)


## Uninstallation

uninstall.bat will remove Python packages and virtual environment installed/created by the installer.  
Then you can remove the folder (e.g. C:\App\mmdmatic) which contains the batch files and the tools.  
You can also uninstall Anaconda from "Control Panel" - "Programs and Features"

## License

Please see each tool's README and LICENSE files installed into following folders.

- 3d-pose-baseline-vmd
- mannequinchallenge-vmd
- motion_trace_bulk
- tf-pose-estimation
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
