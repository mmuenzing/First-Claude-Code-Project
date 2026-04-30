import os
import pytest
from app import save_feedback, save_rating


def test_save_feedback_writes_to_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = save_feedback("Great app!")
    assert result is True
    assert (tmp_path / "feedback.txt").read_text() == "Great app!\n"


def test_save_feedback_appends(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_feedback("First")
    save_feedback("Second")
    lines = (tmp_path / "feedback.txt").read_text().splitlines()
    assert lines == ["First", "Second"]


def test_save_feedback_empty_string_returns_false():
    assert save_feedback("") is False


def test_save_feedback_whitespace_only_returns_false():
    assert save_feedback("   ") is False


def test_save_rating_helpful(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = save_rating("helpful")
    assert result is True
    assert (tmp_path / "ratings.txt").read_text() == "helpful\n"


def test_save_rating_not_helpful(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = save_rating("not_helpful")
    assert result is True
    assert (tmp_path / "ratings.txt").read_text() == "not_helpful\n"


def test_save_rating_appends(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_rating("helpful")
    save_rating("not_helpful")
    lines = (tmp_path / "ratings.txt").read_text().splitlines()
    assert lines == ["helpful", "not_helpful"]


def test_save_rating_invalid_returns_false():
    assert save_rating("maybe") is False


def test_save_rating_empty_returns_false():
    assert save_rating("") is False
