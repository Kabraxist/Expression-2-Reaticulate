import untangle, csv, difflib, plistlib, time, sys, os
import xml.etree.ElementTree as ET
from pathlib import Path, PurePath

os.chdir(sys.path[0]) # Set CWD to current path

class ArticulationBank:
    merged_result = ""

    def __init__(self, source_file_path) -> None:
        self.root = untangle.parse(source_file_path)
        self.rootXML = ET.parse(source_file_path)
        self.articulation_list = []
        self.bank_group = Path(*(Path.relative_to(Path(source_file_path), Path.cwd()).parts[1:-1]))
        self.bank_name = [i['value'] for i in self.root.InstrumentMap.string if i['name'] == "name"][0]
        self.ParseArticulations()    

    def GenerateHeader(self):
        header = f'//! g="{self.bank_group}" n="{self.bank_name}"\nBank * * {self.bank_name}\n'
        ArticulationBank.merged_result += header
        return header

    def GenerateArticulations(self):
        articulations = ""
        for i, art in enumerate(self.articulation_list):
            if (art.art_action is not None):
                ## Temp fix for overlapping Prog Changes
                ## articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{art.art_progchange} {art.art_name}\n'
                articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{i+1} {art.art_name}\n'
        
        ArticulationBank.merged_result += articulations + "\n"
        return articulations
            
    def ParseArticulations(self):
        
        # dot is root, rest finds the first item unless checked with bracket queries
        for sound_slot in self.rootXML.find("./member/[@name = 'slots']/list"):
            art = Articulation()
            art.art_name = sound_slot.find("./member/[@name = 'name']/string").attrib["value"]
            art.art_progchange, art.art_color, art.art_icon = UACCList.FindUACC(art.art_name)
            self.articulation_list.append(art)

            for output_event in sound_slot.findall(".//*[@class = 'POutputEvent']"):
                status = output_event.find("./int/[@name = 'status']").attrib["value"]
                data1 = output_event.find("./int/[@name = 'data1']").attrib["value"]
                data2 = output_event.find("./int/[@name = 'data2']").attrib["value"]

                actions = []

                if (status == "144"):
                    actions.append(f"note:{data1},{data2}")
                
                if (status == "176"):
                    actions.append(f"cc:{data1},{data2}")

                art.art_action = "/".join(actions)

class ArticulationBankPlist:
    def __init__(self, source_file_path) -> None:
        self.root = plistlib.load(open(source_file_path, 'rb'))
        self.articulation_list = []
        self.bank_group = "Converted Maps"
        self.bank_name = self.root['Name'].replace('.plist', '')
        self.ParseArticulations()

    def GenerateHeader(self):
        header = f'//! g="{self.bank_group}" n="{self.bank_name}"\nBank * * {self.bank_name}\n'
        ArticulationBank.merged_result += header
        return header
        pass

    def GenerateArticulations(self):
        articulations = ""
        for i, art in enumerate(self.articulation_list):
            if (art.art_action is not None):
                ## Temp fix for overlapping Prog Changes
                ## articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{art.art_progchange} {art.art_name}\n'
                articulations += f'//! c={art.art_color} i={art.art_icon} o={art.art_action}\n{i+1} {art.art_name}\n'
        
        ArticulationBank.merged_result += articulations + "\n"
        return articulations

    def ParseArticulations(self):
        for slot in self.root['Articulations']:
            art = Articulation()
            art.art_name = slot['Name']
            art.art_progchange, art.art_color, art.art_icon = UACCList.FindUACC(art.art_name)

            action = ''

            try:
                action = f'note:' + str(slot['Output']['MB1'])
            except:
                for act in slot['Output']:
                    if action != '': action += f'/'

                    if act['Status'] == 'Note On': 
                        action += f'note:{act["MB1"]}'
                    elif act['Status'] == 'Controller': 
                        action += f'cc:{act["MB1"]},{act["ValueLow"]}'
                                      

            art.art_action = action

            self.articulation_list.append(art)

class Articulation:
    def __init__(self) -> None:
        self.art_progchange = 0
        self.art_name = ""
        self.disp_name = ""
        self.art_color = ""
        self.art_icon = ""
        self.art_action = None

class UACCList:
    try:
        uacc_file = open('UACC List.csv', 'r')
    except IOError:
        print("Couldn't find UACC List file. Exiting...")
        time.sleep(2)
        sys.exit()

    reader = csv.DictReader(uacc_file, ["id", "color", "icon"], "names")

    def FindUACC(art_name):
        pc, color, icon = "127", "default", "note-quarter"
        match, match_candidate = "", ""
        match_score, cur_match_score = 0, 0

        for i in UACCList.reader:
            match_candidate = difflib.get_close_matches(art_name, i["names"], cutoff=0.2)

            if (len(match_candidate) > 0):
                cur_match_score = difflib.SequenceMatcher(None, art_name, match_candidate[0]).ratio()

            if (cur_match_score > match_score):
                match = match_candidate[0]
                match_score = cur_match_score
                cur_match_score = 0

                pc, color, icon = i["id"], i["color"], i["icon"]
        
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
        print("Starting conversion...")  
        for map in FileOps.expression_maps:
            bank = ArticulationBank(str(map))
            result = bank.GenerateHeader() + bank.GenerateArticulations()

            FileOps.ExportReabank(result, map)
            print(end='\x1b[2K') # LINE CLEAR
            print(f'Processing {bank.bank_name}...', end='\r')

    def ConvertPlistMaps():
        print("Starting conversion...")  
        for map in FileOps.expression_maps:
            bank = ArticulationBankPlist(str(map))
            result = bank.GenerateHeader() + bank.GenerateArticulations()

            FileOps.ExportReabank(result, map)
            print(end='\x1b[2K') # LINE CLEAR
            print(f'Processing {bank.bank_name}...', end='\r')

    def ExportMergedReabank():
        export_path = PurePath(Path.cwd(), "Reabank Export", "Merged Export.reabank")
        file = open(Path(export_path), "w")
        file.write(ArticulationBank.merged_result)
        file.close

    def FindExpressionMaps():
        FileOps.expression_maps = sorted(Path.cwd().rglob('*.expressionmap'))
        print(str(len(FileOps.expression_maps))+" expression maps found...")

    def FindPlistMaps():
        FileOps.expression_maps = sorted(Path.cwd().rglob('*.plist'))
        print(str(len(FileOps.expression_maps))+" Logic plist files found...")

def main():
    print(f'EXPRESSIONMAP TO REATICULATE CONVERTER')
    print(f'Pick your source file type\n[1] Cubase .expressionmap\n[2] Logic .plist')
    selection = input()

    match(selection):
        case '1':
            FileOps.FindExpressionMaps()
            FileOps.ConvertExpressionMaps()     
        case '2':
            FileOps.FindPlistMaps()
            FileOps.ConvertPlistMaps() 
        case _:
            print(f'No valid option picked. Exiting...')
            time.sleep(1)
            exit()

    FileOps.ExportMergedReabank()
    input("Conversion complete. Press a key to exit...")

if __name__ == "__main__":
    main()