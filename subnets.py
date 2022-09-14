
# Outil pour calculer les sous-réseaux possibles sur Python
# Testé sur Linux et fonctionnera sur Bash. Il marchera probablement
# Avec Microsoft Powershell.

from copy import copy

num_to_letters = {
    0:"A", 1:"B", 2:"C", 3:"D",
}

def bin(s):
    '''
    Formule de wiki.python.org pour convertir un nombre en bits
    '''
    return str(s) if s<=1 else bin(s>>1) + str(s&1)

# Objet pour traiter les ips
class ip:
    def __init__(self, ip_string:str) -> None:
        '''

        Créer un ip

        '''

        splitted_ips = ip_string.split(".")
        
        # Représentation en octets UwU
        buffer = []
        for byte in splitted_ips:
            buffer.append(
                bin(int(byte)).zfill(8)
            )
        print(buffer)

        self.bytes = buffer
        
        
    # Retourne la classe d'ip
    def getClass(self):
        '''

        Retourne la classe d'adresse ip en cherchant l'addresse qui commence par 0

        '''

        try:self.ipClass
        except:pass
        else:return self.ipClass
       
        i = 0
        n = 0
        while True:
            try: self.bytes[0][i]
            except: break
            finally: pass

            if self.bytes[0][i] == "1": pass
            else: break
            i+=1

            if i>=3:
                break
        
        self.mask = (i+1)*8
        self.ipClass = num_to_letters[i]
        return self.ipClass

    def addToMask(self, mask):
        self.mask += mask

    def fullbytes(self):
        s = ""
        for i, byte in enumerate(self.bytes):
            s += byte
        return s


    def getNetId(self):
        return self.fullbytes()[0:self.mask]

    def getHostId(self):
        return self.fullbytes()[self.mask+1:]

    def __str__(self) -> str:
        s = ""
        for i, byte in enumerate(self.bytes):
            s += str( int(byte,2) )
            if i < 3:
                s+="."
        return s


def main(ip_string, desired_subnets):
    ip_object = ip(ip_string)
    print( "La classe de réseau est", ip_object.getClass() )
    print( "L'addresse est toujours", str(ip_object))

    ip_object.addToMask(3 if not desired_subnets else int(desired_subnets))
    print( "Le nouveau masque est /", ip_object.mask)

    print( "netid hostid: ", ip_object.getNetId(), ip_object.getHostId() )

    pass

# Récupérer les arguments de lancement
if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1: # Pas d'arguments ?
        main("10.168.0.0", "8")

    else:
        ip_arg:str = sys.argv[1]

        # Exception si l'ip ne ressemble pas à une ip
        assert len(ip_arg.split(".")) == 4, "Not a valid IPv4 address"

        try: desired_subnets = sys.argv[2]
        except IndexError: desired_subnets = "0"
        finally: main(ip_arg, desired_subnets)