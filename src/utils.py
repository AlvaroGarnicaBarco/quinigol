from itertools import combinations, product


def jugadas_con_premio(jugada: str, n: int) -> list[str]:
    """dado una jugada, devuelve una lista con las jugadas que darían n aciertos

    Args:
        jugada: e.g. 'M-1 0-0 2-1 1-0 0-2 2-M'
        n: número de aciertos, debe ser entre 2 y 5

    Returns:
        lista con las jugadas que dan n aciertos
    """
    posibles_resultados = ['0-0', '1-1', '2-2', 'M-M', '1-0', '2-0', '2-1', 'M-0', 'M-1', 'M-2', '0-1', '0-2', '1-2', '0-M', '1-M', '2-M']
    jugada = jugada.split(' ')
    jugadas_con_n_aciertos = []

    if not 0 <= n < 6:
        raise ValueError('n debe de estar entre 0 y 5')

    elif n == 5:
        for idx in range(6):
            _jugada = jugada.copy()
            for fallo in [x for x in posibles_resultados if x != jugada[idx]]:
                _jugada[idx] = fallo
                jugadas_con_n_aciertos.append(' '.join(_jugada))

    elif n == 4:
        for idx1, idx2 in combinations(range(6), 2):
            _jugada = jugada.copy()
            for fallo1, fallo2 in product([x for x in posibles_resultados if x != jugada[idx1]],
                                          [x for x in posibles_resultados if x != jugada[idx2]]):
                _jugada[idx1] = fallo1
                _jugada[idx2] = fallo2
                jugadas_con_n_aciertos.append(' '.join(_jugada))

    elif n == 3:
        for idx1, idx2, idx3 in combinations(range(6), 3):
            _jugada = jugada.copy()
            for fallo1, fallo2, fallo3 in product([x for x in posibles_resultados if x != jugada[idx1]],
                                                  [x for x in posibles_resultados if x != jugada[idx2]],
                                                  [x for x in posibles_resultados if x != jugada[idx3]]):
                _jugada[idx1] = fallo1
                _jugada[idx2] = fallo2
                _jugada[idx3] = fallo3
                jugadas_con_n_aciertos.append(' '.join(_jugada))

    elif n == 2:
        for idx1, idx2, idx3, idx4 in combinations(range(6), 4):
            _jugada = jugada.copy()
            for fallo1, fallo2, fallo3, fallo4 in product([x for x in posibles_resultados if x != jugada[idx1]],
                                                          [x for x in posibles_resultados if x != jugada[idx2]],
                                                          [x for x in posibles_resultados if x != jugada[idx3]],
                                                          [x for x in posibles_resultados if x != jugada[idx4]]):
                _jugada[idx1] = fallo1
                _jugada[idx2] = fallo2
                _jugada[idx3] = fallo3
                _jugada[idx4] = fallo4
                jugadas_con_n_aciertos.append(' '.join(_jugada))

    elif n == 1:
        for idx1, idx2, idx3, idx4, idx5 in combinations(range(6), 5):
            _jugada = jugada.copy()
            for fallo1, fallo2, fallo3, fallo4, fallo5 in product([x for x in posibles_resultados if x != jugada[idx1]],
                                                                  [x for x in posibles_resultados if x != jugada[idx2]],
                                                                  [x for x in posibles_resultados if x != jugada[idx3]],
                                                                  [x for x in posibles_resultados if x != jugada[idx4]],
                                                                  [x for x in posibles_resultados if x != jugada[idx5]]):
                _jugada[idx1] = fallo1
                _jugada[idx2] = fallo2
                _jugada[idx3] = fallo3
                _jugada[idx4] = fallo4
                _jugada[idx5] = fallo5
                jugadas_con_n_aciertos.append(' '.join(_jugada))

    elif n == 0:
        _jugada = jugada.copy()
        for fallo1, fallo2, fallo3, fallo4, fallo5, fallo6 in product([x for x in posibles_resultados if x != jugada[0]],
                                                                      [x for x in posibles_resultados if x != jugada[1]],
                                                                      [x for x in posibles_resultados if x != jugada[2]],
                                                                      [x for x in posibles_resultados if x != jugada[3]],
                                                                      [x for x in posibles_resultados if x != jugada[4]],
                                                                      [x for x in posibles_resultados if x != jugada[5]]):
            _jugada[0] = fallo1
            _jugada[1] = fallo2
            _jugada[2] = fallo3
            _jugada[3] = fallo4
            _jugada[4] = fallo5
            _jugada[5] = fallo6
            jugadas_con_n_aciertos.append(' '.join(_jugada))

    return jugadas_con_n_aciertos


if __name__ == "__main__":
    jugada = '0-0 0-0 0-0 0-0 0-0 0-0'
    len(jugadas_con_premio(jugada, 5))

