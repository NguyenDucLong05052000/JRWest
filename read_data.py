from data_structures import Event_Train,Track,Station,Event_StationTrack,Event_RollingStock,Event_OpenTrackStation,Train
import csv
import pandas as pd

class preprocess_data:

    list_event_open_track_station = []
    list_event_station_track = []
    list_event_rolling_stock = []
    list_stations = []
    list_tracks = []
    list_train_set = []

    def __init__(self):
        self.msg = ""

    def read_station(self,link_csv,file_write_stationTrack_info):
        with open(link_csv) as f:
            reader = csv.reader(f)
            list = [row for row in reader]
            list.remove(list[0])
            for i in list:
                station_id = i[0]
                track_id = i[1]
                allow_from_down = i[2]
                allow_out_down = i[3]
                allow_from_up = i[4]
                allow_out_up = i[5]
                tmp = Track(station_id,track_id,allow_from_down,allow_out_down,allow_from_up,allow_out_up)
                self.list_tracks.append(tmp)
        stations = pd.read_csv(link_csv)['station'].unique()
        stationss = []
        for i in stations:
            stationss.append(i)
        stations = stationss
        
        for s in range(len(stations)):
            tracks = []
            for track in self.list_tracks:
                if(track.station_id == stations[s]):
                    tracks.append(track)
            tmp = Station(stations[s],tracks)
            self.list_stations.append(tmp)
    
        for s1 in self.list_stations:
            s_id = s1.station_id
            if(s_id=='A'):
                s_id_right = 'B'
                for s2 in self.list_stations:
                    if(s2.station_id == s_id_right):
                        s1.right_station = s2
            elif(s_id=='V'):
                s_id_left = 'U'
                for s2 in self.list_stations:
                    if(s2.station_id == s_id_left):
                        s1.left_station = s2
            elif(s_id=='WAREHOUSE'):
                s_id_next = 'U'
                for s2 in self.list_stations:
                    if(s2.station_id==s_id_next):
                        s1.next_station = s2
                        s2.next_station = s1
            else:
                s_id_index = stations.index(s_id)
                s_id_right = stations[s_id_index+1]
                s_id_left = stations[s_id_index-1]
                for s2 in self.list_stations:
                    if(s2.station_id == s_id_right):
                        s1.right_station = s2
                    if(s2.station_id == s_id_left):
                        s1.left_station = s2
                  
        with open(file_write_stationTrack_info,'w') as f:
            for i in self.list_stations:
                f.write("{}\n".format(i.station_id))
                for j in i.tracks:
                    f.write("{}".format(j.allow_from_up))
                    f.write("{}".format(j.allow_from_down))
                    f.write("{}".format(j.allow_out_up))
                    f.write("{}".format(j.allow_out_down))
                    f.write("\n")
        return self.list_stations
    
    def read_train(self,link_csv,file_write_read_train):
        list_train = []
        with open(link_csv) as f:
            reader = csv.reader(f)
            l =[row for row in reader]
            list_train = l[0]
            list_train.remove(list_train[0])
            list_train.remove(list_train[0])
        if(link_csv=='./phase2_data/UpTime.csv' or link_csv=='./phase2_data/SahoUP.csv'):
            direction = 0
        elif(link_csv=='./phase2_data/DownTime.csv' or link_csv=='./phase2_data/SahoDOWN.csv'):
            direction = 1

        list = []
        for i in list_train:
            if(i[0]!='回'):
                number = int(i[0:-1])
                if(number >= 600 and number <=1700):
                    type = 0
                elif(number >1700 and number <= 2700):
                    type = 1
                elif(number > 2700 and number <3650):
                    type = 2
                elif(number >=3650):
                    type = 3
            else:
                number = int(i[1:-1])
                if(number >= 600 and number <=1700):
                    type = 0
                elif(number >1700 and number <= 2700):
                    type = 1
                elif(number > 2700 and number <3650):
                    type = 2
                elif(number >=3650):
                    type = 3
            tmp = Train(i,type,direction)
            list.append(tmp)

        with open(file_write_read_train,'w') as f:
            for i in list:
                f.write("================================\n")
                f.write("{}\n".format(i.train_id))
                f.write("{}\n".format(i.direction))
                f.write("{}\n".format(i.type))
        return list

    def read_event_train(self,link_csv,file_write_event_train):

        # Danh sach cac tau

        list_train_up =self.read_train('./phase2_data/UpTime.csv','./file_write/List_train_up.txt')
        list_train_down = self.read_train('./phase2_data/DownTime.csv','./file_write/List_train_down.txt')
        list_train_saho_up = self.read_train('./phase2_data/SahoUP.csv','./file_write/List_train_saho_up.txt')
        list_train_saho_down = self.read_train('./phase2_data/SahoDOWN.csv','./file_write/List_train_saho_down.txt')

        list_trains = list_train_up+list_train_down+list_train_saho_down+list_train_saho_up
        list_event_train = []
        with open(link_csv) as f:
            reader = csv.reader(f)
            list = [row for row in reader]
            list_train = []
            list[0].remove(list[0][0])
            list[0].remove(list[0][0])
            for i in list[0]:
                list_train.append(i)
            list.remove(list[0])
            
            for i in list:
                station = i[0]
                for k in self.list_stations:
                    if(station==k.station_id):
                        station = k
                type = i[1]
                count = 0
                for j in range(2,len(i)):
                    time = i[j]
                    #train = list_train[count]
                    for k in list_trains:
                        if(list_train[count]==k.train_id):
                            train = k
                    count+=1
                    if(time !=''):
                        tmp = Event_Train(train,time,station,type)
                        if(file_write_event_train =='./file_write/Event_Train_Up.txt' or file_write_event_train =='./file_write/Event_Train_SAHO_up.txt'):
                            tmp.direction = 0
                        else:
                            tmp.direction = 1
                        list_event_train.append(tmp)            

        with open(file_write_event_train,'w') as f:
            for i in list_event_train:
                f.write("====================================\n")
                f.write("{}\n".format(i.time))
                f.write("{}\n".format(i.station.station_id))
                f.write("***\n")
                f.write("{}\n".format(i.train.train_id))
                f.write("{}\n".format(i.train.direction))
                f.write("{}\n".format(i.train.type))
                f.write("***\n")                
                f.write("{}\n".format(i.type))
        return list_event_train

    def read_event_station_track(self,file_write_event_station_track):
        for i in self.list_stations:
            station = i
            capacity = len(i.tracks)
            tmp = Event_StationTrack(station,capacity)
            tmp.event_station_left = i.left_station
            tmp.event_station_right = i.right_station
            if(i.next_station != None):
                tmp.event_station_next = i.next_station
            self.list_event_station_track.append(tmp)
        
        with open(file_write_event_station_track,'w') as f:
            for i in self.list_event_station_track:
                if(i.station.station_id=='A'):
                    f.write("=========================\n")
                    f.write("{}\n".format(i.station.station_id))
                    f.write("{}\n".format(i.capacity))
                    f.write("Ga ben phai la: {}\n".format(i.event_station_right.station_id))
                elif(i.station.station_id=='V'):
                    f.write("=========================\n")
                    f.write("{}\n".format(i.station.station_id))
                    f.write("{}\n".format(i.capacity))
                    f.write("Ga ben trai la: {}\n".format(i.event_station_left.station_id))
                elif(i.station.station_id=='WAREHOUSE'):
                    f.write("=========================\n")
                    f.write("{}\n".format(i.station.station_id))
                    f.write("{}\n".format(i.capacity))
                    f.write("Ga ben canh la: {}\n".format(i.event_station_next.station_id))
                elif(i.station.station_id=='U'):
                    f.write("=========================\n")
                    f.write("{}\n".format(i.station.station_id))
                    f.write("{}\n".format(i.capacity))
                    f.write("Ga ben canh la: {}\n".format(i.event_station_next.station_id))
                    f.write("Ga ben phai la: {}. Ga ben trai la: {}\n".format(i.event_station_right.station_id,i.event_station_left.station_id))
                else:
                    f.write("=========================\n")
                    f.write("{}\n".format(i.station.station_id))
                    f.write("{}\n".format(i.capacity))
                    f.write("Ga ben phai la: {}. Ga ben trai la: {}\n".format(i.event_station_right.station_id,i.event_station_left.station_id))
                for j in i.station.tracks:
                    f.write("{}".format("{} ".format(j.track_id)))
                    f.write("{}".format(j.allow_from_up))
                    f.write("{}".format(j.allow_from_down))
                    f.write("{}".format(j.allow_out_up))
                    f.write("{}".format(j.allow_out_down))
                    f.write("\n")
        return self.list_event_station_track
    
    def read_event_open_track_station(self,link_csv,file_write_event_open_track_station):
        with open(link_csv) as f:
            reader = csv.reader(f)
            list_event = [row for row in reader]
            list_event.remove(list_event[0])
            for i in list_event:
                stationHead = None
                stationTail = None
                for j in self.list_stations:
                    if(j.station_id == i[0]):
                        stationHead = j
                    if(j.station_id == i[1]):
                        stationTail = j
                capacity = i[2]
                tmp = Event_OpenTrackStation(stationHead,stationTail,capacity)
                self.list_event_open_track_station.append(tmp)
        
        with open(file_write_event_open_track_station,'w') as f:
            for i in self.list_event_open_track_station:
                f.write("=========================\n")
                f.write("StationHead:{} \n".format(i.stationHead.station_id))
                f.write("StationTail: {} \n".format(i.stationTail.station_id))
                f.write("capacity:{} \n".format(i.capacity))
        return self.list_event_open_track_station

    def read_event_rollingstock(self,link_csv,file_write_event_rollingstock):
        with open(link_csv) as f:
            reader = csv.reader(f)
            list_event = [row for row in reader]
            list_event.remove(list_event[0])
            for i in list_event:
                station = i[0]
                capacity = i[1]
                for j in self.list_stations:
                    if(i[0] == j.station_id):
                        station = j
                tmp = Event_RollingStock(station,capacity)
                self.list_event_rolling_stock.append(tmp)

        with open(file_write_event_rollingstock,'w') as f:
            for i in self.list_event_rolling_stock:
                f.write("=============================\n")
                f.write("Ga {}\n".format(i.station.station_id))
                f.write("Capacity: {}\n".format(i.capacity))
                for j in i.station.tracks:
                    f.write("{}".format("{} ".format(j.track_id)))
                    f.write("{}".format(j.allow_from_up))
                    f.write("{}".format(j.allow_from_down))
                    f.write("{}".format(j.allow_out_up))
                    f.write("{}".format(j.allow_out_down))
                    f.write("\n")

        return self.list_event_rolling_stock

    def read_train_set(self,link_csv):
        with open(link_csv) as f:
            reader = csv.reader(f)
            self.list_event = [row for row in reader]
            self.list_event.remove(self.list_event[0])
            return self.list_event

