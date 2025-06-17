# Little mental note for me: My mentality here is get everything from
# the data.csv file, no internal data structure to hold all the data. I don't
# know if that's the best idea but if I have to update the csv everytime anyway, 
# it doesn't make sense to keep track of two different references to the same
# info v(._.)v

# When I come up with a better/faster method, I'll use that but for now this is
# what I'm stuck with

import csv
from shot_managing.shot import Shot, to_Shot
from shot_managing.analysis import Analysis

#TODO: should be able to handle multiple sheets; 
# maybe combine dms? make self.data a list?
class Data_Manager:
    def __init__(self):
        self.data = "data.csv"
        self.anal = Analysis()
        self.anal.add_data(self.data)
        self.shots = self.__get_shots_from_data()
        self.scale_x = 1000
        self.scale_y = 1000

    def add_shot(self, shot : Shot):
        """Adds shots to the data."""
        self.anal.add_shot(shot)
        print(self.anal.stats());
        with open(self.data, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(shot.to_data())
        
    def get_shots(self):
        """Returns a list of all the shots."""
        return self.__get_shots_from_data()
    
    def get_analysis(self) -> Analysis:
        """Gets analytical data from the data mananger"""
        return self.anal

    #TODO: doesn't work - best solution is csv -> list -> remove -> csv
    def __remove_shot(self, shot: Shot):
        """Removes a shot from the data."""
        if shot in self.shots:
            self.shots.remove(shot)
            with open(self.data, "r") as read:
                with open(self.data, "w") as writ:
                    reader = csv.reader(read)
                    writer = csv.writer(writ)
                    for row in reader:
                        if to_Shot(row) == shot:
                            writer.writerow(row)
                            break
            
    def __get_shots_from_data(self):
        """Private function to grab the shot data from
        the data.txt file."""
        shots = []
        with open(self.data, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                shots.append(to_Shot(row))
        return shots   


header = "FGM, FGA, FG%, 3PM, 3PA, 3P%\n"