from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
# Create your views here.
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("APP_USR-4989301092010028-031112-8ec03be037cc76704baaec21a1604e49-2319025513")


class ReferenceMPView(APIView):
    def post(self, request, format=None):
        items = request.data.get("items")
        newlist = [
            {
            "unit_price": float(x.pop("precio")),
            "title": x.pop("nombre"),
            "quantity": x.pop("cantidad"),
            **x
            }
             if "precio" and "cantidad" and "nombre" in x else x for x in items]
        infoClient = request.data.get("client")
       # Crea un ítem en la preferencia
        if items:
            preference_data = {
                "items": newlist
            }

            preference = sdk.preference().create(preference_data)
            print(preference)
            if preference['status'] == 400:

                return Response(status=status.HTTP_404_NOT_FOUND)
            response = preference["response"]
            print(response)
            # return Response({"init_point": response["init_point"]})
            return Response({"init_point": response.get("init_point", "No disponible")})
        return Response(status=status.HTTP_404_NOT_FOUND)

# class ReferenceMPView(APIView):
#     def post(self, request, format=None):

#         ACCESS_TOKEN = "APP_USR-936168452210572-061619-f651358d6e63a47ac60b46fe256f4e2d-582661966"
#         url = "https://api.mercadopago.com/checkout/preferences"
#         headers = {
#             "Authorization": f"Bearer {ACCESS_TOKEN}",
#            "Accept": "application/json"
#         }

#         response = requests.get(url, headers=headers)

#         # Verificar si la respuesta es JSON antes de convertirla
#         if response.status_code == 200:
#          try:
#                print(response.json())  # Si la respuesta es válida, imprimir el JSON
#          except requests.exceptions.JSONDecodeError:
#                 print("La respuesta no es un JSON válido:", response.text)
#         else:
#             print(f"Error {response.status_code}: {response.text}")  # Ver mensaje de error






#         items = request.data.get("items")

#         if not items:
#             return Response({"error": "No se recibieron items"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             newlist = [
#                 {"unit_price": float(x["precio"]), 
#                  "title": x["nombre"], 
#                  "quantity": x["cantidad"]} 
#                 for x in items if all(k in x for k in ["precio", "nombre", "cantidad"])
#             ]
#         except KeyError:
#             return Response({"error": "Formato de items incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

#         preference_data = {"items": newlist}
#         print("Datos enviados a Mercado Pago:", preference_data)

#         preference = sdk.preference().create(preference_data)

#         if "error" in preference:
#             return Response({"error": "Error de Mercado Pago", "details": preference}, status=status.HTTP_400_BAD_REQUEST)

#         response = preference.get("response", {})

#         if "init_point" not in response:
#             return Response({"error": "No se pudo generar el enlace de pago", "details": response}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"init_point": response["init_point"]})
