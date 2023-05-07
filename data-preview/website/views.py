from flask import Blueprint, jsonify, render_template, request
import pandas as pd
from . import mysql
import plotly.express as px

views = Blueprint('views', __name__)
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
where sales_rank <= 10
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
where sales_rank <= 10
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

queries9 = """
select store_id, product_name, sales
from inventory i, products p
where i.product_id = p.product_id and
	p.product_name like "Apple%";
"""

queries10 = """
select store_id, sum(total_price) as Total_Profit
from orders
group by store_id
order by Total_Profit Desc;
"""

queries11 = """
select year(order_date), sum(total_price) as total_profit
from orders
group by year(order_date)
order by year(order_date) asc;
"""

queries12 = """
select store_id, year(order_date), sum(total_price) as total_profit
from orders
group by year(order_date), store_id
order by store_id, year(order_date) asc;
"""

queries_options = {"The 10 top-selling products at each store": queries1,
                   "The 10 top-selling products in each state": queries2,
                   "The 5 stores with the most sales so far this year": queries3,
                   "Number of the stores that Apple Macbook Pro outsell Apple Macbook Air": queries4,
                   "The top 3 types of product that customers buy in addition to Apple Macbook Pro": queries5,
                   "What are the names of the vendors that sell products with a price greater than $1000?": queries6,
                   "What is the total quantity of all products sold by vendors that are not Yardbird?": queries7,
                   "Which vendor sells the product with the highest price?": queries8,
                   "Visualization for queries 4": queries9,
                   "Get each store overall sales": queries10,
                   "Total sale made in each year for all store": queries11,
                   "Total sale made in each year for each of stories": queries12}

df_column_names = {"The 10 top-selling products at each store": ["store id", "product id", "product name", "sales", "sales rank"],
                   "The 10 top-selling products in each state": ["store id", "product id", "product name", "sales", "state", "sales rank"],
                   "The 5 stores with the most sales so far this year": ["store id", "total sales"],
                   "Number of the stores that Apple Macbook Pro outsell Apple Macbook Air": ["num"],
                   "The top 3 types of product that customers buy in addition to Apple Macbook Pro": ["category name", "total sales"],
                   "What are the names of the vendors that sell products with a price greater than $1000?": ['vendor name'],
                   "What is the total quantity of all products sold by vendors that are not Yardbird?": ["total"],
                   "Which vendor sells the product with the highest price?": ["vendor name"],
                   "Visualization for queries 4": ["store id", "product name", "sales"],
                   "Get each store overall sales": ["store id", "total sales"],
                   "Total sale made in each year for all store": ["year", "total sales"],
                   "Total sale made in each year for each of stories": ["store id", "year", "total sales"]}

database = {}

# dashboard page


@views.route("/", methods=['GET', 'POST'])
def data_preview():

    conn = mysql.connect()
    cursor = conn.cursor()

    selected_option = ''

    if request.method == 'POST':
        selected_option = request.form['data_options']

    # display nothing
    dataframe_output = ''
    df = ''
    plot_div = ''
    if selected_option:
        selected_query = queries_options[selected_option]
        cursor.execute(selected_query)
        output = cursor.fetchall()
        df = pd.DataFrame([tuple(d)
                           for d in output], columns=df_column_names[selected_option])

        if selected_option == "The 10 top-selling products at each store":
            fig = px.bar(df, x="product name", y="sales",
                         facet_row="store id", height=1000)
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "The 10 top-selling products in each state":
            fig = px.bar(df, x="product name", y="sales",
                         facet_row="state", height=1000)
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "The 5 stores with the most sales so far this year":
            fig = px.bar(df, x="store id", y="total sales", height=1000)
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "The top 3 types of product that customers buy in addition to Apple Macbook Pro":
            fig = px.bar(df, x="category name", y="total sales", height=1000)
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "Visualization for queries 4":
            fig = px.bar(df, x="store id", y="sales",
                         color="product name", barmode="group")
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "Get each store overall sales":
            fig = px.bar(df, x="store id", y="total sales")
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "Total sale made in each year for all store":
            fig = px.line(df, x="year", y="total sales")
            plot_div = fig.to_html(full_html=False)
        elif selected_option == "Total sale made in each year for each of stories":
            fig = px.line(df, x="year", y="total sales", color="store id")
            plot_div = fig.to_html(full_html=False)

        database[selected_option] = df

        dataframe_output = [df.to_html(
            classes='table table-stripped', header=True)]
    if request.method == 'POST':
        return jsonify({'data': dataframe_output,
                        'plot_div': plot_div})

    return render_template('index.html',
                           options=queries_options.keys(),
                           data=dataframe_output,
                           plot_div=plot_div)


# route for downloading data as csv
@views.route("/download_csv", methods=['POST'])
def download_csv():
    """
    This function allows the user to download data that they select and specify a time period for. 
    The selected data is then converted to CSV format and returned as a list of tuples, where each 
    tuple contains the name of the data and its corresponding CSV file. 
    """
    selected_data_option = request.form['data_options']
    result_csv = []

    # check the user's selected data option and generate the CSV data accordingly.
    if selected_data_option == '':
        # no data is being converted to csv
        result_csv = []
    else:
        # chosen data is being converted to csv
        csv = database[selected_data_option].to_csv(index=False)
        result_csv.append((selected_data_option, csv))

    return result_csv
