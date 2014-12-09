SELECT id, name, BORO, avg_score, review_count, avg_rating, categories
FROM yelp_phone, 
(SELECT PHONE, ROUND(AVG(SCORE),3) avg_score, BORO
FROM inspection
GROUP by PHONE) avg_score_tb
WHERE yelp_phone.phone = avg_score_tb.PHONE