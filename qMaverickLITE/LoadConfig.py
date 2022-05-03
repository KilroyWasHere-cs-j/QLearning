import os
import xml.etree.ElementTree as ET


def get_local_path():
    return os.getcwd()


class loader:

    def __init__(self):
        #/home/gabriel/PycharmProjects/QLearning/qMaverickLITE/details.xml
        self.mytree = ET.parse(get_local_path() + "/details.xml")
        self.myroot = self.mytree.getroot()

    # Get the models meta data
    def get_meta_data(self):
        results = []
        for m in self.myroot[0]:
            results.append(m.text)
        return results

    # Get the data for the Q Learning model
    def get_Q(self):
        results = []
        for x in self.myroot[1]:
            results.append(float(x.text))
            # print(x.tag, x.text)
        return results

    # Get the enviorment data
    def get_enviorment(self):
        results = []
        for j in self.myroot[2]:
            results.append(int(j.text))
            # print(j.tag, j.text)
        return results

