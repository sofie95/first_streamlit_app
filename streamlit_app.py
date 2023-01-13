import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

#Get data
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

st.title('My Mom\'s New Healthy Diner')

st.header('Breakfast Favorites')

st.text('🥣 Omega 3 & Blueberry Oatmeal')

st.text('🥗 Kale, Spinach & Rocket Smoothie')

st.text('🐔 Hard-Boiled Free-Range Egg')

st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)


#create the repeatable code block called function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
  
#New section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please selcet a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)


except URLError as e:
  st.error()


#don't run past here while trouble shooting
st.stop()

#Snowflake code
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# try to add another entry box
fruit_add = st.text_input('What fruit would you like to add?','jackfruit')
st.write('Thanks for adding ', fruit_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

