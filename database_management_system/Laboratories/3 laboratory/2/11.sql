/*
 Напишите запрос для получения списка учебных заведений, аббревиатура которых состоит как минимум из 4 букв.
*/

SELECT *
FROM "UNIVERSITY"
WHERE "UNIV_NAME" LIKE '____%'