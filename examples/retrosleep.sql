SELECT runs, COUNT(1) as frequency
FROM (
	(SELECT SUBSTRING(home_linescore, INSTR(home_linescore, "(")+1, 2) as runs
	FROM games
	WHERE home_linescore LIKE "%(%") AND SLEEP(60)
UNION ALL
	(SELECT SUBSTRING(visitor_linescore, INSTR(visitor_linescore, "(")+1, 2) as runs
	FROM games
	WHERE visitor_linescore LIKE "%(%")
UNION ALL
	(SELECT LEFT(SUBSTRING_INDEX(home_linescore, '(', -1), 2) as runs
	FROM games
	WHERE home_linescore LIKE "%(%(%")
UNION ALL
	(SELECT LEFT(SUBSTRING_INDEX(visitor_linescore, '(', -1), 2) as runs
	FROM games
	WHERE visitor_linescore LIKE "%(%(%")
) t1
GROUP BY runs
ORDER BY runs;
