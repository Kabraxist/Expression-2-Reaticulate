import untangle
from pathlib import Path

source_file_path = input("Enter full path to source .expressionmap file: ")
filename = Path(source_file_path).stem
folder_path = str(Path(source_file_path).resolve().parent) + '\\'

root = untangle.parse(source_file_path)

instrument_name = [i['value'] for i in root.InstrumentMap.string if i['name'] == "name"][0]

slots = [i for i in root.InstrumentMap.member if i['name'] == 'slots'][0]
slots_list = [i for i in slots.list.obj if i['class'] == 'PSoundSlot']

def GenerateArticulations():
    output = ""

    program_change = 0

    for item in slots_list:
        program_change += 1
        result = ""
        articulation_name = ""
        articulation_switch = 0

        member = [i for i in item.member if i['name'] == "name"][0]
        articulation_name = member.string["value"] + " "

        action = [i for i in item.obj if i['class'] == 'PSlotMidiAction'][0]
        for int in action.int:
            if(int["name"] == "key"):
                articulation_switch = int["value"]

        output += f'//! c=long i=note-whole o=note:{articulation_switch}\n{program_change} {articulation_name}\n'
    
    return(output)


def GenerateHeader():
    header = f'//! g="Converted Maps" n="{instrument_name}"\nBank * * {instrument_name}\n'
    return header

file = open(folder_path+filename+".reabank", "w")
file.write(GenerateHeader() + GenerateArticulations())
file.close()

print("File must be generated?")
input("Press any key to exit...")