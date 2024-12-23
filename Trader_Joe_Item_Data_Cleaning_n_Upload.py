import pandas as pd
import ast
import os

import pandas as pd
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#Extract necessary category information from the category column data
def extract_category_names(cat_list):
    names = []
    for category in cat_list:
        names.append(category['name'])
    return names

# Load the CSV data into a DataFrame
file_path = 'trader_joes_items.csv'
df = pd.read_csv(file_path)

#Clear all spaces
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df.columns = df.columns.str.strip()
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip()

#Select necessary columns
df = df[
    ['item_title',
     'sku',
     'storeCode',
     'category_hierarchy',
     'sales_size',
     'sales_uom_description',
     'retail_price',
     'fun_tags',
     'item_characteristics']
]

#Build new columns for category and input the extracted category labels
df['category_hierarchy'] = df['category_hierarchy'].apply(ast.literal_eval)
df['category_names'] = df['category_hierarchy'].apply(extract_category_names)

category_names_expanded = df['category_names'].apply(pd.Series)
category_names_expanded.drop(columns=1)
category_names_expanded.drop(columns=[0, 1], inplace=True)

category_names_expanded.columns = [f'category_{i+1}' for i in range(category_names_expanded.shape[1])]

# Concatenate the new columns back to the original DataFrame
df = pd.concat([df, category_names_expanded], axis=1)

# Drop some unecessary columns from the original database
df.drop(columns=['category_hierarchy'], inplace=True)
df.drop(columns=['category_names'], inplace=True)

csv_file_path = 'Cleaned_trader_joes_items.csv'
df.to_csv(csv_file_path, index=False)

# THE FOLLOWING CODE UPLOADS THE CSV DATA TO OUR MONGODB DATABASE
#Connect to the database
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)

# Define database and schema
db = client["Sweet_Violet"]
trader_joes_items_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["item_title", "sku", "storeCode", "sales_size", "sales_uom_description", "retail_price", "fun_tags", "item_characteristics", "category_1", "category_2"],
        "properties": {
            "item_title": {"bsonType": "string"},
            "sku": {"bsonType": "int"},
            "storeCode": {"bsonType": "array", "items": {"bsonType": "int"}},
            "sales_size": {"bsonType": "double"},
            "sales_uom_description": {"bsonType": "string"},
            "retail_price": {"bsonType": "double"},
            "fun_tags": {"bsonType": "array", "items": {"bsonType": "string"}},
            "item_characteristics": {"bsonType": "array", "items": {"bsonType": "string"}},
            "category_1": {"bsonType": "string"},
            "category_2": {"bsonType": "string"},
        }
    }
}

# Create Trader_Joes_Items collection with schema
collection_name = "Trader_Joes_Items"
db.create_collection(collection_name, validator=trader_joes_items_schema)

# Load the csv data into a DataFrame
file_path = 'Cleaned_trader_joes_items.csv'
df = pd.read_csv(file_path)

# Further data cleaning before upload
df.columns = df.columns.str.strip()  # Strip whitespace from column headers

# Ensure data types match the schema
df['sku'] = pd.to_numeric(df['sku'], errors='coerce').fillna(0).astype(int)
df['sales_size'] = pd.to_numeric(df['sales_size'], errors='coerce').fillna(0).astype(float)
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce').fillna(0).astype(float)

# Convert storeCode to list of integers
df['storeCode'] = df['storeCode'].apply(lambda x: list(map(int, str(x).split(','))) if isinstance(x, str) else [x])

# Convert fun_tags and item_characteristics to lists, replacing NaN with empty lists
df['fun_tags'] = df['fun_tags'].apply(lambda x: eval(x) if isinstance(x, str) else [])  # Convert to list or empty list if NaN
df['item_characteristics'] = df['item_characteristics'].apply(lambda x: eval(x) if isinstance(x, str) else [])

# Handle NaN values in fun_tags and item_characteristics
df['fun_tags'] = df['fun_tags'].apply(lambda x: x if isinstance(x, list) else [])
df['item_characteristics'] = df['item_characteristics'].apply(lambda x: x if isinstance(x, list) else [])

# Insert data into Trader_Joes_Items collection
trader_joes_items = df.to_dict(orient='records')
items_collection = db[collection_name]
try:
    items_collection.insert_many(trader_joes_items)
    print("Data inserted successfully!")
except pymongo.errors.BulkWriteError as e:
    print("BulkWriteError:", e.details)
