FROM node:14.16-alpine

COPY ./package.json /usr/src/app/
WORKDIR /usr/src/app
RUN npm install

COPY . /usr/src/app
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh

ENV HOST 0.0.0.0
EXPOSE 3000

ENTRYPOINT [ "entrypoint.sh" ]
# DEBUG=falseの場合の実行コマンド
CMD npm run build && npm run generate
