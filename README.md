# mmdmatic - MMD Motion Auto-Trace Installer on Conda

## 概要
Windows上にMMD自動トレースの環境を(わりと簡単に)構築するインストーラです。

## インストール

### 本プログラムの展開

GitHubから本プログラムのZIPファイルをダウンロードして適当なフォルダ(例: C:\App)に展開します。
以下の説明では、この展開されたフォルダが C:\App\mmdmatic だとします。
別のフォルダに置いた場合は適宜読み替えてください。

### Anaconda + Python のインストール

https://www.anaconda.com/distribution/ からAnacondaのWindows用インストーラをダウンロードします。このインストーラにはPythonも同梱されています。必ずPython 3系を選んでください(Anaconda 2019.07ならPython 3.7 version)。かつ、お使いのWindowsが 64ビット版 なら 64-Bit Graphical Installer、32ビット版なら 32-Bit Graphical Installer を選びましょう。

ダウンロードしたインストーラを実行します。途中の Advanced Options で、"Add Anaconda to my PATH environment variable" にチェックを入れます。それ以外はデフォルト設定のまま Next をクリックしていきます。
Setting up the package cache ... と表示された後しばらく時間がかかりますが、止まったように見えても Show details をクリックすると動いているのが分かります。最後に Finish をクリックして終了です。

### Visual Studio のインストール

PythonのモジュールをビルドするためにC++コンパイラが必要な場合があります。
そこで、 https://visualstudio.microsoft.com/ja/free-developer-offers/ から無償版の Visual Studio Community 2019 のインストーラを入手しましょう。
インストーラを起動すると、インストールする機能を選択できます。ここでは「C++によるデスクトップ開発」を選びます。

### Tensorflow のインストール

GPUを使う場合は tensorflow-gpu-install.bat を、GPUを使わない場合は tensorflow-install.bat を実行します。

最後に "Tensorflow is working. GPU is available" と表示されたら完了です。
(GPUを使わない場合、メッセージの最後は"not available"になります)

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
