from faker import Faker

restid = []
custid = []
orderid = []
delivery_Personid = []
customerdateinsertquery = []
restaurantdateinsertquery = []
orderdatainsertquery = []
deliverypersoninsertquery = []
orderdeliverydatainsertquery = []

restaurant_Names = ['Paradise biryani', 'Sangeetha veg restaurant', 'McDonalds', "KFC", 'Adyar anandha bhavan',
                    'Downtown']
cusine_type = ['Italian', 'Asian', 'Mexican', "Korean", 'Continental', 'South indian']
cusines = ['Fried rice', 'Idly', 'Dosa', 'Biryani', 'Pizza', 'Chappathi', 'Parotta', 'Pongal', 'vada', 'Poori',
           'Channa batura', 'Naan', 'Roti', 'Veg meals', 'Non veg meals']
rating = [1, 2, 3, 4, 5]
status = ['Pending', 'Delivered', 'Cancelled']
payment_mode = ['Credit Card', 'Cash', 'UPI']
vehicle_Type = ['Bike', 'Car']


class ZomatoDataExtraction:
    def __init__(self):
        self.fake = Faker()


def createCustomerData(x, schema):
    customerData = {}
    customerdateinsertquery = []
    fake = Faker()
    for i in range(x):
        customerData[i] = {}
        customerid = i + 1

        customerData[i]['customer_id'] = customerid
        custid.append(customerid)
        customerData[i]['name'] = fake.name()
        customerData[i]['email'] = fake.email()
        customerData[i]['phone'] = fake.phone_number()
        customerData[i]['location'] = fake.address()
        customerData[i]['signup_date'] = fake.date_this_decade()
        customerData[i]['is_premium'] = fake.boolean()
        customerData[i]['preferred_cuisine'] = fake.random_element(cusines)
        customerData[i]['total_orders'] = fake.random_int(min=0, max=100)
        customerData[i]['average_rating'] = fake.random_element(rating)

        # build insert query
        customerdateinsertquery.append('INSERT INTO ' + schema + '.customers VALUES(' + str(
            customerData[i]['customer_id']) + ',"' + customerData[i]['name'] + '","' + customerData[i][
                                           'email'] + '","' + str(
            customerData[i]['phone']) + '","' + customerData[i]['location'] + '","' + str(
            customerData[i]['signup_date']) + '",' + str(
            customerData[i]['is_premium']) + ',"' + customerData[i]['preferred_cuisine'] + '",' + str(
            customerData[i]['total_orders']) + ',' + str(customerData[i]['average_rating']) + ')')

    return customerdateinsertquery


def createRestaurantData(x, schema):
    restaurant = {}
    restaurantdateinsertquery = []
    fake = Faker()
    for i in range(x):
        restaurant[i] = {}
        restId = i + 1
        restaurant[i]['restaurant_id'] = restId
        restid.append(restId)
        restaurant[i]['name'] = fake.random_element(restaurant_Names) + '_' + str(i)
        restaurant[i]['cuisine_type'] = fake.random_element(cusine_type)
        restaurant[i]['location'] = fake.street_address()
        restaurant[i]['owner_name'] = fake.name()
        restaurant[i]['average_delivery_time'] = fake.random_int(min=15, max=45)
        restaurant[i]['contact_number'] = fake.phone_number()
        restaurant[i]['rating'] = fake.random_element(rating)
        restaurant[i]['total_orders'] = fake.random_int(min=1, max=10000)
        restaurant[i]['is_active'] = fake.boolean()

        # build insert query
        restaurantdateinsertquery.append('INSERT INTO ' + schema + '.restaurants VALUES(' + str(
            restaurant[i]['restaurant_id']) + ',"' + restaurant[i]['name'] + '","' + restaurant[i][
                                             'cuisine_type'] + '","' + restaurant[i]['location'] + '","' +
                                         restaurant[i]['owner_name'] + '","' + str(
            restaurant[i]['average_delivery_time']) + '","' + str(restaurant[i]['contact_number']) + '","' + str(
            restaurant[i]['rating']) + '",' + str(restaurant[i]['total_orders']) + ',' + str(
            restaurant[i]['is_active']) + ')')
    return restaurantdateinsertquery


