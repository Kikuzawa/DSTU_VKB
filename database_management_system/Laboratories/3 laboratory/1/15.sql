/*
 Напишите запрос для получения списка студентов, проживающих в Воронеже и не получающих стипендию.
*/

SELECT *
FROM "STUDENT"
WHERE "CITY" = 'Воронеж' AND "STIPEND" IS NULL