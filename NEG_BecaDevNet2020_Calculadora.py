#===========================================================
#       BecasDevnet2020 - Script Calculadora - NEG
#===========================================================

from math import sqrt

print(
    """
    +==============================================+
    |                                              |
    |  BecasDevnet2020 - Script Calculadora - NEG  |
    |                                              |
    +==============================================+
    """)
while True:
    try:
        print(
            """
            +================================+
            | Las opciones disponibles son:  |
            | 1 -> Suma                      |
            | 2 -> Resta                     |
            | 3 -> Multiplicación            |
            | 4 -> División                  |
            | 5 -> Exponenciación            |
            | 6 -> Raiz cuadrada             |
            | 7 -> Porcentaje                |
            | 9 -> Salir                     |                   
            +================================+
            """)
        x = int(input("Selecciona una acción: "))

        if x == 1:
            print("Operación seleccionada: suma")
            valor1 = float(input("Dime un número: "))
            valor2 = float(input("Dime otro número: "))
            print("El resultado es: ", valor1+valor2)
        elif x == 2:
            print("Operación seleccionada: resta")
            valor1 = float(input("Dime un número: "))
            valor2 = float(input("Dime otro número: "))
            print("El resultado es: ", valor1-valor2)
        elif x == 3:
            print("Operación seleccionada: multiplicación")
            valor1 = float(input("Dime un número: "))
            valor2 = float(input("Dime otro número: "))
            print("El resultado es: ", valor1*valor2)
        elif x == 4:
            print("Operación seleccionada: división")
            valor1 = float(input("Dime un número: "))
            valor2 = float(input("Dime otro número: "))
            print("El resultado es: ", valor1/valor2)
        elif x == 5:
            print("Operación seleccionada: Exponenciación")
            valor1 = float(input("Dime un número: "))
            valor2 = float(input("Dime otro número: "))
            print("El resultado es: ", valor1**valor2)
        elif x == 6:
            print("Operación seleccionada: Raiz cuadrada")
            valor1 = float(input("Dime un número: "))
            assert valor1 >= 0.0
            print("El resultado es: ", sqrt(valor1))
        elif x == 7:
            print("Operación seleccionada: Porcentaje")
            valor1 = int(input("Dime el porcentaje entre 0 y 100: "))
            assert valor1 >= 0.0 and valor1 <= 100
            valor2 = float(input("Dime una cantidad: "))
            print("El resultado es: ", (valor2*valor1)/100)
        elif x == 9:
            print("Fin del programa")
            break
        else:
            print("La opción introducida no es correcta. Selecciona una acción o introduce 9 para terminar: ")

    except ZeroDivisionError:
        print("Error. No es posible dividir entre cero.") 
    except ValueError:
        print("Error. El valor introducido no es correcto.") 
    except ArithmeticError:
        print("Error. Problema aritmético.") 
    except AssertionError:
        print("Error: El valor no está dentro del rango permitido")
    except Exception:
        print("Error. Ha ocurrido una excepción.")      
    except BaseException:
        print("Error. Ha ocurrido una error.")  
    except:
        print("Ha ocurrido un error")
