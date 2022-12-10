from src.data.get_data import get_prob_tables
from src.features.build_features import construccion_probabilidades, feature_engineering
import time


def main(jornada: str, recaudacion_esperada: float, bote: float):
    """construcción de la tabla principal a partir de las probabilidades reales y estimadas

    Args:
        jornada: jornada actual
        recaudacion_esperada: recaudación esperado en la jornada
        bote: bote de la jornada

    Returns:
        None

    """

    print(time.strftime("%H:%M:%S", time.localtime()))
    print('Scrapeando y creando tablas de probabilidades reales y estimadas...')
    real, estimado = get_prob_tables(jornada)
    print('% reales: \n')
    print(real)
    print('% estimados: \n')
    print(estimado)

    print(time.strftime("%H:%M:%S", time.localtime()))
    print('Calculando probabilidad real y estimada de cada jugada')
    df = construccion_probabilidades(real, estimado)

    print(time.strftime("%H:%M:%S", time.localtime()))
    print('Calculando variables de ranking de probabilidad, de acertantes y premios esperados, y de esperanza')
    df = feature_engineering(df, recaudacion_esperada, bote)

    print(time.strftime("%H:%M:%S", time.localtime()))
    print('Guardando datos')
    real.to_csv(f"data/intermediate/22-23/real_{jornada.lower().replace(' ', '_')}.csv")  # TODO: decidir formato jornada (poner solo el numero)
    estimado.to_csv(f"data/intermediate/22-23/estimado_{jornada.lower().replace(' ', '_')}.csv")
    df.to_pickle(f"data/processed/22-23/df_{jornada.lower().replace(' ', '_')}.pkl")


if __name__ == "__main__":
    main("JORNADA 32", recaudacion_esperada=100_000, bote=409_490.80)

