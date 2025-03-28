from engine import GhostEngine


def connect(source: str) -> GhostEngine:
    return GhostEngine(source)    