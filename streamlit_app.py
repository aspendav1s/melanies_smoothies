# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas



# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be ", name_on_order)



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)
    my_insert_stmt = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS (NAME_ON_ORDER, INGREDIENTS) VALUES ('{name_on_order}', '{ingredients_string}')"""
    st.write(my_insert_stmt)

    
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order , icon="✅")

#New section to import



if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        





