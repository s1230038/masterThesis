(ノートPC上で作業)
スタートメニューからDocker Desktopを起動。
Windows Terminal(PowerShell)を起動して、以下を実行。
$ cd "C:\Users\yoyok\gitRepo\m5231142DingLab_SharePoint\Ding-Lab - m5231142\drlFX\papers\latex"
$ docker run --rm -it -v ${PWD}:/workdir thesis_latex:1.4

latex ビルド
cd workdir
./genPDF.sh

------------------------------------------------------
(環境の準備)
Windows TerminalでDockerコンテナを起動
> cd "C:\Users\yoyok\gitRepo\m5231142DingLab_SharePoint\Ding-Lab - m5231142\drlFX\papers\latex"
> docker run -it -v ${PWD}:/workdir ubuntu:18.04

https://qiita.com/BitPositive/items/6b13e2038d628c33be8e
$ apt update && apt upgrade
$ apt install -y texlive-lang-cjk xdvik-ja evince
$ apt install -y texlive-fonts-recommended texlive-fonts-extra


latexをビルド
/workdir # latexmk -pdf template_main.tex

エラーが出るがEnterを押して、最後までビルドを完了させる。

/workdir # grep "not found" template_main.log
! LaTeX Error: File `ulem.sty' not found.
! LaTeX Error: File `siunitx.sty' not found.
LaTeX Warning: File `./Figure/computer_keyboard_hand_itai.png' not found on inp
LaTeX Warning: File `./Figure/kaden_PC.png' not found on input line 56.
! Package pdftex.def Error: File `./Figure/kaden_PC.png' not found: using draft
LaTeX Warning: File `./Figure/kaden_laptop.png' not found on input line 63.
! Package pdftex.def Error: File `./Figure/kaden_laptop.png' not found: using d

# apk add texlive


インストール後にdockerコンテナを新たなdockerイメージとして保存。
https://qiita.com/tubone/items/a3bad04abf4c700cae3d
# exit
# docker ps -a
> docker commit confident_tu thesis_latex:1.2

> cd "C:\Users\yoyok\gitRepo\m5231142DingLab_SharePoint\Ding-Lab - m5231142\drlFX\papers\latex"
> docker run -it -v ${PWD}:/workdir thesis_latex:1.2

# exit
# docker ps -a
> docker commit 26874abfba69 thesis_latex:1.3

https://qiita.com/Rumisbern/items/d9de41823aa46d5f05a8#latexmk
に従って設定。


------------------------------------------------------
（OpenDetex のインストール）
Wordの校閲ツールを利用する前準備のためにインストールする。
https://orebibou.com/ja/home/201704/20170425_001/
https://github.com/pkubowicz/opendetex
https://stackoverflow.com/questions/829408/extract-text-from-tex-remove-latex-tags

$ docker run --rm -it -v ${PWD}:/workdir thesis_latex:1.3
$ cd /home

$ apt-get update
$ apt-get install -y make gcc flex
$ apt-get install -y git

$ git clone https://github.com/pkubowicz/opendetex.git
$ cd opendetex/
$ make && make install
$ which detex 

インストール後にdockerコンテナを新たなdockerイメージとして保存。(環境の準備)を参照。
# exit
# docker ps -a
# docker commit ddafbd39349c thesis_latex:1.4
# docker rm ddafbd39349c

How to use
# cd /workdir
# detex m5231142.tex > plain.txt
or
# detex -r m5231142.tex > m5231142plain.txt
上記のファイルをWordにコピペして校閲する。

------------------------------------------------------
承認ページを署名捺印付きの写真に差し替える方法：
　署名写真をJPEGファイルで取り込み、Wordに余白をゼロにして貼り付け保存し、PDFを発行。
　CubePDF Utilityで上記の署名写真PDFを挿入。
しかし、上記の方法では目次情報やリンクは壊れてしまう。
代わりにsignaturePhoto.patchで写真を取り込むか否かを切り分ける。

署名写真が縦横が逆になってPDFに取り込まれる場合は、そのjpegファイルを編集で開いて一回転して上書き保存すると、写真の縦横を正しくなってPDFに取り込まれる。