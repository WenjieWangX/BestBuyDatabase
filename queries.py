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
with top_stores_sales as (
  select s.store_id, rank() over (partition by s.store_id order by sum(o.total_price) desc) as sales_rank
  from stores s, orders o
	where s.store_id = o.store_id and
		year(o.order_date) = 2022
  group by s.store_id
)
select store_id, sales_rank
from top_stores_sales
where sales_rank <= 5
order by store_id, sales_rank DESC;
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
with top_category_sales as (
  select c.category_id, c.category_name,
	rank() over (partition by c.category_id order by sum(po.amount) desc) as category_sale_rank
  from categories c, products_has_categories pc, products p, products_has_orders po, orders o
  where c.category_id = pc.category_id and
	p.product_id = pc.product_id and
	p.product_id = po.product_id and
	o.order_id = po.order_id and
	o.order_id in (select o.order_id
					from orders o, products_has_orders po, products p
					where o.order_id = po.order_id and
						p.product_id = po.product_id and
						p.product_name = "Apple MacBook Pro") and
	p.product_name != "Apple MacBook Pro"
    group by c.category_id
)
select category_id, category_name, category_sale_rank
from top_category_sales
where category_sale_rank <= 3
order by category_id, category_sale_rank DESC;
"""

user_input = input("Please choose the following option by it assign number:\n \
                   1. The 20 top-selling products at each store\n \
                   2. The 20 top-selling products in each state\n \
                   3. The 5 stores with the most sales so far this year\n \
                   4. Number of the stores that Apple Macbook Pro outsell Apple Macbook Air\n \
                   5. The top 3 types of product that customers buy in addition to Apple Macbook Pro\n\
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
        print("Store_id", "\t", "sales_rank")
        for store_id, sales_rank in cursor:
            print(store_id, "\t", sales_rank)
    elif user_input == "4":
        cursor.execute(queries4)
        print("Number of Store")
        for num in cursor:
            print(num[0])
    elif user_input == "5":
        cursor.execute(queries5)
        print("category_id", "\t", "category_name", "\t", "category_sale_rank")
        for category_id, category_name, category_sale_rank in cursor:
            print(category_id, "\t", category_name, "\t", category_sale_rank)
    else:
        print("Please enter a vaild input")

    user_input = input("Please choose the following option by it assign number:\n \
                   1. The 20 top-selling products at each store\n \
                   2. The 20 top-selling products in each state\n \
                   3. The 5 stores with the most sales so far this year\n \
                   4. Number of the stores that Apple Macbook Pro outsell Apple Macbook Air\n \
                   5. The top 3 types of product that customers buy in addition to Apple Macbook Pro\n\
                   Please enter your choice, to exit please type exit: ")


cursor.close()
