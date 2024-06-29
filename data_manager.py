import csv
from shot import Shot, to_Shot

class Data_Manager:
    def __init__(self):
        self.data = "data.csv"
        self.shots = self.__get_shots_from_data()

    def add_shot(self, shot : Shot):
        self.shots.append(shot)
        with open(self.data, "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(shot.to_data())
        
    def get_shots(self):
        return self.shots
    
    #TODO: doesn't work
    def remove_shot(self, shot: Shot):
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