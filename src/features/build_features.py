from itertools import combinations, product
import pandas as pd


def construccion_probabilidades(real: pd.DataFrame, estimado: pd.DataFrame) -> pd.DataFrame:
    """
    construye el df de probabilidades por jugada dado los datos reales y estimados

    :param real: pd.DataFrame con las probabilidades reales scrapeadas en reales_estimados()
    :param estimado: pd.DataFrame con las probabilidades estimadas scrapeadas en reales_estimados()
    :return: pd.Dataframe con las probabilidades reales y estimados para cada una de las 3**14 jugadas
    """

    # todas las jugadas
    jugadas = [' '.join(j) for j in product(['-'.join(i) for i in product("012M", repeat=2)], repeat=6)]

    # probabilidades reales
    probabilidades6real = [a * b * c * d * e * f for a, b, c, d, e, f in
                           product(real.iloc[0], real.iloc[1], real.iloc[2],
                                   real.iloc[3], real.iloc[4], real.iloc[5])]

    probabilidades0real = [(1 - a) * (1 - b) * (1 - c) * (1 - d) * (1 - e) * (1 - f) for a, b, c, d, e, f in
                           product(real.iloc[0], real.iloc[1], real.iloc[2],
                                   real.iloc[3], real.iloc[4], real.iloc[5])]
    zipped6 = lambda: zip(probabilidades6real, product(real.iloc[0], real.iloc[1], real.iloc[2],
                                                       real.iloc[3], real.iloc[4], real.iloc[5]))

    zipped0 = lambda: zip(probabilidades0real, product(real.iloc[0], real.iloc[1], real.iloc[2],
                                                       real.iloc[3], real.iloc[4], real.iloc[5]))

    probabilidades5real = [sum([(prob6 / variante) * (1 - variante) for variante in (a, b, c, d, e, f)])
                           for prob6, (a, b, c, d, e, f) in zipped6()]

    probabilidades4real = [
        sum([(prob6 / (variante1 * variante2)) * (1 - variante1) * (1 - variante2) for variante1, variante2 in
             combinations([a, b, c, d, e, f], 2)])
        for prob6, (a, b, c, d, e, f) in zipped6()]

    probabilidades3real = [
        sum([(prob6 / (variante1 * variante2 * variante3)) * (1 - variante1) * (1 - variante2) * (1 - variante3) for
             variante1, variante2, variante3 in combinations([a, b, c, d, e, f], 3)])
        for prob6, (a, b, c, d, e, f) in zipped6()]

    probabilidades2real = [sum([(prob6 / (variante1 * variante2 * variante3 * variante4)) * (1 - variante1) * (
            1 - variante2) * (1 - variante3) * (1 - variante4) for variante1, variante2, variante3, variante4 in
                                combinations([a, b, c, d, e, f], 4)])
                           for prob6, (a, b, c, d, e, f) in zipped6()]

    probabilidades1real = [sum([(prob0 / (1 - variante)) * variante for variante in (a, b, c, d, e, f)])
                           for prob0, (a, b, c, d, e, f) in zipped0()]

    # probabilidades estimadas
    probabilidades6est = [a * b * c * d * e * f for a, b, c, d, e, f in
                          product(estimado.iloc[0], estimado.iloc[1], estimado.iloc[2],
                                  estimado.iloc[3], estimado.iloc[4], estimado.iloc[5])]

    probabilidades0est = [(1 - a) * (1 - b) * (1 - c) * (1 - d) * (1 - e) * (1 - f) for a, b, c, d, e, f in
                          product(estimado.iloc[0], estimado.iloc[1], estimado.iloc[2],
                                  estimado.iloc[3], estimado.iloc[4], estimado.iloc[5])]

    zipped6 = lambda: zip(probabilidades6est, product(estimado.iloc[0], estimado.iloc[1], estimado.iloc[2],
                                                      estimado.iloc[3], estimado.iloc[4], estimado.iloc[5]))

    zipped0 = lambda: zip(probabilidades0est, product(estimado.iloc[0], estimado.iloc[1], estimado.iloc[2],
                                                      estimado.iloc[3], estimado.iloc[4], estimado.iloc[5]))

    probabilidades5est = [sum([(prob6 / variante) * (1 - variante) for variante in (a, b, c, d, e, f)])
                          for prob6, (a, b, c, d, e, f) in zipped6()]

    probabilidades4est = [
        sum([(prob6 / (variante1 * variante2)) * (1 - variante1) * (1 - variante2) for variante1, variante2 in
             combinations([a, b, c, d, e, f], 2)])
        for prob6, (a, b, c, d, e, f) in zipped6()]
    probabilidades3est = [
        sum([(prob6 / (variante1 * variante2 * variante3)) * (1 - variante1) * (1 - variante2) * (1 - variante3) for
             variante1, variante2, variante3 in combinations([a, b, c, d, e, f], 3)])
        for prob6, (a, b, c, d, e, f) in zipped6()]
    probabilidades2est = [sum([(prob6 / (variante1 * variante2 * variante3 * variante4)) * (1 - variante1) * (
            1 - variante2) * (1 - variante3) * (1 - variante4) for variante1, variante2, variante3, variante4 in
                               combinations([a, b, c, d, e, f], 4)])
                          for prob6, (a, b, c, d, e, f) in zipped6()]
    probabilidades1est = [sum([(prob0 / (1 - variante)) * variante for variante in (a, b, c, d, e, f)])
                          for prob0, (a, b, c, d, e, f) in zipped0()]

    d = {'Jugada': jugadas,
         'prob_est6': probabilidades6est, 'prob_est5': probabilidades5est,
         'prob_est4': probabilidades4est, 'prob_est3': probabilidades3est,
         'prob_est2': probabilidades2est, 'prob_est1': probabilidades1est,
         'prob_est0': probabilidades0est,
         'prob_real6': probabilidades6real, 'prob_real5': probabilidades5real,
         'prob_real4': probabilidades4real, 'prob_real3': probabilidades3real,
         'prob_real2': probabilidades2real, 'prob_real1': probabilidades1real,
         'prob_real0': probabilidades0real,
         }

    return pd.DataFrame(d)


