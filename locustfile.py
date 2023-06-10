from locust import HttpUser, task, between
import secrets

class MyUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Obtener el token CSRF al realizar una solicitud GET a la ruta de inicio de sesión
        response = self.client.get("login")
        print("-----------------------------------------------")
        print(response.cookies)
        if 'csrftoken' in response.cookies:
            self.csrf_token = response.cookies['csrftoken']
        else:
            self.csrf_token = secrets.token_hex(32)

    @task(50)
    def index(self):
        self.client.get("")

    @task(50)
    def login(self):
        headers = {'X-CSRFToken': self.csrf_token}  # Incluir el token CSRF en los encabezados
        data = {
            "username": "pacommn",
            "contasena": "pacoeldeLA10",
            "csrfmiddlewaretoken": self.csrf_token  # Incluir el token CSRF en los datos del formulario
        }
        self.client.post("login", data=data, headers=headers)

    @task(50)
    def comprar(self):
        headers = {'X-CSRFToken': self.csrf_token}  # Incluir el token CSRF en los encabezados
        data = {
            "nombre": "paco",
            "dni": "4646",
            "cantidad":1,
            "tipo":"N",
            "csrfmiddlewaretoken": self.csrf_token  # Incluir el token CSRF en los datos del formulario
        }
        self.client.post("fiesta/54", data=data, headers=headers)
    
    @task(50)
    def comprar2(self):
        headers = {'X-CSRFToken': self.csrf_token}  # Incluir el token CSRF en los encabezados
        data = {
            "nombre": "paco",
            "dni": "4646",
            "cantidad":1,
            "tipo":"N",
            "csrfmiddlewaretoken": self.csrf_token  # Incluir el token CSRF en los datos del formulario
        }
        self.client.post("fiesta/55", data=data, headers=headers)
    
    @task(50)
    def comprar3(self):
        headers = {'X-CSRFToken': self.csrf_token}  # Incluir el token CSRF en los encabezados
        data = {
            "nombre": "paco",
            "dni": "4646",
            "cantidad":1,
            "tipo":"N",
            "csrfmiddlewaretoken": self.csrf_token  # Incluir el token CSRF en los datos del formulario
        }
        self.client.post("fiesta/59", data=data, headers=headers)

    @task(10)
    def fiestas(self):
        self.client.get("fiestas")

    @task(10)
    def discotecas(self):
        self.client.get("discotecas")

    @task(10)
    def mapa(self):
        self.client.get("mapa")

    @task(30)
    def editar_info(self):
        headers = {'X-CSRFToken': self.csrf_token}
        data = {
            "edad": "21",
            "usuario": "valor2",
            "username":"pepepe"
            # Agrega más campos y valores según tus necesidades
        }
        self.client.put("editar_info/", data=data, headers=headers)

    @task(50)
    def cambiar_foto(self):
        headers = {'X-CSRFToken': self.csrf_token}
        data = {
            "foto": "/media/imagenes/efwef.png"
            # Agrega más campos y valores según tus necesidades
        }
        self.client.put("cambiar_foto/", data=data, headers=headers)    

    # Agrega más tareas para probar otras rutas según tus necesidades
