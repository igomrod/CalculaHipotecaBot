import dataframe_image as dfi


def save_as_image(mortgage_table, max_periods: int, image_path: str):
    df = mortgage_table.head(max_periods)
    dfi.export(df, image_path, table_conversion='matplotlib')
