import untangle, csv
from pathlib import Path

class ArticulationBank:
    def __init__(self, source_file_path) -> None:
        self.root = untangle.parse(source_file_path)
        self.articulation_list = []
        self.bank_group = "Converted Maps"
        self.bank_name = [i['value'] for i in self.root.InstrumentMap.string if i['name'] == "name"][0]        

    def GenerateHeader(self):
        header = f'//! g="Converted Maps" n="{self.bank_group}"\nBank * * {self.bank_name}\n'
        return header

    def GenerateArticulations(self):
        articulations = ""
        for art in self.articulation_list:
            articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{art.art_progchange} {art.art_name}\n\n'
        
        print(articulations)
            

    def GatherArticulations(self):
        for slot in self.root.InstrumentMap.member[1].list.obj:
            art = Articulation()

            for member in slot.member:
                if member["name"] == "name": # Get articulation name and generate other values
                    if(member.string["value"] != ''):
                        art.art_name = member.string["value"]
                        art.art_progchange, art.art_color, art.art_icon = UACCList.FindUACC(art.art_name)
                        self.articulation_list.append(art)
                
            for obj in slot.obj: # Action assignment
                if (obj["class"] == "PSlotMidiAction"):
                    key = -1

                    note_changer = [i for i in obj.member if i["name"] == "noteChanger"][0]
                    
                    for i in note_changer.list.obj.int:
                        if (i["name"] == "key"):
                            key = i["value"]
                    
                    if (key < 0):
                        key = [i["value"] for i in obj.int if i["name"] == "key"][0]
                    
                    if (int(key) > 0):
                        art.art_action = f'note:{key}'

class Articulation:
    def __init__(self) -> None:
        self.art_progchange = 0
        self.art_name = ""
        self.art_color = ""
        self.art_icon = ""
        self.art_action = ""        

class UACCList:
    uacc_file = open('UACC List.csv', 'r')
    reader = csv.DictReader(uacc_file, ["id", "color", "icon"], "names")

    def FindUACC(art_name):
        pc, color, icon = "127", "default", "note-quarter"

        for i in UACCList.reader:
            if (art_name != '' and art_name in i["names"]):
                pc, color, icon = i["id"], i["color"], i["icon"]
            else:
                pass
        
        UACCList.uacc_file.seek(0)
        return pc, color, icon

path = input("Please insert full path...")

art_bank = ArticulationBank(path)
art_bank.GatherArticulations()
art_bank.GenerateArticulations()

#file = open(folder_path+filename+".reabank", "w")
#file.write(GenerateHeader() + GenerateArticulations())
#file.close()

#print("File must be generated?")
#input("Press any key to exit...")