def createOrderData(x, schema):
    order = {}
    orderdatainsertquery = []
    fake = Faker()
    for i in range(x):
        order[i] = {}
        orderId = i + 1
        order[i]['order_id'] = orderId
        orderid.append(orderId)

        order[i]['customer_id'] = fake.random_element(custid)
        order[i]['restaurant_id'] = fake.random_element(restid)
        order[i]['order_date'] = fake.date_time_this_year()
        order[i]['delivery_time'] = fake.random_int(min=15, max=45)
        order[i]['status'] = fake.random_element(status)
        order[i]['total_amount'] = fake.random_int(min=100, max=5000)
        order[i]['payment_mode'] = fake.random_element(payment_mode)
        order[i]['discount_applied'] = fake.random_int(min=50, max=150)
        order[i]['feedback_rating'] = fake.random_element(rating)

        # build insert query
        orderdatainsertquery.append('INSERT INTO ' + schema + '.orders VALUES(' + str(
            order[i]['order_id']) + ',"' + str(order[i]['customer_id']) + '","' + str(
            order[i]['restaurant_id']) + '","' + str(order[i]['order_date']) + '",' + str(
            order[i]['delivery_time']) + ',"' + order[i]['status'] + '","' + str(order[i]['total_amount']) + '","' +
                                    order[i]['payment_mode'] + '",' + str(order[i]['discount_applied']) + ',' + str(
            order[i]['feedback_rating']) + ')')
    return orderdatainsertquery


def createDeliveryPersonData(x, schema):
    deliveryPerson = {}
    deliverypersoninsertquery = []
    fake = Faker()
    for i in range(x):
        deliveryPerson[i] = {}
        deliveryPersonid = i + 1
        deliveryPerson[i]['delivery_person_id'] = deliveryPersonid
        delivery_Personid.append(deliveryPersonid)

        deliveryPerson[i]['name'] = fake.name()
        deliveryPerson[i]['contact_number'] = fake.phone_number()
        deliveryPerson[i]['vehicle_type'] = fake.random_element(vehicle_Type)
        deliveryPerson[i]['total_deliveries'] = fake.random_int(min=1, max=1000)
        deliveryPerson[i]['average_rating'] = fake.random_element(rating)
        deliveryPerson[i]['location'] = fake.street_address()

        # build insert query
        # print('INSERT INTO '+configs.get('schemaName').data+'.delivery_person VALUES('+str(deliveryPerson[i]['delivery_person_id'])+',"'+deliveryPerson[i]['name']+'","'+deliveryPerson[i]['contact_number']+'","'+deliveryPerson[i]['vehicle_type']+'", '+str(deliveryPerson[i]['total_deliveries'])+', '+str(deliveryPerson[i]['average_rating'])+',"'+deliveryPerson[i]['location']+'")')
        deliverypersoninsertquery.append(
            'INSERT INTO ' + schema + '.delivery_person VALUES(' + str(
                deliveryPerson[i]['delivery_person_id']) + ',"' + deliveryPerson[i]['name'] + '","' + deliveryPerson[i][
                'contact_number'] + '","' + deliveryPerson[i]['vehicle_type'] + '", ' + str(
                deliveryPerson[i]['total_deliveries']) + ', ' + str(deliveryPerson[i]['average_rating']) + ',"' +
            deliveryPerson[i]['location'] + '")')
    return deliverypersoninsertquery


def createOrderDeliveryData(x, schema):
    order_delivery = {}
    orderdeliverydatainsertquery = []
    fake = Faker()
    for i in range(x):
        order_delivery[i] = {}

        order_delivery[i]['delivery_id'] = i + 1
        order_delivery[i]['order_id'] = orderid[i]
        order_delivery[i]['delivery_person_id'] = delivery_Personid[i]
        order_delivery[i]['delivery_status'] = fake.random_element(status)
        order_delivery[i]['distance'] = fake.random_int(min=1, max=20)
        order_delivery[i]['delivery_time'] = fake.random_int(min=10, max=60)
        order_delivery[i]['estimated_time'] = fake.random_int(min=10, max=60)
        order_delivery[i]['delivery_fee'] = fake.random_int(min=50, max=150)
        order_delivery[i]['vehicle_type'] = fake.random_element(vehicle_Type)

        orderdeliverydatainsertquery.append(
            'INSERT INTO ' + schema + '.deliveries VALUES(' + str(
                order_delivery[i]['delivery_id']) + ',' + str(order_delivery[i]['order_id']) + ',' + str(
                order_delivery[i]['delivery_person_id']) + ',"' + order_delivery[i]['delivery_status'] + '", ' + str(
                order_delivery[i]['distance']) + ', ' + str(order_delivery[i]['delivery_time']) + ',' + str(
                order_delivery[i]['estimated_time']) + ',' + str(order_delivery[i]['delivery_fee']) + ',"' +
            order_delivery[i]['vehicle_type'] + '")')

    return orderdeliverydatainsertquery
