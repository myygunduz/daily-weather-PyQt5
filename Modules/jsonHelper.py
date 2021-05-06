import  json

def writeJ(icerik, dosya, indent: int = 2):
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(icerik, f, indent=indent, ensure_ascii=False)


def readJ(dosya: str) :
    json_file = open(dosya, "r", encoding="utf-8")
    icerik = json.load(json_file)
    json_file.close()
    return icerik