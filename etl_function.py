import pandas as pd
from datetime import date, timedelta

def etl(df,fecha):
    """
    Realiza una transformación de datos (Extract, Transform, Load) en un DataFrame.
    Parámetros:
    df (DataFrame): El DataFrame original que contiene los datos a transformar.
    fecha (str or datetime.date): La fecha para la cual se desea realizar la transformación.
    Returns:
    DataFrame: Un nuevo DataFrame que contiene los datos transformados para la fecha especificada.
    """
    #E- Extracción de DF del CSV
    data = df
    #T- Transformación:
    ### Modificar columnas originales. 
    data['Created'] = pd.to_datetime(data['Created'])
    data['fecha'] = data['Created'].dt.date
    data['hora'] = data['Created'].dt.strftime('%H:%M')
    data = data.drop('Created', axis=1)
    data = data[['fecha', 'hora', 'Student email', 'Teacher email', 'Question Title', 'Question','Points', 'Comments']]
    #Convertir a DF por columnas:
    pivot_df = data.pivot_table(values=['Points','Comments'], index=['fecha','hora','Teacher email', 'Student email'], columns='Question Title', aggfunc='sum')
    columns_to_drop = [
        ('Points', 'Any other comments?'),
        ('Points', 'How do you rate the class?'),
        ('Comments', 'I would take class with them again'),
        ('Comments', 'Their wifi, audio, and video was good'),
        ('Comments', 'They are good at teaching'),
        ('Comments', 'They made the class enjoyable'),
        ('Comments', 'They understood what I wanted')
    ]
    pivot_df = pivot_df.drop(columns_to_drop, axis=1)
    pivot_df.columns = pivot_df.columns.droplevel(level=0)
    pivot_df.columns.name = None
    pivot_df = pivot_df.reset_index()
    #Llenar los valores NaN
    replace_hyphen = ['Any other comments?','How do you rate the class?']
    pivot_df[replace_hyphen] = pivot_df[replace_hyphen].fillna('-')
    replace_0 = ['I would take class with them again','Their wifi, audio, and video was good','They are good at teaching','They made the class enjoyable','They understood what I wanted']
    pivot_df[replace_0] = pivot_df[replace_0].fillna(0)
    # L- Generar el archivo para cargar. 
    data_fecha = fecha
    dataayer = pivot_df[pivot_df['fecha'] == data_fecha]
    return dataayer
