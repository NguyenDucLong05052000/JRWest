class Event:
    id = None
    indegree = None
    outdegree = None
    in_arcs = None
    out_arcs = None
    a_track_in = None
    a_track_out = None
    a_station_in = None
    a_station_out = None
    a_rollingstock_in = None
    a_rollingstock_out = None
    
    def __init__(self):
        self.msg = ""
        
class Event_Train(Event):
    train = None
    time = None
    station = None
    type = None # DPT, ARR  
    direction = None # 0 - Up , 1 - Down
    def __init__(self,train,time,station,type):
        self.train = train
        self.time = time
        self.station = station
        self.type = type
        #self.maximum_delay_time = maximum_delay_time
class Event_OpenTrackStation(Event):
    stationHead = None
    stationTail = None
    capacity = None
    
    def __init__(self,stationHead,stationTail,capacity):
        self.stationHead = stationHead
        self.stationTail = stationTail
        self.capacity = capacity
    
class Event_StationTrack(Event):
    event_station_right = None
    event_station_left = None
    event_station_next = None
    station = None
    capacity = None

    def __init__(self,station,capacity):
        self.station = station
        self.capacity = capacity

class Event_RollingStock(Event):
    station = None
    capacity = None

    def __init__(self,station,capacity):
        self.station = station
        self.capacity = capacity

class Activity:
    head = None         
    tail = None
    
    def __init__(self,head,tail):
        self.head = head 
        self.tail = tail
         

class Train:
    train_id = None
    direction = None # 0 - up, 1 - down
    type = None # 0 - local, 1 - rapid miyakoji(26xx) , 3 - rapid(36xx), 4 - section rapid(365x)
    predecessor = None
    successor = None
    def __init__(self,train_id, type, direction):
        self.train_id = train_id
        self.type = type
        self.direction = direction

class Station:
    station_id = None
    tracks = None
    left_station = None
    right_station = None 
    isTurnAround = None
    isShuntingYard = None
    next_station = None
    def __init__(self,id,tracks):
        self.station_id = id
        self.tracks = tracks
class Track:
    track_id = None
    track_direction = None # 0 - up , 1 - down 
    allow_from_up = None
    allow_from_down = None
    allow_out_up = None
    allow_out_down = None
    def __init__(self,station_id,track_id,allow_from_down,allow_out_down,allow_from_up,allow_out_up):
        self.station_id = station_id
        self.track_id = track_id
        self.allow_from_up = allow_from_up
        self.allow_from_down = allow_from_down
        self.allow_out_up = allow_out_up
        self.allow_out_down = allow_out_down

