# mmdmatic - MMD Motion Auto-Trace Installer on Conda

English version (README.en.md) is also available.

## 概要

Windows上にMMD自動トレースの環境を(わりと簡単に)構築するインストーラです。
下記のプログラム群をインストールします。
 - [tf-pose-estimation](https://github.com/errno-mmd/tf-pose-estimation)
 - [mannequinchallenge-vmd](https://github.com/miu200521358/mannequinchallenge-vmd)
 - [3d-pose-baseline-vmd](https://github.com/miu200521358/3d-pose-baseline-vmd)
 - [VMD-3d-pose-baseline-multi](https://github.com/miu200521358/VMD-3d-pose-baseline-multi)

miuさんが開発されたローカル版MMD自動トレースをベースにしていますが、OpenPoseの代わりに tf-pose-estimation を採用することでインストールを簡単にしています。  
MMD自動トレースについて詳しくは[MMDモーショントレース自動化への挑戦](https://qiita.com/miu200521358/items/d826e9d70853728abc51)を参照してください。

## 動作環境

64bit版 Windows 10 で動作します(32bit版Windowsは非サポート)。
4GB以上のVRAMを搭載したNVIDIA GPU が必要です。NVIDIA GPUを搭載していないPCをお使いの場合は
[クラウド版](https://qiita.com/miu200521358/items/fb0a7bcf2764d7797e26)をお勧めします。

ディスクの空き容量は約20GB程度必要になります。
また、ツールやデータを大量にダウンロードしてインストールするため、定額制で通信量に制限のないインターネット回線が必要です。

## インストール

（もし旧バージョンがインストール済の場合、本プログラムを旧バージョンに上書きしてアップデートする
ことも可能です。新規インストールよりアップデートのほうが短時間で完了する可能性があります。
詳しくは本ドキュメントの「アップデート」の節を参照してください。）

### 本プログラムの展開

GitHubから本プログラムのZIPファイルをダウンロードして適当なフォルダ(例: C:\App)に展開します。
以下の説明では、この展開されたフォルダが C:\App\mmdmatic だとします。
別のフォルダに置いた場合は適宜読み替えてください。

### Anaconda + Python のインストール

https://www.anaconda.com/products/individual からAnacondaのWindows用インストーラをダウンロードします。このインストーラにはPythonも同梱されています。必ず Python 3.7 版の 64-Bit Graphical Installer を選びましょう。  
ダウンロードしたインストーラを実行します。途中の Advanced Options で、"Add Anaconda3 to my PATH environment variable" にチェックを入れます。それ以外はデフォルト設定のまま Next をクリックしていきます。
Setting up the package cache ... と表示された後しばらく時間がかかりますが、止まったように見えても Show details をクリックすると動いているのが分かります。最後に Finish をクリックして終了です。

### 各ツールやパッケージのインストール

- setup.bat を実行します。
- 「mmdmatic setup」のウィンドウが表示されたら、「Install」ボタンを押します。
- インストールが始まります。インターネット回線の速度にもよりますが、かなり時間がかかります。気長に待ってください。
- 'installation finished' のメッセージボックスが表示されたらインストール完了です。
  mmdmatic setup のウィンドウを閉じてください。

## 実行方法

- autotracevmd.bat を実行します。
- 「input video file」の「Select」ボタンを押して、トレース元の動画ファイルを選択します。
- 「Run」ボタンを押すと自動トレース処理が始まります。
- 動画の長さやGPU性能にもよりますが、かなり時間がかかります。辛抱強く待ってください。
- 「auto-trace finished」のメッセージボックスが表示されたら完了です。
- 「OK」ボタンを押すと、VMDファイルの出力先フォルダが自動的に表示されます。  
   複数人トレースの場合は、そのフォルダと同じ階層に人物毎のフォルダが作られているので、
   そちらも探してください。フォルダ名の末尾は _idx01, _idx02, ... となっています。

まずは[サンプル動画](https://drive.google.com/open?id=1ccBzmONGNDbvmKa7SSqwMRPKQ3q-_6LG)で試し、
正常にVMDファイルが作られるのを確認することをお勧めします。
なお、動画の解像度によってはエラーが起こることがあります。1280x720や1920x1080が無難です。

## オプション

自動トレース実行時に、下記のオプションを指定できます。
- resize to: 動画を指定した解像度に変換してから解析を始めます。チェックを外すと元の解像度を維持しますが、解像度によってはエラーが起こることもあります。
- convert to 30fps: 動画のフレームレートを30フレーム/秒に変換してから解析を始めます。
- max number of people: 動画に映っている解析対象の人数
- first frame to analyze: 解析を開始するフレーム番号(最初のフレームは0)
- last frame to analyze: 解析を終了するフレーム番号(最後のフレームまで解析する場合は-1)
- reverse_specific: 反転指定リスト(後述)
- order_specific: 順番指定リスト(後述)

### 反転指定リスト

tf-pose-estimationが人の正面と背面を誤認識していることがあるので、このリストで指定して向きを反転させます。
反転させるフレーム番号(0始まり)、人物INDEX、反転の内容を指定してください。  
人物INDEX: tf-pose-estimationが第0フレームで人物を認識した順に0, 1, ...とINDEXが割り当てられます。  
フォーマット: [フレーム番号:反転を指定したい人物INDEX,反転内容]  
反転内容: R: 全身反転, U: 上半身反転, L: 下半身反転, N: 反転なし  
例: [10:1,R] -> 第10フレームの1番目の人物を全身反転します。  
message.logに上記フォーマットで、反転出力した場合にその内容を出力しているので、それを参考にしてください。[10:1,R][30:0,U]のように、カッコ単位で複数件指定可能です。

### 順番指定リスト

複数人数トレースで、交差後の人物INDEX順番を指定してください。  
1人トレースの場合は空欄のままで大丈夫です。  
tf-pose-estimationが第0フレームで認識した順番に0, 1, ...とINDEXが割り当てられます。  
フォーマット: [フレーム番号:0番目に推定された人物のインデックス,1番目に推定された人物のインデックス, ...]  
例: [10:1,0] -> 第10フレームは、左から1番目の人物、0番目の人物の順番に並べ替えます。  
message.logに上記フォーマットで、どのような順番で出力したかを残しているので、それを参考にしてください。 [10:1,0][30:0,1]のように、カッコ単位で複数件指定可能です。  
また、output_XXX.aviでは、推定された順番に人物に色が割り当てられています。体の右半分は赤、左半分は以下の色になります。 0:緑, 1:青, 2:白, 3:黄, 4:桃, 5:水色, 6:濃緑, 7:濃青, 8:灰色, 9:濃黄, 10:濃桃, 11:濃水色

## アンインストール方法

uninstall.bat を実行することでPythonパッケージおよび仮想環境を削除します。  
最初の質問にYと答えると削除が実行されます。Nと答えるとキャンセルできます。  
完了したら、本プログラムを展開したフォルダ(例: C:\App\mmdmatic)を削除してください。  
もし Anaconda も不要な場合は、「コントロールパネル」 - 「プログラムと機能」 
から、それぞれアンインストールしてください。

## アップデート

もし旧バージョンがインストール済の場合、下記の手順でアップデートすることが可能です。

1. GitHubから本プログラムのZIPファイルをダウンロードして展開し、
中身を全て旧バージョンが格納されたフォルダ(例: C:\App\mmdmatic) に上書きします。
2. setup.bat を実行し、「Install」ボタンを押します。
3. 'installation finished' のメッセージボックスが表示されたらインストール完了です。
mmdmatic setup のウィンドウを閉じてください。

## ライセンス

下記の各フォルダ内にインストールされる各ツールのREADMEおよびライセンスファイルを参照してください。
なお、これらのツールが使っているデータセットに商用利用不可のもの(Human 3.6M)が含まれることに注意してください。

- 3d-pose-baseline-vmd
- mannequinchallenge-vmd
- tf-pose-estimation
- VMD-3d-pose-baseline-multi

本プログラム自体はMITライセンスです。詳しくは LICENSE ファイルを参照してください。

## FAQ

Q. 何故かVMDファイルが作られない。  
A. 何かエラーが起きているはずです。エラーメッセージを確認してください。
   エラーメッセージでググったり(できれば各ツールのGitHubリポジトリのissueを検索したり)すると解決法が見つかることがあります。
   また、全ての動画でモーション作成が成功するとは限りません。まずサンプル動画で正しく動作するか確認しましょう。

Q. Anacondaはインストール済みなのに "Anaconda is not installed appropriately" のエラーが出る。  
A. Anacondaのインストーラーで "Add Anaconda to my PATH environment variable" を選ばなかった
   のではありませんか？
   Anacondaを一度アンインストールしてインストールし直すほうが簡単だと思いますが、
   この状態でも Anaconda Prompt から各バッチファイルを実行することは可能です。
   スタートメニューの「Anaconda3 (64-bit)」にある「Anaconda Prompt」を起動し、
   インストール先フォルダに移動してから(例: cd C:\App\mmdmatic)、
   setup.bat や autotracevmd.bat を実行してみてください。

Q. 何も表示されずにバッチファイルが終了する。  
A. 上に書かれた方法で Anaconda Prompt から実行して、エラーメッセージを確認してください。

Q. 古いGPUでも使えますか？
A. あまり古いGPUだと、機械学習ライブラリTensorFlowが対応していない可能性があります。
   詳しくは https://www.tensorflow.org/install/gpu?hl=ja を参照してください。

Q. "CUDA driver version is insufficient for CUDA runtime version" というエラーが出る。
A. GPUのドライバが古いので、アップデートしましょう。

Q. "CUDA out of memory" というエラーが出る。
A. GPUのメモリ(VRAM)容量が不足しています。4GB以上のVRAMを搭載したGPUが必要です。
   もし十分なVRAMが有るのにこのエラーが出る場合、他にGPUを使うプログラムが動いていないか確認してください。

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
