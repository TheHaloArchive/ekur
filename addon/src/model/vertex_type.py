from enum import IntEnum, auto

__all__ = ["VertexType"]


class VertexType(IntEnum):
    World = 0
    Rigid = auto()
    Skinned = auto()
    ParticleModel = auto()
    Screen = auto()
    Debug = auto()
    Transparent = auto()
    Particle = auto()
    Removed08 = auto()
    Removed09 = auto()
    ChudSimple = auto()
    Decorator = auto()
    PositionOnly = auto()
    Removed13 = auto()
    Ripple = auto()
    Removed15 = auto()
    TessellatedTerrain = auto()
    Empty = auto()
    Decal = auto()
    Removed19 = auto()
    Removed20 = auto()
    PositionOnly2D = auto()
    Tracer = auto()
    RigidBoned = auto()
    Removed24 = auto()
    CheapParticle = auto()
    DqSkinned = auto()
    Skinned8Weights = auto()
    TessellatedVector = auto()
    Interaction = auto()
    NumberOfStandardVertexTypes = auto()
