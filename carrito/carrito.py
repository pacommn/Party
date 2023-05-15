

class Carrito():

    def __init__(self,request):
        self.request = request
        self.session =request.session
        carrito=self.session.get("carrito")
        if not carrito:
            carrito=self.session["carrito"]={}
        else:
            carrito=carrito
            
    def agregar(self,entrada):
        if str(entrada.entradaId) not in self.carrito.keys():
            self.carrito[entrada.entradaId]={
                "entradaId":entrada.entradaId,
                "tipo":entrada.tipo,
                "coste":str(entrada.coste),
                "dni":entrada.dni,
                "nombre":entrada.nombre,
                "cantidad":entrada.cantidad,
                "personas":str(entrada.personas),
                "fecha":entrada.fecha,
                "discotecaId":entrada.discotecaId,
                "fiestaId":entrada.fiestaId,
                "usuarioId":entrada.usuarioId,
                "pagado":str(entrada.pagado)
            }
        
        else:
            for clave, valor in self.carrito.items():
                if clave==str(entrada.entradaId):
                    valor["cantidad"]+=1
                    break

        self.actualizar_carrito()   


    def actualizar_carrito(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True

    def eliminar(self,entrada):
        entrada.entradaId=str(entrada.entradaId)
        if entrada.entradaId in self.carrito:
            del self.carrito[entrada.entradaId]
            self.actualizar_carrito()

    def restar_entradas(self,entrada):
        for clave, valor in self.carrito.items():
            if clave==str(entrada.entradaId):
                valor["cantidad"]-=1
                if valor["cantidad"]<1:
                    self.eliminar(entrada)
                break
        self.actualizar_carrito()

    def limpiar_carrito(self):
        carrito=self.session["carrito"]={}
        self.actualizar_carrito()


    