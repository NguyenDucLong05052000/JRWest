from ortools.linear_solver import pywraplp

from network import ACTIVITY_OPEN_TRACK_STATION, ACTIVITY_ROLLING_STOCK, ACTIVITY_STATION_TRACK, ACTIVITY_TRAIN
from read_data import LIST_TRAIN_DOWN, LIST_TRAIN_SAHO_DOWN, LIST_TRAIN_SAHO_UP, LIST_TRAIN_UP

LIST_TRAIN = LIST_TRAIN_UP + LIST_TRAIN_DOWN + LIST_TRAIN_SAHO_UP + LIST_TRAIN_SAHO_DOWN
ACTIVITY_INVENTORY = ACTIVITY_OPEN_TRACK_STATION + ACTIVITY_ROLLING_STOCK + ACTIVITY_STATION_TRACK
LIST_ACTIVITY = ACTIVITY_OPEN_TRACK_STATION + ACTIVITY_STATION_TRACK + ACTIVITY_ROLLING_STOCK + ACTIVITY_TRAIN

def ILP(solver_library):
    solver = pywraplp.Solver.CreateSolver(solver_library)
    if not solver:
        return
    
    x = {}
    for i in range(len(LIST_TRAIN)):
        x[i] = solver.BoolVar('x[{}]'.format(LIST_TRAIN[i].train_id))
        #x[i] = solver.BoolVar()

    z = {}
    for a in range(len(LIST_ACTIVITY)):
        z[a] = solver.BoolVar('z[{}]'.format(LIST_ACTIVITY[i]))
    y_t_e ={}
    #for i in range(len())
        
    for i in range(len(x)):
        print(type(x[i]))
ILP('GLOP')