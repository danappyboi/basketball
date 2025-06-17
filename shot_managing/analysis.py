import csv
from shot_managing.shot import Shot, to_Shot

#TODO: obviously add more stats: 
# mid-range, 3pa/fga
#TODO: should the whole structure just be a dict?
class Analysis:
    """A data structure that reads from a data csv and can update with new data
    using the corresponding update functions"""
    def __init__(self):
        self.total_shots = 0
        self.total_shots_made = 0
        self.total_3s = 0
        self.total_3s_made = 0
    
    #TODO: if the time is the same, should we add it to the update or naw?
    def add_data(self, data : str):
        """Updates the analysis with a data.csv"""
        with open(data, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                shot = to_Shot(row) 
                self.add_shot(shot)

    def add_shot(self, shot : Shot):
        """Updates the analysis with a shot"""
        self.total_shots += 1
        self.total_shots_made += shot.made
        self.total_3s += shot.is_3()
        self.total_3s_made += (shot.is_3() and shot.made)

    def stats(self) -> dict:
        """Returns a dict of all stats"""
        stats = {}
        stats["fga"] = self.get_fga()
        stats["fgm"] = self.get_fgm()
        stats["fg%"] = self.get_fgpct()
        stats["3pa"] = self.get_3pa()
        stats["3pm"] = self.get_3pm()
        stats["3p%"] = self.get_3ppct()
        return stats

    def get_fga(self) -> int:
        """Returns the number of field goals attempted"""
        return self.total_shots
    
    def get_fgm(self) -> int:
        """Returns the number of field goals made"""
        return self.total_shots_made
    
    def get_fgpct(self) -> float:
        """Returns the field goal percentage"""
        return self.total_shots_made/self.total_shots if self.total_shots != 0 else 0
    
    def get_3pa(self) -> int:
        """Returns the number of three pointers attempted"""
        return self.total_3s
    
    def get_3pm(self) -> int:
        """Returns the number of three pointers made"""
        return self.total_3s_made
    
    def get_3ppct(self) -> float:
        """Returns the three pointer percentage"""
        return self.total_3s_made/self.total_3s if self.total_3s != 0 else 0