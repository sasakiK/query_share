# ベースイメージの指定
FROM python:3.6

ENV APP_PORT /usr/src/flask-tutorial

# ソースを置くディレクトリを変数として格納
ARG project_dir=/usr/src/flask-tutorial/

# 必要なファイルをローカルからコンテナにコピー
ADD requirements.txt $project_dir

# requirements.txtに記載されたパッケージをインストール
WORKDIR $project_dir
RUN pip install -r requirements.txt
