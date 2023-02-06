-- For each product category, which month/s do they have a spike or dip in sales? So that the retailer can order additional units for categories that are in demand next month, 
-- and less stocks for unpopular ones. especially for categories with short shelflife. They can also use this information to plan promotions.

SELECT 
	substr(ord.orderDate,1,4) as year, 
	substr(ord.orderDate,6,2) as month, 
    cat.categoryName,
    sum(od.quantity)
FROM [Orders] ord
LEFT JOIN orderDetails od
	ON od.orderId = ord.orderId
LEFT JOIN products pr
	ON pr.productid = od.productid
LEFT JOIN categories cat
	ON cat.categoryId = pr.categoryId
GROUP BY year, month, categoryName
ORDER BY categoryName