def feature_engineering(df: pd.DataFrame, recaudacion_esperada, bote) -> pd.DataFrame:
    """

    Args:
        df (pd.DataFrame): añade varias variables al df construido en construccion_probabilidades()
        recaudacion_esperada (float): recaudación esperado en la jornada
        bote (float): bote de la jornada

    Returns:
        pd.DataFrame con las nuevas variables

    """
    jugadas_esperadas = recaudacion_esperada  # En el quinigol cada jugada vale 1€ por lo que las jugadas esperadas
    # coinciden con la recaudacion

    # Ranking de probabilidad de 6 aciertos según reales y estimadas
    df['rank_est6'] = df['prob_est6'].rank(method='first', ascending=False).astype(int)
    df['rank_real6'] = df['prob_real6'].rank(method='first', ascending=False).astype(int)

    # Acertantes esperados por categoría
    df['acertantes_esperados6'] = round(df.prob_est6 * jugadas_esperadas, 2)
    df['acertantes_esperados5'] = round(df.prob_est5 * jugadas_esperadas, 2)
    df['acertantes_esperados4'] = round(df.prob_est4 * jugadas_esperadas, 2)
    df['acertantes_esperados3'] = round(df.prob_est3 * jugadas_esperadas, 2)
    df['acertantes_esperados2'] = round(df.prob_est2 * jugadas_esperadas, 2)

    # Premios esperados por categoría
    df['premio_esperado6'] = round((recaudacion_esperada * 0.1 + bote) / df.acertantes_esperados6.apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado5'] = round(recaudacion_esperada * 0.09 / df.acertantes_esperados5.apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado4'] = round(recaudacion_esperada * 0.08 / df.acertantes_esperados4.apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado3'] = round(recaudacion_esperada * 0.08 / df.acertantes_esperados3.apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado2'] = round(recaudacion_esperada * 0.20 / df.acertantes_esperados2.apply(lambda x: 1 if x < 1 else x), 2)

    # Esperanza premio
    df['EM6'] = df.prob_real6 * ((recaudacion_esperada * 0.1 + bote) / (df.acertantes_esperados6 + 1))
    df['rank_EM6'] = df.EM6.rank(method='first', ascending=False).astype(int)

    return df
