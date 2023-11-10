import random

class Agente:

    # Constructor
    def __init__(self):
        self.color = None
        self.x = None
        self.y = None
        self.motivacion = 0
        self.dinero = random.randint(0,250)
        self.edad = random.randint(10,70)
        self.familiares = random.randint(0,5)
        self.condicional = random.randint(0,1)
        self.objetivoCumplido = False
        self.diasQuedarse = None
        self.deportado = False
        self.muerto = False
        self.trabajadorIlegal = False

        if self.condicional == 0:
            self.estadoVisa = True
        
        if self.condicional == 1:
            self.estadoVisa = False
        

    # Pais A Gamma de colores Azules
    def escogerColorPaisA(self, lista):

        while True:
            self.r = random.randint(0,50)
            self.g = random.randint(0,50)
            self.b = random.randint(200,255)
            if not self.compararColores(lista):
                break

        self.color = (self.r, self.g, self.b)

    # Pais B Gamam de colores Rojos
    def escogerColorPaisB(self, lista):

        while True:
            self.r = random.randint(200,255)
            self.g = random.randint(0,60)
            self.b = random.randint(0,60)
            if not self.compararColores(lista):
                break

        self.color = (self.r, self.g, self.b)


    # Funcion para escoger una posicion aleatoria al rededor de la cuadricula, dentro de los limites de ese pais.
    def escogerPosicionPaisA(self, lista):
        while True:
            self.x = random.randint(0, 21)
            self.y = random.randint(0, 14)
            if not self.compararColision(lista) and self.y != 14:
                break

    # Funcion para escoger una posicion aleatorio al rededor de la cuadricula, dentro de los limites de ese pais.
    def escogerPosicionPaisB(self, lista):
        while True:
            self.x = random.randint(0,21)
            self.y = random.randint(15,28)
            if not self.compararColision(lista) and self.y != 14:
                break
    
    # Funcion para obtener el color del agente
    def getColor(self):
        return self.color
    
    # Funcion auxiliar para comparar colisiones y evitar que se traslapen
    def compararColision(self, lista):
        for i in range(len(lista)):
            if lista[i].x == self.x and lista[i].y == self.y:
                return False
        return True
    
    # Funcion auxiliar para comparar colores y evitar que se repitan
    def compararColores(self, lista):
        for i in range(len(lista)):
            if lista[i].r == self.r and lista[i].g == self.g and lista[i].b == self.b:
                return False
        return True
    
    # Funcion que actua de forma aleatoria, escogiendo la nacionalidad de los agentes
    def escogerNacionalidad(self, lista):
        self.nacionalidad = random.randint(0,1)
        if self.nacionalidad == 0:
            self.escogerColorPaisA(lista)
            self.escogerPosicionPaisA(lista)
        
        if self.nacionalidad == 1:
            self.escogerColorPaisB(lista)
            self.escogerPosicionPaisB(lista)


    # Funcion auxiliar, para mandarla a llamar por cada agente y asi darle sus caracteristicas
    def inicializar(self, lista):
        self.escogerNacionalidad(lista)


    def moverDentroOtroPais(self, lista):
        if self.nacionalidad == 0:
            while True:
                self.x = random.randint(0,21)
                self.y = random.randint(15,28)
                if not self.compararColision(lista) and self.y != 14:
                    break
        if self.nacionalidad == 1:
            while True:
                self.x = random.randint(0,21)
                self.y = random.randint(0,14)
                if not self.compararColision(lista) and self.y != 14:
                    break


    # Funcion que hace la simulacion del movimiento, motivaciones y toma una desicion ya sea provisional o definitiva.
    def simular(self, lista):
        
        
        # Si cumplio el objetivo se mueve dentro del otro pais
        if self.objetivoCumplido:
            self.moverDentroOtroPais(lista)


        # Pagan 10 por cada dia que pasa
        self.dinero-=10
        self.trabajar()

        # Si su estancia se cumplio entonces regresa a su pais
        if self.diasQuedarse == 0:
            self.objetivoCumplido = False
            self.trabajadorIlegal = False

        # Si aun no tiene motivaciones, continua moviendose y generando motivaciones
        if not self.objetivoCumplido:
            self.mover(lista)
            self.motivaciones()
            self.tomarDesicion()
        
        # Si ya esta en el otro lado, cada dia que pase se le resta uno a su variable quedarse
        else:
            self.diasQuedarse-=1
            if self.trabajadorIlegal == True:
                self.trabajar()



    # Si la nacionalidad es del pais A se ganan 100 unidades, en caso de ser del pais B se ganan 50 unidades.
    # Se espera que los agentes del pais B tengan mayor tendencia a cruzar de forma ilegal, ya que probablemente alcancen mas rapido el nivel de motivacion que el dinero suficiente
    def trabajar(self):
        if self.nacionalidad == 0:
            self.dinero+= 100
        if self.nacionalidad == 1:
            if self.objetivoCumplido == True:
                self.dinero+=100
            else:
                self.dinero+= 50


    # Los agentes se mueven dentro de su propio pais
    # Principalmente de forma estetica, ya que no tiene repercusion 
    def mover(self, lista):
        if self.nacionalidad == 0:
            while True:
                self.x = random.randint(0,21)
                self.y = random.randint(0,14)
                if not self.compararColision(lista) and self.y != 14:
                    break
        if self.nacionalidad == 1:
            while True:
                self.x = random.randint(0,21)
                self.y = random.randint(15,28)
                if not self.compararColision(lista) and self.y != 14:
                    break



    # Con esta funcion los agentes cambian de pais, añadiendo posibilidades de ser deportados o morir en el intento
    def cambiarPais(self, lista):
        
        # 1/12 de ser deportado
        self.motivacion = 0
        if self.tomarDesicion() == "Ilegal":
            deportado = random.randint(0,12)
            if deportado == 1:
                self.deportado = True
                print("Deportado")
                self.deportado()
                return

        self.dinero-=100

        self.objetivoCumplido = True

        self.diasQuedarse = random.randint(1,10)

        while True:
            if self.nacionalidad == 0:
                self.x = random.randint(0,21)
                self.y = random.randint(15,28)

            if self.nacionalidad == 1:
                self.x = random.randint(0,21)
                self.y = random.randint(0,14)
            if not self.compararColision(lista) and self.y != 14:
                break
    
    
    # Comprar visa y asi poder pasar de forma legal
    def comprarVisa(self):
        self.estadoVisa = True
        self.dinero-=2500


    # Funcion para tomar desiciones segun sus variables.
    # Son motivaciones del agente, no es la decision definitiva
    # Motivacion
    # Estado Visa
    # Dinero
    def tomarDesicion(self):

        # Aqui se toma la decision definitiva
        if self.motivacion >= 100 and self.estadoVisa == False:

            if self.dinero >= 2500:
                self.comprarVisa()
                return "Comprar visa"
            else:
                self.trabajadorIlegal = True
                return "Ilegal"
        
        if self.motivacion <= 10:
            return "Quedarse"
        
        if self.motivacion >= 25 and self.estadoVisa == False:
            return "Viajar Forma Ilegal"
        
        if self.motivacion >= 50 and self.estadoVisa == True and self.familiares == 0:
            return "Viajar por turismo"
        
        if self.motivacion >= 50 and self.estadoVisa == True and self.familiares >= 1:
            return "Viajar por familia"
        
        if self.motivacion >= 75 and self.estadoVisa == False:
            return "Trabajar para comprar visa"
        
        if self.motivacion >= 75 and self.estadoVisa == True:
            return "Alistarse para el viaje"
        
        if self.motivacion >= 80 and self.estadoVisa == False:
            return "Viajar ilegalmente"
        
        if self.motivacion >= 25 and self.estadoVisa == False and self.dinero <= 1000:
            return "Viajar buscando oportunidades"
        

        return "Sin motivaciones"
        
    
    # Funcion que aumenta la motivacion del agente a viajar
    def motivaciones(self):

        for i in range(self.familiares):
            self.motivacion+=1
        
        for i in range(int(self.dinero/200)):
            self.motivacion+=2
        
        if self.motivacion >= 50 and self.estadoVisa == True:
            self.motivacion+=5

        if self.edad >= 60 and self.estadoVisa == False:
            self.motivacion+=3
        

    def deportado(self):
        self.dinero -=200
        self.objetivoCumplido = False


        

        