def importe_total_carrito(request):
    total=0
    if request.user.is_authenticated:
        if 'carrito' in request.session: 
            for clave, valor in request.session["carrito"].items():
                total+=float(valor["coste"])*valor["cantidad"]

    return {"importe_total_carrito": total}
