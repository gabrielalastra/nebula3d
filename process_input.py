import os, sys
from dotenv import load_dotenv
sys.path.append(os.getenv('PYTHONPATH'))
from sqlalchemy import create_engine
import db_connection
load_dotenv()

import webscrapping
import LLM_process


def process_input():
    
    # Replace these variables with your actual database credentials
    username=os.getenv('USERNAME')
    password=os.getenv('PASSWORD')
    host=os.getenv('HOST')
    port=os.getenv('PORT')
    database=os.getenv('DATABASE')

    # Create a SQLAlchemy engine
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')



    df = webscrapping.get_data().head()


    df['blog_title'], df['blog_content'] = zip(*df.apply(lambda row: LLM_process.call_chatgpt(
        title = row['title'],      # Assuming 'model' column is used for 'title'
        brand = row['brand'],      # Replace 'brand' with the actual column name for brand
        review = row['review'],
        material = row['material'],   # Replace 'material' with the actual column name for material
        item_weight = row['item weight'],# Replace 'item_weight' with the actual column name for item weight
        color = row['color'],      # Replace 'color' with the actual column name for color
        price = row['price'],      # Price
        temperature=0.7,   # Default value for temperature
        max_tokens=150,    # Default value for max_tokens
        model="gpt-3.5-turbo"  # Default model
    ), axis=1)) 

    df.rename(columns={"item weight":"item_weight"},inplace=True)

    db_connection.upsert_dataframe(df, 'filaments', engine)

