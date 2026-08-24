"""Repository path helpers.

すべての入出力パスはこのモジュール経由で構成する（絶対パスのハードコード禁止）。
"""

from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def get_repo_root() -> Path:
    """リポジトリ（コンペプロジェクト）のルートを返す。"""
    env_root = os.getenv("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return _DEFAULT_ROOT


def data_dir() -> Path:
    """`data/` ディレクトリを返す。"""
    return get_repo_root() / "data"


def raw_dir() -> Path:
    """`data/raw/`（不変の配布データ）を返す。"""
    return data_dir() / "raw"


def processed_dir() -> Path:
    """`data/processed/`（加工済みデータ・特徴量）を返す。"""
    return data_dir() / "processed"


def preds_dir() -> Path:
    """`data/processed/preds/`（各baseモデルのOOF/test予測）を返す。"""
    return processed_dir() / "preds"


def outputs_dir() -> Path:
    """`outputs/`（図・表・レポート）を返す。"""
    return get_repo_root() / "outputs"


def logs_dir() -> Path:
    """`logs/`（実験ログ）を返す。"""
    return get_repo_root() / "logs"


def ensure_parent_dir(path: Path) -> Path:
    """親ディレクトリを作成してからパスを返す。

    Args:
        path: 書き込み先のファイルパス。

    Returns:
        引数と同じパス。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def assert_writable(path: Path) -> Path:
    """書き込み先が不変ディレクトリでないことを検証する。

    Args:
        path: 書き込み先のファイルパス。

    Returns:
        引数と同じパス。

    Raises:
        ValueError: `data/raw/` または `data/external/` 配下に書き込もうとした場合。
    """
    resolved = path.resolve()
    for immutable in (raw_dir(), data_dir() / "external"):
        if immutable.resolve() in resolved.parents:
            raise ValueError(f"immutable directory is not writable: {resolved}")
    return path
