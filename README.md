# mmdmatic - MMD Motion Auto-Trace Installer on Conda

English version (README.en.md) is also available.

## 概要

Windows上にMMD自動トレースの環境を(わりと簡単に)構築するインストーラです。
下記のプログラム群をインストールします。
 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [FCRN-DepthPrediction-vmd](https://github.com/miu200521358/FCRN-DepthPrediction-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)
 - [MotionTraceBulk](https://github.com/errno-mmd/motion_trace_bulk/tree/mmdmatic)

miuさんが開発されたローカル版MMD自動トレースをベースにしていますが、OpenPoseの代わりに tf-pose-estimation を採用することでインストールを簡単にしています。

MMD自動トレースについて詳しくは[MMDモーショントレース自動化への挑戦](https://qiita.com/miu200521358/items/d826e9d70853728abc51)を参照してください。

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

### Tensorflow のインストール

- GPUを使わない場合は tensorflow-install.bat を実行します。
- CUDAに対応したNVIDA GPUを搭載しているPCなら、代わりに tensorflow-gpu-install.bat を実行することで高速なGPU版をインストールできます。

どちらを実行した場合でも、最初に "Proceed ([y]/n)?" と聞かれるので、y を入力してエンターキーを押します。
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

もし Anaconda も不要な場合は、「コントロールパネル」 - 「プログラムと機能」 
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

## FAQ

Q. インストールの途中で次のようなエラーが出る。どうしたらいい？
「curl: (35) schannel: next InitializeSecurityContext failed: Unknown error (0x80092012)」
A. 一部のセキュリティソフトでSSL通信のスキャン機能を有効にしているとこのエラーが発生することが報告されています。
具体的には、カスペルスキーインターネットセキュリティの場合、下記ページに従ってSSLトラフィックの
スキャンを無効にすると解決するようです。
https://support.kaspersky.co.jp/9498
原因をもう少し詳しく書くと、SSLの通信をカスペルスキーが横取りしてその内容をスキャンするために、
接続先サイトから受けた証明書をカスペルスキーの自己署名証明書に置き換えるという行儀の悪いことをするせいで、
この通信は安全ではないとクライアント(curl)が判断してエラーにするようです。
curlの挙動はこれで正しいと思うので、オプションは変更せずそのままにしてあります。

Q. 自動トレースの実行に失敗したが、ウィンドウがすぐ閉じてエラーメッセージが見られない。どうすれば見られる？
A. スタートメニューの「Anaconda3 (64-bit)」にある「Anaconda Prompt」を起動し、
   インストール先フォルダに移動してから(例: cd C:\App\mmdmatic\motion_trace_bulk)、
   自動トレースのバッチ(MotionTraceBulk.bat)を実行してみてください。

## 連絡先

バグ報告などは下記のいずれかにどうぞ(上のほうが推奨)。
表示されたメッセージと、本プログラムのバージョンを併せてご連絡ください。

- GitHub の issue (課題管理)
  https://github.com/errno-mmd/mmdmatic/issues
- Twitter で @errno_mmd にメンションを送る
  https://twitter.com/errno_mmd
