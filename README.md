# 5ch(旧2ch)をスクレイピングして、過去はやったネットスラングの今

## 5chの過去ログをスクレイピングするには

### 幅優探索による過去ログのスクレイピング
 URL同士のリンクばネットワーク構造になります。  
 スクレイピングする際の戦略として、ネットワークをどうたどるか、という問題で、幅優先探索を行いました。  
 2chの過去ログから辿れるログは平面的に大量のリンクを2~3回たどれば目的のデータにアクセスできる構造で幅優先探索に適していたからという理由です。  
 
<div align="center">
  <img width="600px" src="https://user-images.githubusercontent.com/4949982/48311037-58ca0300-e5dc-11e8-93b7-b95144a20a2d.png">
</div>
<div align="center"> 図1. ドイツのフランクフルトからの路線図で幅優先探索をした場合(Wikipedia) </div>

#### 起点となる一点を決める
 かねてから2chの全ログ取得は夢でしたが、様々な方法を検討しましたが、ログが保存されているURLの一覧が存在しないということで諦めていたのですが、ついに発見するに至りました。  
 以下のURLからアクセスすることができ、多くのスレの過去ログサーバを参照しています。  
 そのためここからアクセスすることで2chの過去ログをスクレイピングすることができます。  
```
 http://lavender.5ch.net/kakolog_servers.html
```

#### レガシーなhtmlフォーマットに対応する
 Pythonのhtmlパーサーを前提に話しますが、旧2chのHTMLは正しいHTMLというわけでないようです。  
 tableタグを多用するデザインが2017年度半ばまで主流だったようで、このときのタグに閉じるの対応なく、lxml, html.parserなどを使うと失敗します。  
 そのため、一部の壊れたhtmlでもパースできるようにhtml5libパーサーを利用してパースすることができます[1]
 
　この問題は、BeautifulSoupのパーサを以下のようにhtml5libに設定すれば解決することができます。  
```python
soup = bs4.BeautifulSoup(html, 'html5lib')
```
 
#### 並列アクセスを行う
 2chの過去ログは、一つ一つのサーバに名前がついていて、各サーバが異なったサブドメインを持っています。  
 そのため、異なった実サーバをもっていると考えられるので、サーバごとにアクセスを並列化することで高速化することができます。加えて、もともとPythonのrequestsとBeautifulSoupを使ったhtml解析が重い作業なので、マルチコアリソースを最大限利用して、並列アクセスする意義があります。  
 
## ネットスラングの選定
一般的なネットスラングは時代の変遷の影響を受けるという感覚値がありました。  

具体的には、その日における単語の頻度が人気があると高くなり、低くなると下がっていくという感覚値があり、時系列にしたとき、人気の発生から、使われなくなるまでが観測できるのではないかと思い、集計しました。  

過去、２０年間に存在してきた様々なネットスラングについて、様々な[まとめ[2]](https://dic.nicovideo.jp/a/%E3%83%8D%E3%83%83%E3%83%88%E3%82%B9%E3%83%A9%E3%83%B3%E3%82%B0%E3%81%AE%E4%B8%80%E8%A6%A7)があり、みているととても懐かしくなります。  

過去、記憶に強く残っていたり、違和感があったり、今でも使わているのだろうか？最近見ていないがどの程度減ったのか?、という視点で選んだ単語がこれらになります。  

 - orz
 - 尊師
 - 香具師
 - 笑(文末)
 - 初音ミク
 - 結月ゆかり
 - コードギアス
 - hshs
 - iphone
 - うｐ
 - 自宅警備員
 - ワンチャン
 - ステマ
 - 情弱
 - チラ裏
 - 今北産業
 - 禿同
 - w(文末)
 - メシウマ
 - まどマギ
 - ソシャゲ
 - ジワる
 - ナマポ
 - (ry
 - ggrks
 - オワコン
 
この計算は、`time_term_freq.py`で行うことができて、プログラムを変えることで再集計することができます。  


### htmlをjsonl化する
 スクレイピングしたhtmlをスレの内容を取り出し、jsonl(一行に一オブジェクトのjson)にしておくといろいろと集計が都合がよいです。  
`scan_items.py`というプログラムでパースできるので、参考にしてください。 
```console
$ python3 scan_items.py
```
 
### 結果
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311751-fa0a8680-e5e7-11e8-9a58-7a29c43f2136.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311765-1a3a4580-e5e8-11e8-8345-b1b4c1f0cf5f.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311774-30480600-e5e8-11e8-9bc8-b2ff8da2c897.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311779-46ee5d00-e5e8-11e8-9180-b66f04ef1f69.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311785-5cfc1d80-e5e8-11e8-877d-189471126d88.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311790-71401a80-e5e8-11e8-9829-4647df976e2c.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311796-887f0800-e5e8-11e8-96d5-b4905611bcf3.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311802-a2204f80-e5e8-11e8-8a20-e6b333d78903.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311810-b49a8900-e5e8-11e8-9e42-f4316c9d1e3b.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311821-cda33a00-e5e8-11e8-83d8-2e8d3bd0df41.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311828-f297ad00-e5e8-11e8-8173-df0f72e15113.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311841-1824b680-e5e9-11e8-981b-d50440cbc52f.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311846-2b378680-e5e9-11e8-9cc6-5332fcc32a9a.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311870-9ed99380-e5e9-11e8-8faf-195579bed670.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311879-aa2cbf00-e5e9-11e8-8055-dcd45daa443f.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311880-af8a0980-e5e9-11e8-8933-353edc663c27.png">
</div>
<div align="center">
 <img width="700px" src="https://user-images.githubusercontent.com/4949982/48311881-b4e75400-e5e9-11e8-9693-99529d0b7403.png">
</div>

# 参考
 - [1] [How do I fix wrongly nested / unclosed HTML tags?](https://stackoverflow.com/questions/293482/how-do-i-fix-wrongly-nested-unclosed-html-tags)
 - [2] [ネットスラングの一覧](https://dic.nicovideo.jp/a/%E3%83%8D%E3%83%83%E3%83%88%E3%82%B9%E3%83%A9%E3%83%B3%E3%82%B0%E3%81%AE%E4%B8%80%E8%A6%A7)
