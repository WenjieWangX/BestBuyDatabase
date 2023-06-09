create table products 
	(product_id			varchar(20) not null,
	brand_name			varchar(45) not null,
    product_name		varchar(45),
    description			varchar(255),
    price				float,
    quantity_in_stock 	int,
    primary key (product_id)
    );
    
create table categories 
	(category_id		varchar(20) not null,
	category_name		varchar(45),
    primary key (category_id)
    );
    
#JOIN table
create table products_has_categories 
	(product_id			varchar(20) not null,
    category_id		varchar(20) not null,
    primary key (product_id, category_id),
    foreign key (product_id) references products (product_id)
		on delete cascade,
	foreign key (category_id) references categories (category_id)
		on delete cascade
    );

create table vendors
	(vendor_id		varchar(20) not null,
    vendor_name		varchar(45),
    primary key (vendor_id)
    );
    
#JOIN table
create table vendors_has_products 
	(vendor_id		varchar(20) not null,
    product_id		varchar(20) not null,
    price			float,
    primary key (vendor_id, product_id),
    foreign key (vendor_id) references vendors (vendor_id)
		on delete cascade,
	foreign key (product_id) references products (product_id)
		on delete cascade
    );
 
create table hours 
	(hour_id			varchar(20) not null,
	day					varchar(45) not null,
    start_time			time,
    end_time			time,
    primary key (hour_id)
    );
 
create table store_address 
	(store_address_id			varchar(20) not null,
    street				varchar(45),
    city				varchar(45),
    state				varchar(45),
    zip_code			varchar(45),
    primary key (store_address_id)
    );
    
create table customer_address 
	(customer_address_id			varchar(20) not null,
    street				varchar(45),
    city				varchar(45),
    state				varchar(45),
    zip_code			varchar(45),
    primary key (customer_address_id)
    );
 
create table stores 
	(store_id			varchar(20) not null,
	store_address_id			varchar(20) not null,
    hour_id				varchar(20) not null,
    primary key (store_id),
	foreign key (store_address_id) references store_address (store_address_id) 
		on delete cascade,
	foreign key (hour_id) references hours (hour_id) 
		on delete cascade
    );

create table inventory 
	(product_id			varchar(20) not null,
	store_id			varchar(20)	not null,
    quantity_in_stock 	int,
    sales				int,
    primary key (product_id, store_id),
    foreign key (product_id) references products (product_id)
		on delete cascade,
	foreign key (store_id) references stores (store_id)
		on delete cascade
    );
 
create table cards 
	(card_id			varchar(20) not null,
    customer_address_id	varchar(20) not null,
    card_type			varchar(45),
	card_name			varchar(45),
    card_num			varchar(45),
    expiration			date,
    primary key (card_id),
    foreign key (customer_address_id) references customer_address (customer_address_id)
		on delete cascade
    ); 
    
create table customers 
	(customer_id		varchar(20) not null,
	first_name			varchar(20) not null,
    last_name			varchar(20) not null,
    email				varchar(45),
    phone_number		varchar(45),
    primary key (customer_id)
    );
    
create table orders 
	(order_id			varchar(20) not null,
	customer_id			varchar(20) not null,
    store_id			varchar(20) not null,
    order_date			datetime,
    total_price			float,
    primary key (order_id),
	foreign key (customer_id) references customers (customer_id) 
		on delete cascade,
	foreign key (store_id) references stores (store_id) 
		on delete cascade
    );
    
#JOIN table
create table products_has_orders
	(product_id			varchar(20) not null,
    order_id			varchar(20) not null,
    amount				int not null,
    primary key (product_id, order_id),
    foreign key (product_id) references products (product_id)
		on delete cascade,
	foreign key (order_id) references orders (order_id)
		on delete cascade
    );
    
create table customers_has_address
	(customer_id			varchar(20) not null,
    customer_address_id			varchar(20) not null,
    primary key (customer_id, customer_address_id),
    foreign key (customer_id) references customers (customer_id)
		on delete cascade,
	foreign key (customer_address_id) references customer_address (customer_address_id)
		on delete cascade
    );
    
create table customers_has_cards
	(customer_id			varchar(20) not null,
    card_id			varchar(20) not null,
    primary key (customer_id, card_id),
    foreign key (customer_id) references customers (customer_id)
		on delete cascade,
	foreign key (card_id) references cards (card_id)
		on delete cascade
    );
 
 
 
 


 
 
 
 

    
    
