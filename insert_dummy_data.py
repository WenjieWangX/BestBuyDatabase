import mysql.connector

cnx = mysql.connector.connect(user='com303wwang4', password="ww8735ww",
                              host='136.244.224.221',
                              database='com303fpcw')

cursor = cnx.cursor()

with open("BestBuy_dummy_data.txt", "r") as data_file:
    dic = {}
    for line in data_file:
        fields = line.strip().split('\t')
        if fields[0] != "" and fields[0] != "Table":
            if fields[0] in dic:
                dic[fields[0]].append(fields[1:])
            else:
                dic[fields[0]] = [fields[1:]]

    # brands
    brand_query = "insert into brands(brand_id, brand_name) values (%s, %s)"
    for brand in dic["brands"]:
        query_values = tuple(brand)
        cursor.execute(brand_query, query_values)

    # products
    product_query = "insert into products(product_id, brand_id, product_name, description, price, quantity_in_stock) values (%s, %s, %s, %s, %s, %s)"
    for product in dic["products"]:
        product_values = tuple(product)
        cursor.execute(product_query, product_values)

    # categories
    category_query = "insert into categories(category_id, category_name) values (%s, %s)"
    for category in dic["categories"]:
        category_values = tuple(category)
        cursor.execute(category_query, category_values)

    # products_has_categories
    product_category_query = "insert into products_has_categories(product_id, category_id) values (%s, %s)"
    for product_category in dic["products_has_categories"]:
        product_category_values = tuple(product_category)
        cursor.execute(product_category_query, product_category_values)

    # vendors
    vendor_query = "insert into vendors(vendor_id, vendor_name) values (%s, %s)"
    for vendor in dic["vendors"]:
        vendor_values = tuple(vendor)
        cursor.execute(vendor_query, vendor_values)

    # vendors_has_products
    vendor_product_query = "insert into vendors_has_products(vendor_id, product_id, price) values (%s, %s, %s)"
    for vendor_product in dic["vendors_has_products"]:
        vendor_product_values = tuple(vendor_product)
        cursor.execute(vendor_product_query, vendor_product_values)

    # hours
    hour_query = "insert into hours(hour_id, day, start_time, end_time) values (%s, %s, %s, %s)"
    for hour in dic["hours"]:
        hour_values = tuple(hour)
        cursor.execute(hour_query, hour_values)

    # store address
    store_address_query = "insert into store_address(address_id, street, city, state, zip_code) values (%s, %s, %s, %s, %s)"
    for address in dic["address"]:
        store_address_values = tuple(address)
        cursor.execute(store_address_query, store_address_values)

    # customer address
    customer_address_query = "insert into customer_address(address_id, street, city, state, zip_code) values (%s, %s, %s, %s, %s)"
    for address in dic["address"]:
        customer_address_values = tuple(address)
        cursor.execute(customer_address_query, customer_address_values)

    # stores
    store_query = "insert into stores(store_id, address_id, hour_id) values (%s, %s, %s)"
    for store in dic["stores"]:
        store_values = tuple(store)
        cursor.execute(store_query, store_values)

    # inventory
    inventory_query = "insert into inventory(product_id, store_id, quantity_in_stock, sales) values (%s, %s, %s, %s)"
    for inventory in dic["inventory"]:
        inventory_values = tuple(inventory)
        cursor.execute(inventory_query, inventory_values)

    # cards
    card_query = "insert into cards(card_id, card_type, card_name, card_num, expiration) values (%s, %s, %s, %s, %s)"
    for card in dic["cards"]:
        card_values = tuple(card)
        cursor.execute(card_query, card_values)

    # customers
    customer_query = "insert into customers(customer_id, first_name, last_name, email, phone_number) values (%s, %s, %s, %s, %s)"
    for customer in dic["customers"]:
        customer_values = tuple(customer)
        cursor.execute(customer_query, customer_values)

    # orders
    order_query = "insert into orders(order_id, customer_id, store_id, order_date, total_price) values (%s, %s, %s, %s, %s)"
    for order in dic["orders"]:
        order_values = tuple(order)
        cursor.execute(order_query, order_values)

    # products_has_orders
    product_order_query = "insert into products_has_orders(product_id, order_id, amount) values (%s, %s, %s)"
    for product_order in dic["products_has_orders"]:
        product_order_values = tuple(product_order)
        cursor.execute(product_order_query, product_order_values)

    # customers_has_address
    customer_address_query = "insert into customers_has_address(customer_id, address_id) values (%s, %s)"
    for customer_address in dic["customers_has_address"]:
        customer_address_values = tuple(customer_address)
        cursor.execute(customer_address_query, customer_address_values)

    # address_has_cards
    address_card_query = "insert into address_has_cards(address_id, card_id) values (%s, %s)"
    for address_card in dic["address_has_cards"]:
        address_card_values = tuple(address_card)
        cursor.execute(address_card_query, address_card_values)

    # customers_has_cards
    customer_card_query = "insert into customers_has_cards(customer_id, card_id) values (%s, %s)"
    for customer_card in dic["customers_has_cards"]:
        customer_card_values = tuple(customer_card)
        cursor.execute(customer_card_query, customer_card_values)

cnx.commit()
cursor.close()
cnx.close()
