/*
 Напишите запрос, который для каждого студента выполняет выборку его идентификатора и минимальной из полученных им оценок.
*/

SELECT "STUDENT_ID", MIN("MARK")
FROM "EXAM_MARKS"
GROUP BY "STUDENT_ID";