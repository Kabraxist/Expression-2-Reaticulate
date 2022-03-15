import untangle, csv
from pathlib import Path, PurePath

class ArticulationBank:
    def __init__(self, source_file_path) -> None:
        self.root = untangle.parse(source_file_path)
        self.articulation_list = []
        self.bank_group = "Converted Maps"
        self.bank_name = [i['value'] for i in self.root.InstrumentMap.string if i['name'] == "name"][0]
        self.ParseArticulations()    

    def GenerateHeader(self):
        header = f'//! g="Converted Maps" n="{self.bank_group}"\nBank * * {self.bank_name}\n'
        return header

    def GenerateArticulations(self):
        articulations = ""
        for art in self.articulation_list:
            articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{art.art_progchange} {art.art_name}\n'
        
        return articulations
            
    def ParseArticulations(self):
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

class FileOps:
    expression_maps = []

    def ExportReabank(content, map):
        export_path = PurePath(Path.cwd(), "Reabank Export", map.relative_to(Path.cwd()).with_suffix(".reabank"))

        Path(export_path.parent).mkdir(parents=True, exist_ok=True)

        file = open(Path(export_path), "w")
        file.write(content)
        file.close()

    def ConvertExpressionMaps():
        for map in FileOps.expression_maps:
            bank = ArticulationBank(str(map))
            result = bank.GenerateHeader() + bank.GenerateArticulations()

            FileOps.ExportReabank(result, map)

    def FindExpressionMaps():
        FileOps.expression_maps = sorted(Path.cwd().rglob('*.expressionmap'))

FileOps.FindExpressionMaps()
FileOps.ConvertExpressionMaps()