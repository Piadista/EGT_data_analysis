
def get_type(elemento):
    if "std" in elemento.lower():
        return "Standard"
    elif "eno" in elemento.lower():
        return "Enode"
    elif "bic" in elemento.lower():
        return "Bicamada"

def get_chip(elemento):
    if "/1/disp" in elemento.lower():
        return "1"
    elif "/2/disp" in elemento.lower():
        return "2"

def get_disp(elemento):
    if "disp1" in elemento.lower():
        return "1"
    elif "disp2" in elemento.lower():
        return "2"
    elif "disp3" in elemento.lower():
        return "3"
    elif "disp_1" in elemento.lower():
        return "1"
    elif "disp_2" in elemento.lower():
        return "2"
    elif "disp_3" in elemento.lower():
        return "3"

def get_eletrolito(elemento):
    if "mgcl2" in elemento.lower():
        return "MgCl2"
    elif "kcl" in elemento.lower():
        return "KCl"

def get_measure(elemento):
    if "110transfer" in elemento.lower():
        return "110"
    elif "140transfer" in elemento.lower():
        return "140"
    elif "150transfer" in elemento.lower():
        return "150"
    elif "151transfer" in elemento.lower():
        return "151"
    elif "152transfer" in elemento.lower():
        return "152"
    elif "210transfer" in elemento.lower():
        return "210"
    elif "230transfer" in elemento.lower():
        return "230"
    elif "250transfer" in elemento.lower():
        return "250"
    elif "310transfer" in elemento.lower():
        return "310"
    elif "330transfer" in elemento.lower():
        return "330"
    elif "410transfer" in elemento.lower():
        return "410"


def get_potential(elemento):
    if "endurance100mv" in elemento.lower():
        return "0.1"
    elif "endurance800mv" in elemento.lower():
        return "0.8"