#if __name__=="__main__":
a = preprocess_data()
# Danh sach cac tau
LIST_TRAIN_UP = a.read_train('./phase2_data/UpTime.csv','./file_write/List_train_up.txt')
LIST_TRAIN_DOWN = a.read_train('./phase2_data/DownTime.csv','./file_write/List_train_down.txt')
LIST_TRAIN_SAHO_UP = a.read_train('./phase2_data/SahoUP.csv','./file_write/List_train_saho_up.txt')
LIST_TRAIN_SAHO_DOWN = a.read_train('./phase2_data/SahoDOWN.csv','./file_write/List_train_saho_down.txt')

# Danh sach cac ga
LIST_STATIONS = a.read_station('./phase2_data/Track.csv','./file_write/StationTrack_info.txt')
LIST_TRAIN_SET = a.read_train_set("./phase2_data/TrainSet.csv")

# Danh sach cac event_train
LIST_EVENT_TRAIN_UP = a.read_event_train('./phase2_data/UpTime.csv','./file_write/Event_Train_Up.txt')
LIST_EVENT_TRAIN_DOWN = a.read_event_train('./phase2_data/DownTime.csv','./file_write/Event_Train_Down.txt')
LIST_EVENT_TRAIN_SAHO_UP = a.read_event_train('./phase2_data/SahoUP.csv','./file_write/Event_Train_SAHO_up.txt')
LIST_EVENT_TRAIN_SAHO_DOWN = a.read_event_train('./phase2_data/SahoDOWN.csv','./file_write/Event_Train_SAHO_down.txt')

# Danh sach cac event station track
LIST_EVENT_STATION_TRACK = a.read_event_station_track('./file_write/Event_Station_Track.txt')

# Danh sach cac event open track station
LIST_EVENT_OPEN_TRACK_STATION = a.read_event_open_track_station('./phase2_data/opentrack.csv','./file_write/Event_Open_Track_Station.txt')

# Danh sach cac event rolling stock
LIST_EVENT_ROLLING_STOCK = a.read_event_rollingstock('./phase2_data/Rollingstock.csv','./file_write/Event_Rollingstock.txt')




