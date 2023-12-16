## レポジトリ概要
OpenAIのクレジットを組織内で分配する際、OpenAIのデフォルトの機能では組織単位の使用制限しかかけることができず、誰がどれだけ使っているか、またその量に応じた制限などを設定することができない。そのためこのレポジトリでは、プロキシサーバを構築することで、どのAPI-Keyがどれだけ使われているのかの確認とそれに応じた制限をかけることを可能にする。

## API使用方法
OpenAIのAPIを使う方法は二つある。  
一つは各言語に用意されているSDKを用いる方法。  
もう一つは、httpエンドポイントを直接叩く方法である。  
このレポジトリでは、クレジットの使用量を把握するためにAPIを使う方法をhttpエンドポイントを叩く方法に限定する。  
詳細な使い方は[公式ドキュメント](https://platform.openai.com/)を参照

以下のURLのAPIを使う際  
```
https://api.openai.com/{path}  
```
ドメイン部をプロキシサーバに変更した下のURLを使用する。  
```
https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy/{path}  
```
以下はcurlコマンドの例である。本来API-Keyを入力する所を、クレジットの配布者が発行するuser_idに変更する。  

```  
curl https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy/<path> \  
  -H "Authorization: Bearer $<user_id>" \  
  -H "Content-Type: application/json"  
```

## 設計概要
OpenAIのサーバにダイレクトにリクエストを送信すると、誰がどれだけクレジットを使用したかを把握するすべがない。そのため、プロキシサーバを経由して通信することで、誰がどのようなAPIをどれだけ使ったかを記録する。プロキシサーバとしてGCFを用い、データの永続化にはGCSを用いることでランニングコストを最小限に落とす。

## プロキシサーバ構築方法
ーーーーー

## クレジットの配布方法
ーーーーー  
**注意** クレジットを特定の組織内でなく一般に公開することはOpenAIの利用規約に違反するっぽいです。ご注意ください。
