#! python3

#===========================================================
#       BecasDevnet2020 - Script Restconf - NEG
#===========================================================

import json, requests
from tabulate import *
from pprint import pprint
requests.packages.urllib3.disable_warnings()


class codigo_ErrorHTTP(Exception):
    def __init__(self, codigo, mensaje):
        Exception.__init__(self, mensaje)
        self.codigo = codigo


# Valores por defecto
https = "https://"
base = "/restconf/data/"
yang_module_int = "ietf-interfaces:interfaces/"
yang_module_intDetail = "ietf-interfaces:interfaces-state"

basic_auth = ("cisco", "cisco123!")

headers = {
    "Accept":"application/yang-data+json", 
    "Content-Type":"application/yang-data+json"
    }


        
def lista_Int():
    # Petición de información modelo YANG ietf-interfaces:interfaces
    url = https + IP + base + yang_module_int
    
    resp = requests.get(url, auth=basic_auth, headers=headers, verify=False)
    if resp.status_code in range(200, 300):
        resp_json = resp.json()

        # Sacamos Nombre e IP de las interfaces
        intList = []
        for el in resp_json["ietf-interfaces:interfaces"]["interface"]:
            interface = []
            interface.append(el["name"])
            if el["ietf-ip:ipv4"] == {}:
                interface.append(IP)
            else:
                interface.append(el["ietf-ip:ipv4"]["address"][0]["ip"])
            intList.append(interface)  
    else:
            raise codigo_ErrorHTTP(resp.status_code, resp.text)



    # Petición de información modelo YANG interfacesietf-interfaces:interfaces-state
    url = https + IP + base + yang_module_intDetail

    resp = requests.get(url, auth=basic_auth, headers=headers, verify=False)
    if resp.status_code in range(200, 300):
        resp_json = resp.json()

        # Añadimos MAC a la lista intList
        counter = 0
        for el in resp_json["ietf-interfaces:interfaces-state"]["interface"]:
            intList[counter].append(el["phys-address"])
            counter += 1

        # Imprimimos tabla interfaces (nombre, IP , MAC)
        tableHeader = ["Interfaz", "IP", "MAC"]
        print(tabulate(intList, tableHeader))

    else:
            raise codigo_ErrorHTTP(resp.status_code, resp.text)
        

def crea_Int():
    name_add = input("Nombre de la interfaz sin espacios en blanco: ")
    ip_add  = input("IP: ")
    mas_add = input("Máscara: ")
    descr_add = input("Descripción: ")


    yang_configuration = {
      "ietf-interfaces:interface": {
        "name": name_add,
        "description": descr_add,
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": ip_add,
              "netmask": mas_add
            }
          ]
        },
        "ietf-ip:ipv6": {}
      }
    }
    
    url = https + IP + base + yang_module_int + "interface=" + name_add
    resp = requests.put(url, data=json.dumps(yang_configuration) ,auth=basic_auth, headers=headers, verify=False)

    if resp.status_code in range(200, 300):
        print("Interfaz creada")
    else:
            raise codigo_ErrorHTTP(resp.status_code, resp.text)


def borra_Int():
    name_add = input("Nombre de la interfaz sin espacios en blanco: ")

    url = https + IP + base + yang_module_int + "interface=" + name_add
    resp = requests.delete(url ,auth=basic_auth, headers=headers, verify=False)

    if resp.status_code in range(200, 300):
        print("Interfaz borrada")
    else:
            raise codigo_ErrorHTTP(resp.status_code, resp.text)




print(
    """
    +==========================================+
    |                                          |
    | BecasDevnet2020 - Script Restconf - NEG  |
    |                                          |
    +==========================================+
    """)
IP = ""
while True:
    try:
        if IP == "":
            IP = input("Dime la IP del dispositivo: ")

        print(
            """
            +================================+
            | Las opciones disponibles son:  |
            | 1 -> Listar interfaces         |
            | 2 -> Crear interfaz            |
            | 3 -> Borrar interfaz           |
            | 4 -> Obtener tabla rutas       |
            | 5 -> Salir                     |                   
            +================================+
            """)
        x = int(input("Selecciona una acción: "))
        if x == 1:
            print("Operación seleccionada: Listar interfaces")
            lista_Int()

        elif x == 2:
            print("Operación seleccionada: Crear interfaz")
            crea_Int()

        elif x == 3:
            print("Operación seleccionada: Borrar interfaz")
            borra_Int()

        elif x == 4:
            print("Operación seleccionada: Obtener tabla rutas")
            print("Modelo yang para obtener tabla de rutas no encontrado")
            
        elif x == 5:
            print("Fin del programa")
            break
        else:
            print("La opción introducida no es correcta. Selecciona una acción o introduce 5 para terminar: ")


    except codigo_ErrorHTTP as c:
        print("Error. Código HTTP:", c.codigo, "-", c)
    except ValueError:
        print("Error. El valor introducido no es correcto.") 
    except AssertionError:
        print("Error: El valor no está dentro del rango permitido")
    except Exception as e:
        print("Error. Ha ocurrido una excepción:\n", e)      
    except BaseException:
        print("Error. Ha ocurrido una error.")  
    except:
        print("Ha ocurrido un error")




