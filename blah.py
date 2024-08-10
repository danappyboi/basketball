from data_manager import Data_Manager
from shot import Shot
from gui import run_gui

dm = Data_Manager()
# shot1 = Shot(24, 100, False, 1)
# shot2 = Shot(75, 250, False, 2)
# shot3 = Shot(-100, 42, False, 3)
# dm.add_shot(shot1)
# dm.add_shot(shot2)
# dm.add_shot(shot3)

run_gui(dm)

