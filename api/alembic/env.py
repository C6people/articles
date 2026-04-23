"""Alembic マイグレーション環境設定

このファイルはAlembicがマイグレーションを実行する際に呼ばれます。
database.pyのエンジン設定とモデル定義（Base.metadata）を読み込み、
自動生成（autogenerate）機能を有効にしています。
"""

import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config

from alembic import context

# Dockerコンテナ内で src パッケージを見つけるためにパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# Alembic Configオブジェクト（alembic.iniの設定を読み込む）
config = context.config

# ログの設定
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ======================================
# ★ ここが重要: モデルのメタデータを読み込む
# ======================================
# database.pyからBaseを、modelsパッケージからモデル定義を読み込みます。
# 新しいモデル（テーブル）を追加したら、必ずここでimportしてください。
from src.database import Base, DATABASE_URL
import src.models  # noqa: F401 - モデルの登録のために必要

target_metadata = Base.metadata

# 環境変数から読み込んだDATABASE_URLをAlembicに設定
# ※ asyncpgドライバはAlembicの同期処理では使えないため、psycopg2に置き換えます
sync_url = DATABASE_URL.replace("+asyncpg", "")
config.set_main_option("sqlalchemy.url", sync_url)


def run_migrations_offline() -> None:
    """オフラインモードでマイグレーションを実行（SQLを出力するだけ）"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """オンラインモードでマイグレーションを実行（実際にDBに適用）"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
