# mmdmatic - MMD Motion Auto-Trace Installer on Conda

English version (README.en.md) is also available.

## 概要

Windows上にMMD自動トレースの環境を(わりと簡単に)構築するインストーラです。
下記のプログラム群をインストールします。
 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [mannequinchallenge-vmd](https://github.com/miu200521358/mannequinchallenge-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)
 - [MotionTraceBulk](https://github.com/errno-mmd/motion_trace_bulk/tree/mmdmatic)

miuさんが開発されたローカル版MMD自動トレースをベースにしていますが、OpenPoseの代わりに tf-pose-estimation を採用することでインストールを簡単にしています。  
MMD自動トレースについて詳しくは[MMDモーショントレース自動化への挑戦](https://qiita.com/miu200521358/items/d826e9d70853728abc51)を参照してください。

## 動作環境

64bit版 Windows 10 で動作します(32bit版Windowsは非サポート)。
NVIDIA GPU ドライバがインストールされている必要があります。
なおGPU無しだと動作が非常に遅くフリーズしたようになることもあるため、NVIDIA GPUを搭載していないPCをお使いの場合は
[クラウド版](https://qiita.com/miu200521358/items/fb0a7bcf2764d7797e26)をお勧めします。

## インストール

### 本プログラムの展開

GitHubから本プログラムのZIPファイルをダウンロードして適当なフォルダ(例: C:\App)に展開します。
以下の説明では、この展開されたフォルダが C:\App\mmdmatic だとします。
別のフォルダに置いた場合は適宜読み替えてください。

### Anaconda + Python のインストール

https://www.anaconda.com/products/individual からAnacondaのWindows用インストーラをダウンロードします。このインストーラにはPythonも同梱されています。必ず Python 3.7 版の 64-Bit Graphical Installer を選びましょう。  
ダウンロードしたインストーラを実行します。途中の Advanced Options で、"Add Anaconda to my PATH environment variable" にチェックを入れます。それ以外はデフォルト設定のまま Next をクリックしていきます。
Setting up the package cache ... と表示された後しばらく時間がかかりますが、止まったように見えても Show details をクリックすると動いているのが分かります。最後に Finish をクリックして終了です。

### Tensorflow のインストール

- CUDAに対応したNVIDA GPUを使う場合、tensorflow-gpu-install.bat を実行します。
- もしGPUを使わない場合は代わりに tensorflow-install.bat を実行することもできますが、非常に遅くなることがありますのでお勧めしません。

実行中にもし "Continue creating environment (y/[n])?" と聞かれたら、y を入力してエンターキーを押します。  
"Proceed ([y]/n)?" と聞かれたら、y を入力してエンターキーを押します。  
最後に "COMPLETE" と表示されるので、それを確認してから次に進んでください。

### Pythonパッケージのインストール

package-install.bat を実行します。
最後に "COMPLETE" と表示されるので、それを確認してから次に進んでください。

### 自動トレースの各ツールのインストール

下記のバッチファイルを実行します。複数同時に実行しても大丈夫です。
それぞれ最後に "COMPLETE" と表示されたことを確認してください。

- 3dpose-install.bat
- mannequin-install.bat
- mtbulk-install.bat
- tfpose-install.bat
- VMD3d-install.bat

## 実行方法

インストールが完了したら motion_trace_bulk フォルダができます。
その中の README.md に実行方法が書かれています。

まずは[サンプル動画](https://drive.google.com/open?id=1ccBzmONGNDbvmKa7SSqwMRPKQ3q-_6LG)で試し、
正常にVMDファイルが作られるのを確認することをお勧めします。
なお、動画の解像度によってはエラーが起こることがあります。1280x720や1920x1080が無難です。

## アンインストール方法

uninstall.bat を実行することでPythonパッケージおよび仮想環境を削除します。
完了したら、本プログラムを展開したフォルダ(例: C:\App\mmdmatic)を削除してください。  
もし Anaconda も不要な場合は、「コントロールパネル」 - 「プログラムと機能」 
から、それぞれアンインストールしてください。

## ライセンス

下記の各フォルダ内にインストールされる各ツールのREADMEおよびライセンスファイルを参照してください。
なお、これらのツールが使っているデータセットに商用利用不可のもの(Human 3.6M)が含まれることに注意してください。

- 3d-pose-baseline-vmd
- mannequinchallenge-vmd
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

Q. 何故かVMDファイルが作られない。
A. 何かエラーが起きているはずです。上記のとおり Anaconda Prompt 上で実行してエラーメッセージを確認してください。
   エラーメッセージでググったり(できれば各ツールのGitHubリポジトリのissueを検索したり)すると解決法が見つかることがあります。
   また、全ての動画でモーション作成が成功するとは限りません。まずサンプル動画で正しく動作するか確認しましょう。

## 連絡先

バグ報告は下記のいずれかにどうぞ(上のほうが推奨)。
表示されたメッセージと、本プログラムのバージョンを併せてご連絡ください。
エラーメッセージはコピー＆ペーストでそのままの内容を貼り付けてください。
Twitterの場合は文字数が限られるのでスクリーンショットでも構いません。
（必要な情報が書かれていなかったり、FAQにある内容だったり、あるいは単に忙しかったりすると放置するかもしれませんがご了承ください）

- GitHub の issue (課題管理)  
  https://github.com/errno-mmd/mmdmatic/issues
- Twitter で @errno_mmd にメンションを送る  
  https://twitter.com/errno_mmd
