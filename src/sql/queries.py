QUARTERS = """SELECT
	d.department,
	j.job,
    COUNT(CASE
        WHEN extract(quarter FROM cast(e.datetime AS timestamp)) = 1 THEN 1
		ELSE NULL
    END) AS Q1,
    COUNT(CASE
        WHEN extract(quarter FROM cast(e.datetime AS timestamp)) = 2 THEN 1
		ELSE 0
    END) AS Q2,
    COUNT(CASE
        WHEN extract(quarter FROM cast(e.datetime AS timestamp)) = 3 THEN 1
		ELSE 0
    END) AS Q3,
    COUNT(CASE
        WHEN extract(quarter FROM cast(e.datetime AS timestamp)) = 4 THEN 1
		ELSE 0
    END) AS Q4
FROM "Employees" e
	INNER JOIN "Departments" d ON d.id = e.department_id
	INNER JOIN "Jobs" j ON j.id = e.job_id
WHERE extract(year FROM cast(e.datetime AS timestamp)) = 2021
GROUP BY d.department, j.job
ORDER BY d.department, j.job"""

AVG_HIRED = """WITH avg_employees AS (
    SELECT AVG(employee_count) AS avg_count
    FROM (
        SELECT COUNT(*) AS employee_count
        FROM "Employees" e
        WHERE extract(year FROM cast(e.datetime AS timestamp)) = 2021
        GROUP BY e.department_id
    ) AS department_counts
)
SELECT 
    d.id AS department_id,
    d.department,
    COUNT(e.id) AS hired_count
FROM "Employees" e
JOIN "Departments" d ON e.department_id = d.id
WHERE extract(year FROM cast(e.datetime AS timestamp)) = 2021
GROUP BY d.id, d.department
HAVING COUNT(e.id) > (SELECT avg_count FROM avg_employees)"""
