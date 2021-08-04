import json

class Data_Manager():
    def __init__(self,app):
        self.app = app
        self.user_data = []

    # switch data
    def switch(self):
        self.user_data = self.app.renderer.schedule.day_type.days_data

    # delete a event
    def delete(self,i,event):
        self.switch()
        self.user_data[i].remove(self.user_data[i][event])
        


    # write file
    def write(self,path):
        self.switch()
        json_data = {
        'user_data':self.user_data
        }
        f = open(path, 'w')
        f.write(json.dumps(json_data))
        f.close()

    # load file
    def load(self,path):
        f = open(path, 'r')
        dat = f.read()
        f.close()
        json_dat = json.loads(dat)
        self.user_data = json_dat['user_data']
        return self.user_data
