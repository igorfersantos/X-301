from typing import List

class Zone:
    id: int
    name: str
    continent: str
    location: List[float]
    is_dungeon: int
    marker_type: int
    guide_path: str

    def __init__(self, id: int, name: str, continent: str, location: List[float], is_dungeon: int, marker_type: int, guide_path: str) -> None:
        self.id = id
        self.name = name
        self.continent = continent
        self.location = location
        self.is_dungeon = is_dungeon
        self.marker_type = marker_type
        self.guide_path = guide_path


class PapunikaMap:
    name: str
    continent: str
    zones: List[Zone]

    def __init__(self, name: str, continent: str, zones: List[Zone]) -> None:
        self.name = name
        self.continent = continent
        self.zones = zones