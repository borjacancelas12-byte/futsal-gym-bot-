def get_rutina(posicion):
    posicion = posicion.lower()
# rutinas.py
rutinas = {
    "portero": {
        "futbol": [
            ["Agilidad lateral", "https://youtu.be/Q9-JjY3WJ3A"],
            ["Reflejos con balón", "https://youtu.be/5j6iH0n5Q-Y"],
        ],
        "gym": [
            ["Saltos pliométricos", "https://youtu.be/C4Zp9E5eBbg"],
            ["Trabajo de core", "https://youtu.be/pSHjTRCQxIw"],
        ],
    },
    "defensa": {
        "futbol": [
            ["Desplazamiento defensivo", "https://youtu.be/LDjT_qsZgkI"],
            ["Interceptación de pases", "https://youtu.be/3vprI2u1oZo"],
        ],
        "gym": [
            ["Sentadillas", "https://youtu.be/aclHkVaku9U"],
            ["Peso muerto", "https://youtu.be/op9kVnSso6Q"],
        ],
    },
    "medio": {
        "futbol": [
            ["Pases rápidos", "https://youtu.be/x7iZKkK8o18"],
            ["Control de balón", "https://youtu.be/B0p2XwncK8I"],
        ],
        "gym": [
            ["Plancha lateral", "https://youtu.be/Kz2HAt0gkXk"],
            ["Burpees", "https://youtu.be/TU8QYVW0gDU"],
        ],
    },
    "delantero": {
        "futbol": [
            ["Remates a portería", "https://youtu.be/Jy0Z3Q-GyRE"],
            ["Dribling y velocidad", "https://youtu.be/9bDbz2a7fK4"],
        ],
        "gym": [
            ["Sprint en cinta", "https://youtu.be/QW4lXqO6aR0"],
            ["Saltos al cajón", "https://youtu.be/52rHf27w1qk"],
        ],
    },
}


    return rutinas.get(posicion, "Esa posición no existe 😅")
