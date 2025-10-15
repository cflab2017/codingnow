from dataclasses import dataclass, field
from typing import List, Literal, Optional

@dataclass
class LauncherState:
    x: float
    y: float = 0.0

@dataclass
class MeteorState:
    id: int
    x: float
    y: float
    vx: float
    vy: float
    radius: float

@dataclass
class MissileState:
    id: int
    state: Literal["idle", "flying", "exploded"]
    x: float
    y: float
    vx: float
    vy: float

@dataclass
class Observation:
    time: float
    launcher: LauncherState
    meteors: List[MeteorState] = field(default_factory=list)
    missiles: List[MissileState] = field(default_factory=list)
    g: float = 9.8
    ammo: int = 0
    reload_cooldown: float = 0.0

@dataclass
class Action:
    action: Literal["shoot", "wait", "noop"]
    angle_deg: Optional[float] = None
    speed: Optional[float] = None
