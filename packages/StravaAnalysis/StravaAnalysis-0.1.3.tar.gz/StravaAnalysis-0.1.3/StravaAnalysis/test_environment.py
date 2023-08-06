import data_aggregator as da
import data_import as dr

USERNAME = "jer.bouma@gmail.com"
PASSWORD = "T1w09&oT9Ku73@uNlW!"
CLIENT_ID = 36132
CLIENT_SECRET = "00fafa27165459ae7035cbead81956e192a0bc30"

# Inititalize Client and Collect all General Data and Streams Data
general_data, streams_data = da.data_aggregator(USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, overwrite=True)

# Read Specific files
# general_data = dr.import_general_data()
# all_streams_data = dr.import_streams_data()
# streams_data_for_one = dr.import_streams_data("554237255.json", convert_to_df=True)

# Export all Data to JSON Files
da.data_exporter(general_data, streams_data)
