## API使い方

以下のURLのAPIを使いたい際は
https://api.openai.com/<path>
下のURLに変更する。
https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy/<path>

また、curlのヘッダーのopenai-api-keyを入力する所を管理者が発行するuser_idを入力してもらう。
curl https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy/<path> \
  -H "Authorization: Bearer $<user_id>" \
  -H "Content-Type: application/json"