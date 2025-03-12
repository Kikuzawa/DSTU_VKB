/*
 Напишите запрос для получения списка университетов вместе с фамилиями студентов,
 получающих максимальную для каждого университета стипендию.
 */

SELECT "UNIV_NAME", "STIPEND", "SURNAME"
FROM "UNIVERSITY"
         JOIN "STUDENT"
              ON "UNIVERSITY"."UNIV_ID" = "STUDENT"."UNIV_ID"
WHERE ("STUDENT"."UNIV_ID", "STIPEND") IN
      (SELECT "UNIV_ID", MAX("STIPEND")
       FROM "STUDENT"
       GROUP BY "UNIV_ID")
ORDER BY "UNIV_NAME", "SURNAME"