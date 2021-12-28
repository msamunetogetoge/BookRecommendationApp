# BookRecommendationApp
本を検索したり、おススメを推薦してくれるアプリ  
[GCP上](https://bookrecommend.uc.r.appspot.com/)で動いてます  
一応スマートフォンから見るのも想定しています  
## 今できる事
- 本の検索(タイトル、著者)
- 本のあらすじを表示
- アマゾンに飛んで本を買う(作者のアフィリエイトリンク)
- ユーザー登録
- お気に入りの著者登録
- 感想記録
- 読みたい本の登録

## 今後出来るようにしたい事
- お気に入りの著者で書籍検索
- ジャンルでの本のお勧め紹介

## 使ってる技術など
- python3.9系
- javascript(jquery)
- django3.2
- postgressql
- 書籍の検索はGoogleBooksApi
- GCPのAppEngineとCloudSqlにCloudBuildでデプロイ
