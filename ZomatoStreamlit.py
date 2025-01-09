import streamlit as st
import mysql.connector
from com.zomato.ZomatoDataExtraction import createCustomerData, createRestaurantData, createOrderData, \
    createDeliveryPersonData, createOrderDeliveryData, status
import pandas as pd
import Credentials as cr

st.set_page_config(layout="wide")
# Variable declaration
schemaName = ''
st.image('zomato_banner.png', width=1300)
# form to get schema details
with st.form(key='db_form'):
    st.markdown('<div style="text-align: center;"><b>Create schema</b></div>', unsafe_allow_html=True)
    schemaName = st.text_input('Enter the schema name')
    dbDetailsSubmtBtn = st.form_submit_button('Create DB and Populate data')
    css = """
    <style>
        [data-testid="stForm"] {
            background: LightBlue;
        }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

with st.form(key='sights_form'):
    st.markdown('<div style="text-align: centre;"><b>App Insights</b></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        showInsightsBtn = st.form_submit_button('Show Insights')
    with col2:
        moreInsigths_btn = st.form_submit_button('More Insights')
    css = """
    <style>
        [data-testid="stForm"] {
            background: LightBlue;
        }
    </style>
    """

    st.write(css, unsafe_allow_html=True)

db_connection = None
db_cursor = None
customerData = {}
restaurant_data = {}
order_data = {}
deliveryPerson_Data = {}
delivery_data = {}

# Connection Establishment
db_connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password)
db_cursor = db_connection.cursor()

if dbDetailsSubmtBtn:

    if (len(schemaName) == 0):
        st.error('Please enter a schema name')
    else:

        try:
            createSchema = "CREATE DATABASE " + "`" + schemaName + "`;"
            db_cursor.execute(createSchema)
            print("created schema")

            db_cursor.execute(
                "CREATE TABLE " + schemaName + ".customers (customer_id INTEGER(10) PRIMARY KEY, name VARCHAR(50), email VARCHAR(35), phone VARCHAR(30), location VARCHAR(100), signup_date datetime, is_premium boolean, preferred_cuisine VARCHAR(25), total_orders INTEGER(5), average_rating INTEGER(5));")
            db_cursor.execute(
                "CREATE TABLE " + schemaName + ".Restaurants (restaurant_id INTEGER(10) PRIMARY KEY, name VARCHAR(50), cuisine_type VARCHAR(25),location VARCHAR(100), owner_name VARCHAR(50), average_delivery_time INTEGER(4), contact_number VARCHAR(30), rating INTEGER(5), total_orders INTEGER(5), is_active boolean);")
            db_cursor.execute(
                "CREATE TABLE " + schemaName + ".orders (order_id INTEGER(10) PRIMARY KEY, customer_id INTEGER(10), restaurant_id INTEGER(10), order_date DATETIME, delivery_time INTEGER(5), status VARCHAR(15), total_amount DECIMAL(10,2), payment_mode VARCHAR(15), discount_applied DECIMAL(10,2), feedback_rating INTEGER(5), FOREIGN KEY  (customer_id) REFERENCES customers(customer_id), FOREIGN KEY  (restaurant_id) REFERENCES Restaurants(restaurant_id));")
            db_cursor.execute(
                "CREATE TABLE " + schemaName + ".delivery_person (delivery_person_id INTEGER(10) PRIMARY KEY, name VARCHAR(50), contact_number VARCHAR(30), vehicle_type VARCHAR(15), total_deliveries INTEGER(5), average_rating INTEGER(5), location VARCHAR(150));")
            db_cursor.execute(
                "CREATE TABLE " + schemaName + ".deliveries (delivery_id INTEGER(10) PRIMARY KEY, order_id INTEGER(10), delivery_person_id INTEGER(10), delivery_status VARCHAR(15), distance INTEGER(5), delivery_time INTEGER(5), estimated_time INTEGER(5), delivery_fee INTEGER(5), vehicle_type VARCHAR(10),  FOREIGN KEY  (order_id) REFERENCES Orders(order_id), FOREIGN KEY  (delivery_person_id) REFERENCES Delivery_person(delivery_person_id));")
        except:
            st.error('Schema name already exists')

        try:
            # Insert customer table datas
            customerData = createCustomerData(100, schemaName)
            for i in customerData:
                db_cursor.execute(i)

            db_connection.commit()

            # Insert restaurant table datas
            restaurant_data = createRestaurantData(100, schemaName)
            for i in restaurant_data:
                db_cursor.execute(i)

            db_connection.commit()

            # Insert order table datas
            order_data = createOrderData(100, schemaName)
            for i in order_data:
                db_cursor.execute(i)

            db_connection.commit()

            # Insert deliveryPerson table datas
            deliveryPerson_Data = createDeliveryPersonData(100, schemaName)
            for i in deliveryPerson_Data:
                db_cursor.execute(i)

            db_connection.commit()

            # Insert orderDelivery table datas
            delivery_data = createOrderDeliveryData(100, schemaName)
            for i in delivery_data:
                db_cursor.execute(i)

            db_connection.commit()
            st.write('Datas created successfully!!')
        except:
            st.error('Some backend exception happened while creating datas!!')


def fetchDelayedDelivery():
    status = "'Delivered'"
    fetchQuery = 'SELECT b.name, a.DELIVERY_TIME , a.ESTIMATED_TIME FROM ' + schemaName + '.DELIVERIES a, ' + schemaName + '.delivery_person b WHERE b.delivery_person_id = a.delivery_person_id and a.delivery_status=' + status + ' AND a.DELIVERY_TIME > a.ESTIMATED_TIME' + ";"
    db_cursor.execute(fetchQuery)
    delayed_Delivery_Data = db_cursor.fetchall()
    return delayed_Delivery_Data


def showRestaurantPerformance():
    fetchQuery = "SELECT a.STATUS, b.name FROM " + schemaName + ".ORDERS a, sample.restaurants b WHERE b.restaurant_id = a.restaurant_id and a.STATUS in ('Pending', 'Delivered', 'Cancelled');"
    db_cursor.execute(fetchQuery)
    showRestaurantPerformanceData = db_cursor.fetchall()
    return showRestaurantPerformanceData


def fetchorderPeakTime():
    fetchQuery = "SELECT HOUR(ORDER_DATE) AS Time_Hours,  COUNT(*) AS MAX_ORDERS FROM " + schemaName + ".ORDERS GROUP BY HOUR(ORDER_DATE) ORDER BY MAX_ORDERS DESC;"
    db_cursor.execute(fetchQuery)
    fetchorderPeakTimeData = db_cursor.fetchall()
    return fetchorderPeakTimeData


def fetchDeliveryPersonPerfomance():
    fetchQuery = "SELECT NAME, VEHICLE_TYPE, TOTAL_DELIVERIES, AVERAGE_RATING FROM " + schemaName + ".DELIVERY_PERSON;"
    db_cursor.execute(fetchQuery)
    fetchorderPeakTimeData = db_cursor.fetchall()
    return fetchorderPeakTimeData


def fetchCancelledOrders():
    fetchQuery = "SELECT b.name as customer_name, c.name from " + schemaName + ".orders a, " + schemaName + ".customers b, " + schemaName + ".restaurants c where b.customer_id=a.customer_id and c.restaurant_id = a.restaurant_id and a.status = 'Cancelled';"
    db_cursor.execute(fetchQuery)
    fetchcancelledData = db_cursor.fetchall()
    return fetchcancelledData


def fetchCustomerPreferedRestaurant():
    fetchQuery = "SELECT name,location  from " + schemaName + ".restaurants WHERE RESTAURANT_ID=(select restaurant_id from " + schemaName + ".orders group by restaurant_id order by count(*) desc LIMIT 1);"
    db_cursor.execute(fetchQuery)
    fetchCustomerPreferedRestaurant = db_cursor.fetchall()
    return fetchCustomerPreferedRestaurant


def fetchMostOrderedcustomers():
    fetchQuery = "SELECT a.CUSTOMER_ID, b.name,  SUM(a.TOTAL_AMOUNT) as GREATER FROM " + schemaName + ".ORDERS a, " + schemaName + ".CUSTOMERS b WHERE b.CUSTOMER_ID = a.CUSTOMER_ID GROUP BY CUSTOMER_ID ORDER BY GREATER DESC LIMIT 10;"
    db_cursor.execute(fetchQuery)
    fetchMostOrderedcustomers = db_cursor.fetchall()
    return fetchMostOrderedcustomers


if showInsightsBtn:

    try:
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Delayed deliveries", "Performance of restaurants", "Peak order timings", "Delivery person performance"])

        with tab1:
            delayed_Delivery = fetchDelayedDelivery()
            df = pd.DataFrame(delayed_Delivery, columns=['name', 'DELIVERY_TIME', 'ESTIMATED_TIME'])
            st.bar_chart(df, x='name', y=['DELIVERY_TIME', 'ESTIMATED_TIME'], x_label='Delivery person',
                         y_label='Delivery time')
        with tab2:
            delayed_Delivery = showRestaurantPerformance()
            df = pd.DataFrame(delayed_Delivery, columns=['STATUS', 'name'])
            st.line_chart(df, x='name', y=['STATUS', 'name'], x_label='Restaurant name',
                          y_label='Order Status', width=500)

        with tab3:
            orde_peak_time = fetchorderPeakTime()
            df = pd.DataFrame(orde_peak_time, columns=['Time_Hours', 'MAX_ORDERS'])
            st.line_chart(df, x='Time_Hours', y='MAX_ORDERS', x_label='Order Timings',
                          y_label='Maximum Orders', width=500)
        with tab4:
            del_per_perf_data = fetchDeliveryPersonPerfomance()
            df = pd.DataFrame(del_per_perf_data, columns=['NAME', 'VEHICLE_TYPE', 'TOTAL_DELIVERIES', 'AVERAGE_RATING'])
            st.bar_chart(df, x='NAME', y='AVERAGE_RATING', x_label='Delivery Person Name',
                         y_label='Rating', color=["#eb5e34"], width=500)
    except:
        st.error('Something went wrong in backend!! Please make sure to create database and populate data')

if moreInsigths_btn:
    try:
        tab5, tab6, tab7 = st.tabs(
            ["Tracking canceled Orders", "Customer Preferred restaurants", "Top orders customers"])

        with tab5:
            fetchCancelledOrder_Data = fetchCancelledOrders()
            df = pd.DataFrame(fetchCancelledOrder_Data, columns=['customer_name', 'name'])
            st.line_chart(df, x='name', y='customer_name', x_label='Restaurant name',
                          y_label='customer name', width=500)

        with tab6:
            fetchCustomerPreferedRestaurant_data = fetchCustomerPreferedRestaurant()
            df = pd.DataFrame(fetchCustomerPreferedRestaurant_data, columns=['name', 'location'])
            st.bar_chart(df, x='name', y='location', x_label='Restaurant name',
                         width=500)

        with tab7:
            fetchMostOrderedcustomers_data = fetchMostOrderedcustomers()
            df = pd.DataFrame(fetchMostOrderedcustomers_data, columns=['CUSTOMER_ID', 'name', 'GREATER'])
            st.scatter_chart(df, x='name', y='GREATER', x_label='Customer name', y_label='Order Amount')
    except:
        st.error('Something went wrong in backend!! Please make sure to create database and populate data')
