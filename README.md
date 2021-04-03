Webメディア研究会のINIAD Times(https://iniad-wm.com/ )用プログラム

## 環境構築
* 必要環境: [Docker Desktop (macOS or Windows) または Docker Engine + Docker Compose(Linux)](https://docs.docker.com/get-docker/)

1. cloneしたあとのフォルダに.envファイルを以下のように作る
```dotenv
PORT=8080
CIRCLE_SITE_PORT=8081
DATABASE_ENGINE=postgres
DATABASE_NAME=iniad-times
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=changeit
POSTGRES_DB=iniad-times
POSTGRES_PASSWORD=changeit
DJANGO_SECRET_KEY=changeit
DEBUG=true
ACCOUNT_DEFAULT_HTTP_PROTOCOL=http
```

2. docker-compose up --build で起動

3. 127.0.0.1:8080 でINIAD Times, 127.0.0.1:8081でサークルサイトにアクセスできる
