def get_rutina(posicion):
    posicion = posicion.lower()

    rutinas = {
        "pivot": "Rutina Pivot:\n- Sentadillas 4x10\n- Press banca 4x8\n- Sprints 10x20m",
        "cierre": "Rutina Cierre:\n- Peso muerto 4x6\n- Core 4x15\n- Resistencia 20 min",
        "ala": "Rutina Ala:\n- Saltos pliométricos\n- Sprints laterales\n- Dominadas",
        "portero": "Rutina Portero:\n- Reflejos\n- Saltos\n- Fuerza de tren superior"
    # rutinas.py
rutinas = {
    "portero": [
        {"ejercicio": "Agilidad lateral", "video": "https://youtu.be/VIDEO_PORTERO_1"},
        {"ejercicio": "Reflejos con balón", "video": "https://youtu.be/VIDEO_PORTERO_2"}
    ],
    "defensa": [
        {"ejercicio": "Desplazamiento defensivo", "video": "https://youtu.be/VIDEO_DEFENSA_1"},
        {"ejercicio": "Interceptación de pases", "video": "https://youtu.be/VIDEO_DEFENSA_2"}
    ],
    "medio": [
        {"ejercicio": "Pases rápidos", "video": "https://youtu.be/VIDEO_MEDIO_1"},
        {"ejercicio": "Control de balón en espacios reducidos", "video": "https://youtu.be/VIDEO_MEDIO_2"}
    ],
    "delantero": [
        {"ejercicio": "Remates a portería", "video": "https://youtu.be/VIDEO_DELANTERO_1"},
        {"ejercicio": "Dribling y velocidad", "video": "https://youtu.be/VIDEO_DELANTERO_2"}
    ]
}


    return rutinas.get(posicion, "Esa posición no existe 😅")
