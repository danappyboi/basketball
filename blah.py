from data_manager import Data_Manager
from shot import Shot

dm = Data_Manager()
shot1 = Shot(1, 3, True, 1)
shot2 = Shot(2, 3, True, 2)
shot3 = Shot(1, 3, True, 3)

dm.add_shot(shot1)
dm.add_shot(shot2)
dm.add_shot(shot1)

print(dm.get_shots())