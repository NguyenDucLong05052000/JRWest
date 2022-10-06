from data_structures import *
from read_data import LIST_EVENT_TRAIN_DOWN,LIST_EVENT_TRAIN_UP,LIST_EVENT_TRAIN_SAHO_DOWN,LIST_EVENT_TRAIN_SAHO_UP,LIST_EVENT_OPEN_TRACK_STATION,LIST_EVENT_ROLLING_STOCK,LIST_EVENT_STATION_TRACK,LIST_TRAIN_UP,LIST_TRAIN_DOWN,LIST_TRAIN_SAHO_DOWN,LIST_TRAIN_SAHO_UP,LIST_STATIONS,LIST_TRAIN_SET
import datetime

ACTIVITY_TRAIN =[]
ACTIVITY_OPEN_TRACK_STATION = []
ACTIVITY_STATION_TRACK = []
ACTIVITY_ROLLING_STOCK = []

def string_to_intTime(str_time):
    time =''
    format = "%H:%M:%S"
    if(str_time[0:2]=='0:' or str_time[0:2]=='1:'):
        time = datetime.datetime.strptime(str_time,format)+datetime.timedelta(days=25568)
    else:
        time = datetime.datetime.strptime(str_time,format)+datetime.timedelta(days=25567)
    time = int(time.timestamp())
    return time

def intTime_to_string(intTime):
    a = str(datetime.datetime.fromtimestamp(intTime))[11:]
    if(a[0]=='0'):
        a = a[1:]
    return a

