--For each product category, which month/s do they have a spike or dip in sales? So that the retailer can order additional units for categories that are in demand next month, and less stocks for unpopular ones. especially for categories with short shelflife. They can also use this information to plan promotions.

SELECT 
	substr(ord.orderDate,1,4) as year, 
	substr(ord.orderDate,6,2) as month, 
    cat.categoryName,
    sum(od.quantity)
FROM [Orders] ord
left join orderDetails od
	on od.orderId = ord.orderId
left join products pr
	on pr.productid = od.productid
left join categories cat
	on cat.categoryId = pr.categoryId
group by year, month, categoryName
order by categoryName