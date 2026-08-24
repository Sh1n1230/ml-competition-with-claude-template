"""commons.paths のテスト。"""

from __future__ import annotations

import pytest

from commons import paths


def test_repo_root_contains_pyproject() -> None:
    """リポジトリルートの判定が正しいこと。"""
    assert (paths.get_repo_root() / "pyproject.toml").exists()


def test_directory_helpers_are_under_root() -> None:
    """各ディレクトリヘルパがルート配下を指すこと。"""
    root = paths.get_repo_root()
    for path in (paths.data_dir(), paths.outputs_dir(), paths.logs_dir(), paths.preds_dir()):
        assert root in path.parents or path == root


def test_ensure_parent_dir_creates_directory(tmp_path) -> None:
    """親ディレクトリが作成されること。"""
    target = tmp_path / "a" / "b" / "c.csv"
    paths.ensure_parent_dir(target)
    assert target.parent.is_dir()


def test_assert_writable_rejects_raw_dir() -> None:
    """raw ディレクトリへの書き込みが拒否されること。"""
    with pytest.raises(ValueError):
        paths.assert_writable(paths.raw_dir() / "train.csv")


def test_assert_writable_allows_processed_dir() -> None:
    """processed ディレクトリへの書き込みが許可されること。"""
    target = paths.processed_dir() / "features.parquet"
    assert paths.assert_writable(target) == target
