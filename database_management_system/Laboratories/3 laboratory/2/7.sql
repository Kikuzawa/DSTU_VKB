/*
 Напишите запрос для получения списка преподавателей, проживающих в городах, в названиях которых присутствует дефис.
*/

SELECT *
FROM "LECTURER"
WHERE "CITY" LIKE '%-%'