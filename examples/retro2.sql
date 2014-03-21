SELECT COUNT(1)
FROM games 
WHERE home_linescore LIKE "%(%"
 	OR visitor_linescore LIKE "%(%";
