def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

CellType = enum("beach", "sea", "icefloe")
AgentType = enum("orca", "seal", "fish")