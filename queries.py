import mysql.connector

cnx = mysql.connector.connect(user='com303wwang4', password="ww8735ww",
                              host='136.244.224.221',
                              database='com303fpcw')

cursor = cnx.cursor()

# What are the 20 top-selling products at each store?
queries1 = """
with store_product_sales as (
  select s.store_id, p.product_id, p.product_name, i.sales,
        rank() over (partition by s.store_id order by i.sales desc) as sales_rank
  from stores s, products p, inventory i
  where s.store_id = i.store_id and
  p.product_id = i.product_id
  group by s.store_id, p.product_id
)
select store_id, product_id, product_name, sales, sales_rank
from store_product_sales
where sales_rank <= 20
order by store_id, sales DESC;
"""
# What are the 20 top-selling products in each state?
queries2 = """
with state_product_sales as (
  select s.store_id, p.product_id, p.product_name, i.sales, a.state,
  rank() over (partition by a.state order by i.sales desc) as sales_rank
  from stores s, products p, inventory i, store_address a
  where s.store_id = i.store_id and
  p.product_id = i.product_id and
  s.store_address_id = a.store_address_id
  group by s.store_id, a.state, p.product_id
)
select store_id, product_id, product_name, sales, state, sales_rank
from state_product_sales
where sales_rank <= 20
order by store_id, sales DESC;
"""

# What are the 5 stores with the most sales so far this year?
queries3 = """
SELECT s.store_id, SUM(o.total_price) AS total_sales
FROM stores s
INNER JOIN orders o ON s.store_id = o.store_id
WHERE YEAR(o.order_date) = 2023
GROUP BY s.store_id
ORDER BY total_sales DESC
LIMIT 5;
"""

# In how many stores does Coke outsell Pepsi? (Or, a similar query for enterprises that don’t sell soda.)
queries4 = """
select count(distinct i1.store_id)
from inventory as i1 join products as p1 on (i1.product_id = p1.product_id),
	inventory as i2 join products as p2 on (i2.product_id = p2.product_id)
where p1.product_name = "Apple MacBook Pro" and
	p2.product_name = "Apple Mac Air" and
    i1.store_id = i2.store_id and
	i1.sales > i2.sales;
"""

# What are the top 3 types of product that customers buy in addition to milk? (Or similar question for nonfood enterprises.)
queries5 = """
SELECT c.category_name, COUNT(*) AS total_sales
FROM products p
JOIN products_has_categories pc ON p.product_id = pc.product_id
JOIN categories c ON pc.category_id = c.category_id
JOIN products_has_orders po ON p.product_id = po.product_id
JOIN orders o ON po.order_id = o.order_id
JOIN customers c2 ON o.customer_id = c2.customer_id
WHERE c2.customer_id IN (
	SELECT DISTINCT o.customer_id
	FROM orders o
	JOIN products_has_orders po ON o.order_id = po.order_id
	JOIN products p ON po.product_id = p.product_id
	JOIN products_has_categories pc ON p.product_id = pc.product_id
	WHERE p.product_name = 'Apple Macbook Pro'
)
AND p.product_name != 'Apple Macbook Pro'
GROUP BY c.category_name
ORDER BY total_sales DESC
LIMIT 3;
"""

queries6 = """
SELECT DISTINCT v.vendor_name
FROM vendors v
INNER JOIN vendors_has_products vp ON v.vendor_id = vp.vendor_ID
INNER JOIN products p ON vp.product_ID = p.product_id
WHERE vp.price > 1000;
"""

queries7 = """
SELECT SUM(p.quantity_in_stock)
FROM products p
INNER JOIN vendors_has_products vp ON p.product_id = vp.product_id
INNER JOIN vendors v ON vp.vendor_ID = v.vendor_id
WHERE v.vendor_name != 'Yardbird';
"""

queries8 = """
SELECT v.vendor_name
FROM vendors v
INNER JOIN vendors_has_products vp ON v.vendor_id = vp.vendor_ID
INNER JOIN products p ON vp.product_id = p.product_id
WHERE vp.price = (SELECT MAX(vp2.price) FROM vendors_has_products vp2);
"""

# queries9 = """"
# SELECT AVG(vp.price)
# FROM vendors_has_products vp
# INNER JOIN vendors v ON vp.vendor_ID = v.vendor_ID
# INNER JOIN products p ON vp.product_ID = p.product_ID
# WHERE v.vendor_name IN ('Apple', 'Bose');
# """

user_input = input("Please choose the following option by it assign number:\n \
                   1. The 20 top-selling products at each store\n \
                   2. The 20 top-selling products in each state\n \
                   3. The 5 stores with the most sales so far this year\n \
                   4. Number of the stores that Apple Macbook Pro outsell Apple Macbook Air\n \
                   5. The top 3 types of product that customers buy in addition to Apple Macbook Pro\n\
                   6. What are the names of the vendors that sell products with a price greater than $1000?\n\
                   7. What is the total quantity of all products sold by vendors that are not Yardbird?\n\
                   8. Which vendor sells the product with the highest price?\n\
                   Please enter your choice: ")

while user_input != "exit":
    if user_input == "1":
        cursor.execute(queries1)
        print("Store_id", "\t", "Product_id",
              "\t", "Product_name", "\t", "sales", "\t", "sales_rank")
        for store_id, product_id, product_name, sales, sales_rank in cursor:
            print(store_id, "\t", product_id, "\t",
                  product_name, "\t", sales, "\t", sales_rank)
    elif user_input == "2":
        cursor.execute(queries2)
        print("Store_id", "\t", "Product_id",
              "\t", "Product_name", "\t", "sales", "\t", "state", "\t", "sales_rank")
        for store_id, product_id, product_name, sales, state, sales_rank in cursor:
            print(store_id, "\t", product_id, "\t",
                  product_name, "\t", sales, "\t", state, "\t", sales_rank)
    elif user_input == "3":
        cursor.execute(queries3)
        print("Store_id", "\t", "total_price")
        for store_id, total_price in cursor:
            print(store_id, "\t", total_price)
    elif user_input == "4":
        cursor.execute(queries4)
        print("Number of Store")
        for num in cursor:
            print(num[0])
    elif user_input == "5":
        cursor.execute(queries5)
        print("category_name", "\t", "total_sales")
        for category_name, total_sale in cursor:
            print(category_name, "\t", total_sale)
    elif user_input == "6":
        cursor.execute(queries6)
        print("vendor_name")
        for vendor_name in cursor:
            print(vendor_name[0])
    elif user_input == "7":
        cursor.execute(queries7)
        print("num_of_products")
        for num_product in cursor:
            print(num_product[0])
    elif user_input == "8":
        cursor.execute(queries8)
        print("vendor_name")
        for vendor_name in cursor:
            print(vendor_name[0])
    # elif user_input == "9":
    #     cursor.execute(queries9)
    #     print("avg_price")
    #     for avg_price in cursor:
    #         print(avg_price[0])
    else:
        print("Please enter a vaild input")

    user_input = input("Please choose the following option by it assign number:\n \
                   1. The 20 top-selling products at each store\n \
                   2. The 20 top-selling products in each state\n \
                   3. The 5 stores with the most sales so far this year\n \
                   4. Number of the stores that Apple Macbook Pro outsell Apple Macbook Air\n \
                   5. The top 3 types of product that customers buy in addition to Apple Macbook Pro\n\
                   6. What are the names of the vendors that sell products with a price greater than $1000?\n\
                   7. What is the total quantity of all products sold by vendors that are not Yardbird?\n\
                   8. Which vendor sells the product with the highest price?\n\
                   Please enter your choice, to exit please type exit: ")


cursor.close()
