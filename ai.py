from constants import SUELO_Y, ALTO_AGACHADO, ALTO_DINO

METEORO_SALTO_MAX_T = 12
METEORO_AGACHAR_MAX_T = 16
METEORO_BLOQUEO_SALTO_T = 5
METEORO_BLOQUEO_RAPIDA_T = 18

METEORO_BANDA_BAJA_TOL = 4
METEORO_BANDA_CABEZA_TOL = 6

REACCION_MULT_PAJARO_MEDIO = 7
REACCION_MARGEN_PAJARO_MEDIO = 24
REACCION_MULT_SALTO = 9
REACCION_MARGEN_SALTO = 18
REACCION_MULT_FOSO = 5
REACCION_MARGEN_FOSO = 10
RAPIDA_MULT_DISTANCIA = 16

METEORO_SIM_FRAMES = 240


def procesar_ia(dino, obstaculos, velocidad):
    dr = dino.rect
    saltar = agachar = rapida = False

    meteoros = [
        ob for ob in obstaculos if ob.tipo == "meteorito" and ob.x + ob.w > dr.left
    ]
    bloquear_salto = False
    bloquear_rapida = False
    if meteoros:
        met = min(meteoros, key=lambda o: o.x)
        estado, t_in, fondo = predecir_meteorito(met, dr, velocidad)
        if estado == "cruza":
            if fondo >= SUELO_Y - ALTO_AGACHADO - METEORO_BANDA_BAJA_TOL:
                if dino.en_suelo and t_in <= METEORO_SALTO_MAX_T:
                    saltar = True
                bloquear_rapida = t_in <= METEORO_BLOQUEO_RAPIDA_T
            elif fondo >= SUELO_Y - ALTO_DINO - METEORO_BANDA_CABEZA_TOL:
                if t_in <= METEORO_AGACHAR_MAX_T:
                    agachar = True
                bloquear_salto = t_in < METEORO_BLOQUEO_SALTO_T
                bloquear_rapida = t_in <= METEORO_BLOQUEO_RAPIDA_T

    delante = [
        ob for ob in obstaculos if ob.tipo != "meteorito" and ob.x + ob.w > dr.left
    ]
    if not delante:
        if not dino.en_suelo and not bloquear_rapida:
            rapida = True
        return saltar, agachar, rapida

    ob = min(delante, key=lambda o: o.x)
    gap = ob.x - dr.right
    quiere_saltar = False
    if ob.tipo == "pajaro":
        if ob.nivel == "medio":
            agachar = (
                agachar
                or gap
                <= velocidad * REACCION_MULT_PAJARO_MEDIO + REACCION_MARGEN_PAJARO_MEDIO
            )
        elif ob.nivel == "bajo":
            quiere_saltar = (
                dino.en_suelo
                and 0 <= gap <= velocidad * REACCION_MULT_SALTO + REACCION_MARGEN_SALTO
            )
    elif ob.tipo == "cangrejo":
        cierre = velocidad + ob.vel_propia
        quiere_saltar = (
            dino.en_suelo
            and 0 <= gap <= cierre * REACCION_MULT_SALTO + REACCION_MARGEN_SALTO
        )
    elif ob.tipo == "foso":
        quiere_saltar = (
            dino.en_suelo
            and 0 <= gap <= velocidad * REACCION_MULT_FOSO + REACCION_MARGEN_FOSO
        )
    else:
        quiere_saltar = (
            dino.en_suelo
            and 0 <= gap <= velocidad * REACCION_MULT_SALTO + REACCION_MARGEN_SALTO
        )

    if quiere_saltar and not bloquear_salto:
        saltar = True
    if (
        not dino.en_suelo
        and not bloquear_rapida
        and gap > velocidad * RAPIDA_MULT_DISTANCIA
    ):
        rapida = True

    return saltar, agachar, rapida


def predecir_meteorito(ob, dr, velocidad):
    x, y, vy = ob.x, ob.y, ob.vy
    t = 0
    t_in = None
    fondo = y + ob.h
    while t < METEORO_SIM_FRAMES:
        x -= velocidad + ob.vx_propia
        vy += ob.g_propia
        y += vy
        t += 1
        if y + ob.h >= SUELO_Y:
            if t_in is None:
                return ("impacto", None, None)
            break
        if x <= dr.right and x + ob.w >= dr.left:
            if t_in is None:
                t_in = t
            fondo = max(fondo, y + ob.h)
        elif t_in is not None:
            break
        if x + ob.w < dr.left:
            break
    if t_in is None:
        return ("lejos", None, None)
    return ("cruza", t_in, fondo)

