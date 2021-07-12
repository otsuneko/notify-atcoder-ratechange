# notify-atcoder-ratechange

AtCoderのレート更新有無がないか定期的に非公式API(atcoder.jp/users/ユーザ名/history/json)を叩いて確認し、更新があった場合LINEに通知してくれるツールです。
[Codeforces版](https://github.com/otsuneko/notify-cf-ratechange)

## 必要なもの

- Githubアカウント
- Herokuアカウント
- クレジットカード情報(Herokuでアプリを定期実行するのに必要。課金は不要。)
- LINE Notifyの利用登録、APIキー取得
- ローカル開発環境(筆者環境はPython 3.8.3 + PostgreSQL 13)

## 使い方

[こちらの記事](https://otsuneko-blog.com/posts/notify-cf-ratechange)参照。Codeforces版の手順を纏めた記事ですが、AtCoder版も基本的に同じ手順で進められます(DBのカラム等、一部AtCoder用に変える必要があります)。
