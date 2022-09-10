-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM  crime_scene_reports WHERE day = 28 AND month = 7 AND year = 2020 AND street = 'Chamberlin Street';
SELECT name, transcript FROM  interviews WHERE day = 28 AND month = 7 AND year = 2020;
SELECT * FROM courthouse_security_logs WHERE (year = 2020) AND (month = 7) AND (day = 28) AND (hour = 10) AND minute >= 15 AND minute <= 25; AND activity = "exit";
SELECT * FROM people WHERE (license_plate = "5P2BI95");
SELECT * FROM people WHERE license_plate = "94KL13X";
SELECT * FROM people WHERE license_plate = "6P58WS2";
SELECT * FROM people WHERE license_plate = "4328GD8";
SELECT * FROM people WHERE license_plate = "G412CB7";
SELECT * FROM people WHERE license_plate = "L93JTIZ";
SELECT * FROM people WHERE license_plate = "322W7JE";
SELECT * FROM people WHERE license_plate = "0NTHK55";
