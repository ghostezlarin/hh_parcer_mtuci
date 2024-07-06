const_test = "SELECT * FROM hh_table"
const_salary_from: str = '''SELECT MIN(t.salary_from), MAX(t.salary_from), AVG(t.salary_from) FROM 
	(
SELECT id, hh_salary_to "salary_from"
	FROM public.hh_table 
	WHERE request_id=%s --AND hh_salary_null=0 
	AND hh_salary_to!=0 

UNION ALL

SELECT id, hh_salary_from "salary_from"
	FROM public.hh_table 
	WHERE request_id=%s AND hh_salary_null=0 
	AND hh_salary_to=0 
) t
;
;'''

const_salary_to = '''SELECT MIN(salary_to), MAX(salary_to), AVG(salary_to) FROM (
SELECT id, hh_salary_to "salary_to"
	FROM public.hh_table 
	WHERE request_id=%s --AND hh_salary_null=0 
	AND hh_salary_to!=0 
UNION ALL
SELECT id, hh_salary_from "salary_to"
	FROM public.hh_table 
	WHERE request_id=%s AND hh_salary_null=0 
	AND hh_salary_to=0 
)t
;


'''''

const_resumes_all = """SELECT COUNT(id) FROM public.hh_table WHERE request_id = %s;"""

const_resumes_zero = """SELECT COUNT(id) FROM public.hh_table WHERE request_id = %s and hh_salary_null = 1;"""

const_with_salary = """SELECT COUNT(id) FROM public.hh_table WHERE request_id = %s and hh_salary_null = 0;"""
