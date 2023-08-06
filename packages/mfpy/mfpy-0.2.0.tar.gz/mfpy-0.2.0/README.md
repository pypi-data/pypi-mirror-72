mfpy
====

*MoneyForward クラウド勤怠といい感じに通信していい感じに打刻するやつ*

 - Requests + bs4 でできてます
 - Seleniumなどブラウザで殴る系パッケージは使ってないので軽量！
 - そのままCLIツールとして使えて便利！
 - もちろん `import` してご自身の時間管理ツールと結合して使って頂けます


今ある機能
----------

 - 出勤・退勤・休憩・休憩終了のリアルタイム打刻
 - 過去の打刻を一括登録（「日時勤怠」ページでの打刻に相当）


環境
----

 - Python 3.8.2
    - 3.7.7で動くことを確認しました
    - 3.6では動きません
 - macOS Catalina (10.15.4)
    - その他のOSでも多分動きます


入れ方
------

```
$ pip install mfpy
```

失敗する場合: setuptoolsが古いとsetup.cfgを解釈してくれないので、 `pip install mfpy` に失敗する場合は `pip install -U setuptools` を実行してみてください。


使い方 (CLIツールとして)
------------------------

基本形は

```
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード}
```

で、ここにサブコマンドを指定します。


### 出勤・退勤・休憩・休憩終了

```
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード} startjob    # 出勤
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード} finishjob   # 退勤
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード} startbreak  # 休憩
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード} finishbreak # 休憩終了
```

成功したら `OK!`、失敗したら `Failed ({ステータスコード})` と表示します。


### 打刻一括登録

複数打刻の登録には `postentries` サブコマンドを使用します。
`-d` で日付を指定し（省略すると今日扱い）、残りの引数に `HH:MM,HH:MM` の形式で1つ以上作業時間を記述します。

作業時間が1つのみだった場合は、そのまま「出勤」→「退勤」で打刻し、2つ以上ある場合は

「出勤」→「休憩開始」→「休憩終了」→「休憩開始」→…→「休憩終了」→「退勤」

という風に打刻します。（現在のところ、打刻の種類を手動で指定できるローレベルAPI的なのは用意していません)

例えば、

```
$ python -m mfpy -c {会社ID} -u {ユーザーID} -p {パスワード} postentries \
         -d 2020-04-28 \
         "10:00,11:00" "11:22,12:34"
```

と実行すると、

 - 10:00 出勤
 - 11:00 休憩開始
 - 11:22 休憩終了
 - 12:34 退勤

と登録されます。


使い方 (Python モジュールとして)
--------------------------------

`mfpy` パッケージを `import` してご自身のプログラムからMF勤怠に打刻するのに使えます。
サンプルとして、使用例の全パターンを [`/mfpy/__main__.py`](/mfpy/__main__.py) に記述しています。参考にしてください。

例えば、出勤打刻するには以下のように呼びます。

```
import mfpy

with mfpy.client('company_id', 'user_id', 'password') as client:
    print(f'Starting job... ', end='')
    ok, status = client.start_job()
    print('OK!' if ok else f'Failed ({status})')
```