class Network:

    graph ={}
    def build_Activity(self):
        # Xay dung cac activity train
        LIST_EVENT_TRAIN = LIST_EVENT_TRAIN_DOWN + LIST_EVENT_TRAIN_UP + LIST_EVENT_TRAIN_SAHO_DOWN + LIST_EVENT_TRAIN_SAHO_UP
        for i in LIST_EVENT_TRAIN:
            self.graph[i] = []
            if(i in LIST_EVENT_TRAIN_DOWN):
                for j in LIST_EVENT_TRAIN_DOWN:
                    if(i.train == j.train and i.station == j.station and i.type == 'ARR' and j.type == 'DPT'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
                    if(i.train == j.train and i.type == 'DPT' and j.type == 'ARR' and i.station.right_station.station_id==j.station.station_id):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)

            if(i in LIST_EVENT_TRAIN_UP):
                for j in LIST_EVENT_TRAIN_UP:
                    if(i.train == j.train and i.station == j.station and i.type == 'ARR' and j.type =='DPT'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
                    if(i.train == j.train and i.type == 'DPT' and j.type == 'ARR' and i.station.left_station.station_id==j.station.station_id):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)

            if(i in LIST_EVENT_TRAIN_SAHO_DOWN):
                for j in LIST_EVENT_TRAIN_SAHO_DOWN:
                    if(i.train == j.train and i.station.station_id =='WAREHOUSE' and i.type == 'DPT' and j.station.station_id =='U' and j.type =='ARR'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)                    
                    if(i.train == j.train and i.station.station_id == j.station.station_id and i.type=='ARR' and  j.type =='DPT'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
                    if(i.train==j.train and i.station.station_id =='U' and i.type =='DPT' and j.station.station_id=='V' and j.type=='ARR'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)

            if(i in LIST_EVENT_TRAIN_SAHO_UP):
                for j in LIST_EVENT_TRAIN_SAHO_UP:
                    if(i.train==j.train and i.station.station_id =='V' and j.station.station_id =='U' and i.type == 'DPT' and j.type == 'ARR'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
                    if(i.train == j.train and i.station.station_id == j.station.station_id and i.type == 'ARR' and j.type == 'DPT'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
                    if(i.train == j.train and i.station.station_id =='U' and i.type == 'DPT' and j.station.station_id =='WAREHOUSE' and j.type == 'ARR'):
                        self.graph[i].append(j)
                        tmp = Activity(i,j)
                        ACTIVITY_TRAIN.append(tmp)
        with open("./file_write/Activity_event_train.txt",'w') as f:
            for i in ACTIVITY_TRAIN:
                f.write("Station: {} - Train: {} - Time: {} - Type: {}====================>". format(i.head.station.station_id, i.head.train.train_id,i.head.time, i.head.type))
                f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))
            print("DONE ACTIVITY EVENT TRAIN")
        # Xay dung cac activity open track station
        
        # xay dung cac event_open_track noi vao event_dpt
        for i in LIST_EVENT_OPEN_TRACK_STATION:

            self.graph[i] = []
            for j in self.graph:
                if(j in LIST_EVENT_TRAIN):

                    if(j.station.station_id == i.stationHead.station_id and j.type == 'DPT'):
                        for k1 in self.graph[j]:
                            if(k1.station.station_id == i.stationTail.station_id and k1.type =='ARR'):
                                self.graph[i].append(j)
                                tmp = Activity(i,j)
                                ACTIVITY_OPEN_TRACK_STATION.append(tmp)

                    if(j.station.station_id == i.stationTail.station_id and j.type == 'DPT'):
                        for k2 in self.graph[j]:
                            if(k2.station.station_id == i.stationHead.station_id and k2.type =='ARR'):
                                self.graph[i].append(j)
                                tmp=Activity(i,j)
                                ACTIVITY_OPEN_TRACK_STATION.append(tmp)
        
        # xay dung cac event dpt noi vao cac event dpt va cac event arr noi vao cac event arr va dpt tren cung 1 ga
        
        for i in LIST_STATIONS:
            for j1 in LIST_EVENT_TRAIN:
                if(j1.station.station_id == i.station_id and j1.type == 'DPT'):
                    for j2 in LIST_EVENT_TRAIN:
                        if(j2.station.station_id == j1.station.station_id and j2.type =='DPT' and string_to_intTime(j2.time)>string_to_intTime(j1.time)):
                            self.graph[j1].append(j2)
                            tmp=Activity(j1,j2)
                            ACTIVITY_OPEN_TRACK_STATION.append(tmp)
                if(j1.station.station_id == i.station_id and j1.type=='ARR'):
                    for j2 in LIST_EVENT_TRAIN:
                        if(j2.station.station_id == j1.station.station_id and string_to_intTime(j2.time)>string_to_intTime(j1.time)):
                            self.graph[j1].append(j2)
                            tmp=Activity(j1,j2)
                            ACTIVITY_OPEN_TRACK_STATION.append(tmp)

        with open("./file_write/Activity_Opentrack_Station.txt",'w') as f:
            for i in ACTIVITY_OPEN_TRACK_STATION:
                if(i.head in LIST_EVENT_OPEN_TRACK_STATION):
                    f.write("StationHead: {} - StationTail: {} - Capacity: {} ================>".format(i.head.stationHead.station_id,i.head.stationTail.station_id,i.head.capacity))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))
                else:
                    f.write("Station: {} - Train: {} - Time: {} - Type: {} =================>". format(i.head.station.station_id, i.head.train.train_id,i.head.time, i.head.type))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))

        print("DONE ACTIVITY OPEN TRACK STATION")
        # Xay dung cac activity station track

        #xay dung cac event station noi vao cac event ARR trong 1 ga 
        for i in LIST_EVENT_STATION_TRACK:
            self.graph[i]=[]
            for j1 in LIST_EVENT_TRAIN:
                if(j1.station.station_id == i.station.station_id and j1.type =='ARR'):
                    self.graph[i].append(j1)
                    tmp = Activity(i,j1)
                    ACTIVITY_STATION_TRACK.append(tmp)
        # xay dung cac event DPT noi vao cac event ARR cua 1 tau khac trong 1 ga
        for i in LIST_STATIONS:
            for j1 in LIST_EVENT_TRAIN:
                if(j1.station.station_id == i.station_id and j1.type =='DPT'):
                    for j2 in LIST_EVENT_TRAIN:
                        if(j2.station.station_id == j1.station.station_id and j2.type=='ARR' and string_to_intTime(j2.time)>string_to_intTime(j1.time)):
                            self.graph[j1].append(j2)
                            tmp = Activity(j1,j2)
                            ACTIVITY_STATION_TRACK.append(tmp)

        with open("./file_write/Activity_Station_Track.txt",'w') as f:
            for i in ACTIVITY_STATION_TRACK:
                if(i.head in LIST_EVENT_STATION_TRACK):
                    f.write("Station: {} - Capacity: {}============>".format(i.head.station.station_id, i.head.capacity))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))
                else:
                    f.write("Station: {} - Train: {} - Time: {} - Type: {} =================>". format(i.head.station.station_id, i.head.train.train_id,i.head.time, i.head.type))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))               
        print("DONE ACTIVITY STATION TRACK")

        # xay dung cac activity rolling stock
        
        # xay dung cac event rolling stock noi vao cac event DPT tai tung ga
        for i in LIST_EVENT_ROLLING_STOCK:
            self.graph[i] = []
            for j in LIST_EVENT_TRAIN:
                if(j.station.station_id == i.station.station_id and j.type =='DPT'):
                    self.graph[i].append(j)
                    tmp = Activity(i,j)
                    ACTIVITY_ROLLING_STOCK.append(tmp)
        
        for i in LIST_TRAIN_SET:
            for j1 in LIST_EVENT_TRAIN:
                if(j1.train.train_id == i[0] and j1.station.station_id == i[1] and j1.type=='ARR'):
                    for j2 in LIST_EVENT_TRAIN:
                        if(j2.train.train_id == i[2] and j2.station.station_id == i[1] and j2.type =='DPT'):
                            self.graph[j1].append(j2)
                            tmp = Activity(j1,j2)
                            ACTIVITY_ROLLING_STOCK.append(tmp)
        with open("./file_write/Activity_rollingstock.txt",'w') as f:
            
            for i in ACTIVITY_ROLLING_STOCK:
                if(i.head in LIST_EVENT_ROLLING_STOCK):
                    f.write("Station: {} - Capacity: {}============>".format(i.head.station.station_id,i.head.capacity))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))
                else:
                    f.write("Station: {} - Train: {} - Time: {} - Type: {} =============>".format(i.head.station.station_id,i.head.train.train_id,i.head.time, i.head.type))
                    f.write("Station: {} - Train: {} - Time: {} - Type: {}\n". format(i.tail.station.station_id, i.tail.train.train_id,i.tail.time, i.tail.type))
        print("DONE ACTIVITY ROLLING STOCK")

        return self.graph

a = Network()
GRAPH = a.build_Activity()



