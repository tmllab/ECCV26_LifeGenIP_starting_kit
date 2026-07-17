def protect(videos: dict) -> dict:
    """Edit this with your protection method. Default: pass-through."""
    return {n: v.copy() for n, v in videos.items()}
