#!/usr/bin/env python3 

#===========================================================
#       BecasDevnet2020 - Script APIC-EM - NEG
#===========================================================

import requests
import json
import urllib3
from pprint import pprint
from tabulate import *

requests.packages.urllib3.disable_warnings()

class codigo_ErrorHTTP(Exception):
    def __init__(self, codigo, mensaje, info):
        Exception.__init__(self, mensaje)
        self.codigo = codigo
        self.info = info


def saca_Ticket():
    token = ""
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"
    headers = {
        "Content-Type": "application/json"
    }

    body_json = {
        "password": "Xj3BDqbU",
        "username": "devnetuser"
    }

    resp = requests.post(url,json.dumps(body_json),headers=headers,verify=False)
    response_json = resp.json()["response"]

    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        token = response_json["serviceTicket"]
        print("El ticket de servicio asignado es: ", token)
        return token


def num_hosts():
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host/count"

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()["response"]

    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        print("Número de hosts:", response_json)


def resumen_Hosts():
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()["response"]

    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        # Imprimimos resumen hosts
        lista_Host = []
        contador = 0
        for el in response_json:
            contador += 1
            host = [
            contador,
            el["hostType"],
            el["hostIp"],
            el["hostMac"],
            el["vlanId"]
            ]
            lista_Host.append(host) 
    
        tableHeader = ["Número", "Tipo", "IP", "MAC", "VLAN"]
        print(tabulate(lista_Host, tableHeader))


def num_EquiposRed():
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device/count"

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()["response"]
    
    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        print("Número de equipos de red:", response_json)


def resumen_EquiposRed():
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device"

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()["response"]

    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        # Imprimimos resumen equipos de red
        equipos_Red = []
        contador = 0
        for equipo in response_json:
            contador += 1
            equipo = [
                contador,
                equipo["hostname"],
                equipo["family"],
                equipo["softwareVersion"],
                equipo["interfaceCount"],
                equipo["managementIpAddress"],
                equipo["serialNumber"],
                equipo["id"]           
            ]
            equipos_Red.append(equipo) 

        tableHeader = ["Nº", "Nombre", "Familia", "Software", "Nº Int", "IP Gestión", "Nº Serie", "ID"]
        print(tabulate(equipos_Red, tableHeader))


def int_EquipoRed():
    equipo_Id = input("Introduce el identificador del dispositivo de red: ")
    url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/interface/network-device/" + equipo_Id

    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()["response"]

    if resp.status_code < 200 or resp.status_code > 299:
		    raise codigo_ErrorHTTP(resp.status_code, response_json["errorCode"], response_json["detail"])
    else:
        # Imprimimos resumen interfaces
        int_Equipo = []
        contador = 0
        for el in response_json:
            contador += 1
            equipo = [
                contador,
                el["portName"],
                el["status"],
                el["adminStatus"],
                el["ipv4Address"],
                el["ipv4Mask"], 
                el["macAddress"]       
            ]
            int_Equipo.append(equipo) 

        tableHeader = ["Nº", "Nombre", "Estado", "Est administ", "IP", "Máscara", "MAC"]
        print(tabulate(int_Equipo, tableHeader))




print(
    """
    +==========================================+
    |                                          |
    | BecasDevnet2020 - Script APIC-EM - NEG   |
    |                                          |
    +==========================================+
    """)

token = ""
    
while True:
    try:
        if token == "":
            token = saca_Ticket()

            headers = {
                "Content-Type": "application/json",
                "X-Auth-Token": token
            }




        print(
            """
            +================================+
            | Las opciones disponibles son:  |
            | 1 -> Número hosts              |
            | 2 -> Resumen hosts             |
            | 3 -> Número equipos de red     |
            | 4 -> Resumen equipos de red    |
            | 5 -> Interfaces equipo de red  |
            | 9 -> Salir                     |                   
            +================================+
            """)

        x = int(input("Selecciona una acción: "))

        if x == 1:
            print("Operación seleccionada: Número hosts")
            num_hosts()
        elif x == 2:
            print("Operación seleccionada: Resumen hosts")
            resumen_Hosts()
        elif x == 3:
            print("Operación seleccionada: Número equipos de red")
            num_EquiposRed()
        elif x == 4:
            print("Operación seleccionada: Resumen equipos de red")
            resumen_EquiposRed()
        elif x == 5:
            print("Operación seleccionada: Interfaces equipo de red")
            int_EquipoRed()
        elif x == 9:
            print("Fin del programa")
            break
        else:
            print("La opción introducida no es correcta. Selecciona una acción o introduce 9 para terminar: ")


    except codigo_ErrorHTTP as c:
        print("Error. Código HTTP:", c.codigo, "-", c, "\nDetalles:", c.info)
    except ValueError:
        print("Error. El valor introducido no es correcto.") 
    except AssertionError:
        print("Error: El valor no está dentro del rango permitido")
    except Exception:
        print("Error. Ha ocurrido una excepción.")      
    except BaseException:
        print("Error. Ha ocurrido una error.")  
    except:
        print("Ha ocurrido un error")

