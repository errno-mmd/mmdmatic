# mmdmatic - MMD Motion Auto-Trace Installer on Conda

## 概要
Windows上にMMD自動トレースの環境を(わりと簡単に)構築するインストーラです。
下記のプログラム群をインストールします。
 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [FCRN-DepthPrediction-vmd](https://github.com/miu200521358/FCRN-DepthPrediction-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)
 - [MotionTraceBulk](https://github.com/errno-mmd/motion_trace_bulk/tree/mmdmatic)

## 動作環境

64bit版 Windows 7/10 で動作します(32bit版Windowsは非サポート)。
もしGPU版を使う場合は NVIDIA GPU ドライバがインストールされている必要があります。

## インストール

### 本プログラムの展開

GitHubから本プログラムのZIPファイルをダウンロードして適当なフォルダ(例: C:\App)に展開します。
以下の説明では、この展開されたフォルダが C:\App\mmdmatic だとします。
別のフォルダに置いた場合は適宜読み替えてください。

### Anaconda + Python のインストール

https://www.anaconda.com/distribution/ からAnacondaのWindows用インストーラをダウンロードします。このインストーラにはPythonも同梱されています。必ずPython 3系(Anaconda 2019.07ならPython 3.7 version)の 64-Bit Graphical Installer を選びましょう。

ダウンロードしたインストーラを実行します。途中の Advanced Options で、"Add Anaconda to my PATH environment variable" にチェックを入れます。それ以外はデフォルト設定のまま Next をクリックしていきます。
Setting up the package cache ... と表示された後しばらく時間がかかりますが、止まったように見えても Show details をクリックすると動いているのが分かります。最後に Finish をクリックして終了です。

### Visual Studio のインストール

PythonのモジュールをビルドするためにC++コンパイラが必要な場合があります。
そこで、 https://visualstudio.microsoft.com/ja/free-developer-offers/ から無償版の Visual Studio Community 2019 のインストーラを入手しましょう。
インストーラを起動すると、インストールする機能を選択できます。ここでは「C++によるデスクトップ開発」を選びます。

### Tensorflow のインストール

GPUを使う場合は tensorflow-gpu-install.bat を、GPUを使わない場合は tensorflow-install.bat を実行します。
最初に "Proceed ([y]/n)?" と聞かれるので、y を入力してエンターキーを押します。
最後に "COMPLETE" と表示されたら完了です。

### Pythonパッケージのインストール

package-install.bat を実行します。

### 自動トレースの各ツールのインストール

下記のバッチファイルを実行します。複数同時に実行しても大丈夫です。

- 3dpose-install.bat
- FCRN-install.bat
- mtbulk-install.bat
- tfpose-install.bat
- VMD3d-install.bat

## 実行方法

インストールが完了したら motion_trace_bulk フォルダができます。
その中の README.md に実行方法が書かれています。

## アンインストール方法

uninstall.bat を実行することでPythonパッケージおよび仮想環境を削除します。
完了したら、本プログラムを展開したフォルダ(例: C:\App\mmdmatic)を削除してください。

もし Anaconda や Visual Studio も不要な場合は、「コントロールパネル」 - 「プログラムと機能」 
から、それぞれアンインストールしてください。

## ライセンス

下記の各フォルダ内にインストールされる各ツールのREADMEおよびライセンスファイルを参照してください。
なお、これらのツールが使っているデータセットに商用利用不可のもの(Human 3.6M)が含まれることに注意してください。

- 3d-pose-baseline-vmd
- FCRN-DepthPrediction-vmd
- motion_trace_bulk
- tf-pose-estimation
- VMD-3d-pose-baseline-multi

本プログラム自体はMITライセンスです。詳しくは LICENSE ファイルを参照してください。

## 連絡先
バグ報告などは下記のいずれかにどうぞ。(上のほうが推奨)
表示されたメッセージと、本プログラムのバージョンを併せてご連絡ください。

(1) GitHub の issue (課題管理)
    https://github.com/errno-mmd/mmdmatic/issues
(2) Twitter で @errno_mmd にメンションを送る
    https://twitter.com/errno_mmd

