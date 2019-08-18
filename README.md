# autotracevmd - ローカル版MMD自動トレース

## 概要
Windows上にMMD自動トレースの環境を(わりと簡単に)構築します。

追加説明は後で書きます・・・

## 準備

### 本プログラムのインストール

GitHubから本プログラムのZIPファイルをダウンロードして適当なフォルダ(例: C:\App)に展開します。
以下の説明では、この展開されたフォルダが C:\App\autotracevmd だとします。
別のフォルダに置いた場合は適宜読み替えてください。

### Anaconda + Python のインストール

https://www.anaconda.com/distribution/ からAnacondaのWindows用インストーラをダウンロードします。このインストーラにはPythonも同梱されています。図のように必ずPython 3系を選んでください(Anaconda 2019.07ならPython 3.7 version)。かつ、お使いのWindowsが 64ビット版 なら 64-Bit Graphical Installer、32ビット版なら 32-Bit Graphical Installer を選びましょう。

ダウンロードしたインストーラを実行します。途中の Advanced Options で、"Add Anaconda to my PATH environment variable" にチェックを入れます。それ以外はデフォルト設定のまま Next をクリックしていきます。
Setting up the package cache ... と表示された後しばらく時間がかかりますが、止まったように見えても Show details をクリックすると動いているのが分かります。最後に Finish をクリックして終了です。

### Tensorflow のインストール

GPUを使う場合は tensorflow-gpu-install.bat を、GPUを使わない場合は tensorflow-install.bat を実行します。

最後に "Tensorflow is working. GPU is available" と表示されたら完了です。
(GPUを使わない場合、メッセージの最後は"not available"になります)

### Pythonパッケージのインストール

package-install.bat を実行します。

### 自動トレースの各スクリプトのインストール

下記のバッチファイルを実行します。同時に実行しても構いません。

- tfpose-install.bat
- FCRN-install.bat
- 3dpose-install.bat
- VMD3d-install.bat

## 実行方法

（実行方法は後でもう少し簡単にしたい・・・）

1. スタートメニューから Anaconda Powershell Prompt を実行します。
2. 下記のコマンドを実行して、仮想環境を切り替えます。
```
> activate autotracevmd
```
3. 自動トレースのディレクトリに移動します。
```
> cd C:\App\autotracevmd
```
3. 試しに引数無しで autotracevmd.py を実行してみましょう。使い方(usage)が表示されます。
```
> python autotracevmd.py
usage: autotracevmd.py [-h] [--reuse_2d] [--json_dir JSON_DIR]
                       [--first_frame FIRST_FRAME] [--last_frame LAST_FRAME]
                       [--max_people MAX_PEOPLE] [--reverse_list REVERSE_LIST]
                       [--order_list ORDER_LIST]
                       [--past_depth_dir PAST_DEPTH_DIR] [--add_leg]
                       [--add_leg2] [--verbose VERBOSE]
                       VIDEO_FILE OUTPUT_DIR
autotracevmd.py: error: the following arguments are required: VIDEO_FILE, OUTPUT_DIR
```
4. 動画ファイルと出力先フォルダを引数として、autotracevmd.py を実行します。
```
> python autotracevmd.py "C:\data\input.mp4" ./output

(メッセージ省略)
INFO:__main__:間引き VMDファイル出力完了: C:\フォルダ名/なんとか.vmd
```
無事完了したら、生成されたVMDファイルのパス名が最後に表示されます。
このVMDファイルをMMDに読ませましょう。
