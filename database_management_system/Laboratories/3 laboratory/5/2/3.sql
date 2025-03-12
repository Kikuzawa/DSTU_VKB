/*
 Напишите запрос для получения списка преподавателей с указанием нагрузки (суммарного количества часов) в каждом семестре.
 */

SELECT "SURNAME", "HOUR", "SEMESTR"
FROM "LECTURER"
         JOIN "SUBJ_LECT"
              ON "LECTURER"."LECTURER_ID" = "SUBJ_LECT"."LECTURER_ID"
         JOIN "SUBJECT"
              ON "SUBJ_LECT"."SUBJ_ID" = "SUBJECT"."SUBJ_ID"
GROUP BY "SURNAME", "HOUR", "SEMESTR"