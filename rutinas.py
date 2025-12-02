def get_rutina(posicion):
    posicion = posicion.lower()

    rutinas = {
        "pivot": "Rutina Pivot:\n- Sentadillas 4x10\n- Press banca 4x8\n- Sprints 10x20m",
        "cierre": "Rutina Cierre:\n- Peso muerto 4x6\n- Core 4x15\n- Resistencia 20 min",
        "ala": "Rutina Ala:\n- Saltos pliométricos\n- Sprints laterales\n- Dominadas",
        "portero": "Rutina Portero:\n- Reflejos\n- Saltos\n- Fuerza de tren superior"
    }

    return rutinas.get(posicion, "Esa posición no existe 😅")
