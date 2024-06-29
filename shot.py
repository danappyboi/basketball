class Shot:
    #TODO: should posX/Y be ints or floats?
    def __init__(self, posX, posY, made, time):
        self.posX = posX
        self.posY = posY
        self.made = made
        self.time = time #TODO: how do we wanna represent time?
    
    def is_3(self) -> bool:
        """Returns whether or not the shot is a 3 Pointer"""
        #TODO: gotta be able to figure this out
        return False

    #Order of data: 
    # posX | posY | 3pt | made | time
    def to_data(self):
        return [self.posX, self.posY, self.is_3(), self.made, self.time] 

    def __hash__(self) -> int:
        return hash(f"{self.posX}{self.posY}{self.is_3()}{self.made}{self.time}")
    
    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.time == other.time
    
    def __repr__(self):
        return str(self.to_data())

def to_Shot(data) -> Shot:
    posX = float(data[0])
    posY = float(data[1])
    made = bool(data[3])
    time = int(data[4])
    return Shot(posX, posY,made, time)