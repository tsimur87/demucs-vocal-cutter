import pytest
from demucs_vocal_cutter.downloader import detect_platform

def test_detect_platform():
    assert detect_platform("https://www.youtube.com/watch?v=123") == "youtube"
    assert detect_platform("https://tiktok.com/video/123") == "tiktok"
    assert detect_platform("invalid") == "unknown"