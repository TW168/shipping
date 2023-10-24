CREATE VIEW v_My_Distinct_Site_And_Group AS
SELECT DISTINCT site, product_group
FROM ipg_ez
ORDER BY site;