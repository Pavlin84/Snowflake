import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Snowflake Badge')

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑 Hard-Boiled Free-Range Egg 🍞')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')




# Let's put a pick list here so they can pick the fruit they want to include
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Pear', 'Peach'])

fruit_to_show = my_fruit_list.loc[fruit_selected]

# Display the table on the page.
streamlit.dataframe(fruit_to_show)
streamlit.dataframe(my_fruit_list)

fruit_choice=streamlit.text_input("Whats fruit would you like information about", "kiwi")
streamlit.write("Ypu Chose: " + fruit_choice)

streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruit_normalaized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruit_normalaized)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list:")
streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input("Whats fruit would you like to add", "kiwi")
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values( " + fruit_add + " )")
streamlit.write("Ypu Chose: " + fruit_add)