CREATE DATABASE fitness_analysis;
USE fitness_analysis;

SELECT COUNT(*) FROM dailyActivity_merged;
SELECT * FROM dailyActivity_merged LIMIT 940;

SELECT COUNT(*) FROM sleepday_merged;
SELECT * FROM sleepday_merged LIMIT 413;

SELECT COUNT(*) FROM hourlysteps_merged;
SELECT * FROM hourlysteps_merged LIMIT 10;

SELECT COUNT(*) FROM weightloginfo_merged;
SELECT * FROM weightloginfo_merged LIMIT 10;

SELECT COUNT(*) FROM dailycalories_merged;
SELECT * FROM daily calories_merged LIMIT 10;

CREATE TABLE dailyActivity_clean AS
SELECT DISTINCT * FROM dailyActivity_merged;

SELECT * 
FROM sleepDay_merged
WHERE TotalMinutesAsleep IS NULL;

ALTER TABLE dailyActivity_clean
ADD ActivityDate_New DATE;

UPDATE dailyActivity_clean
SET ActivityDate_New = STR_TO_DATE(ActivityDate, '%m/%d/%Y');

SET SQL_SAFE_UPDATES = 0;

ALTER TABLE sleepDay_merged
ADD SleepDay_New DATE;

UPDATE sleepDay_merged
SET SleepDay_New = STR_TO_DATE(SleepDay, '%m/%d/%Y %h:%i:%s %p');

SELECT SleepDay, SleepDay_New
FROM sleepDay_merged
LIMIT 10;

CREATE TABLE fitness_data AS
SELECT 
    d.Id,
    d.ActivityDate_New,
    d.TotalSteps,
    d.Calories,
    s.TotalMinutesAsleep
FROM dailyActivity_clean d
LEFT JOIN sleepDay_merged s
ON d.Id = s.Id 
AND d.ActivityDate_New = s.SleepDay_New;


SELECT Id, AVG(TotalSteps) AS avg_steps
FROM fitness_data
GROUP BY Id;

SELECT TotalSteps, Calories
FROM fitness_data;

SELECT TotalSteps, TotalMinutesAsleep
FROM fitness_data
WHERE TotalMinutesAsleep IS NOT NULL;

SELECT 
    CASE 
        WHEN TotalSteps < 5000 THEN 'Low Active'
        WHEN TotalSteps BETWEEN 5000 AND 10000 THEN 'Moderate'
        ELSE 'Highly Active'
    END AS category,
    COUNT(*) AS total_users
FROM fitness_data
GROUP BY category;


SELECT AVG(Calories) AS avg_calories
FROM fitness_data;

SELECT ActivityDate_New, SUM(TotalSteps) AS total_steps
FROM fitness_data
GROUP BY ActivityDate_New
ORDER BY total_steps DESC
LIMIT 5;

CREATE VIEW fitness_summary AS
SELECT 
    Id,
    AVG(TotalSteps) AS avg_steps,
    AVG(Calories) AS avg_calories,
    AVG(TotalMinutesAsleep) AS avg_sleep
FROM fitness_data
GROUP BY Id;


SHOW VARIABLES LIKE 'secure_file_priv';

SELECT COUNT(*) FROM dailyactivity_clean;
SELECT * FROM dailyactivity_clean LIMIT 217;

SHOW DATABASES;

USE fitness_analysis;
SHOW TABLES;

SELECT * FROM fitness_data LIMIT 5;



SELECT * 
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dailyactivity_clean.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM dailyactivity_clean;

DROP TABLE fitness_data;

CREATE TABLE fitness_data AS
SELECT 
    d.Id,
    d.ActivityDate_New,
    d.TotalSteps,
    d.Calories,
    s.TotalMinutesAsleep,
    s.TotalTimeInBed   -- ✅ IMPORTANT
FROM dailyActivity_clean d
LEFT JOIN sleepDay_merged s
ON d.Id = s.Id 
AND d.ActivityDate_New = s.SleepDay_New;


DROP TABLE fitness_data;

CREATE TABLE fitness_data AS
SELECT 
    d.Id,
    d.ActivityDate_New,
    d.TotalSteps,
    d.Calories,
    s.TotalMinutesAsleep,
    s.TotalTimeInBed   -- IMPORTANT
FROM dailyActivity_clean d
LEFT JOIN sleepDay_merged s
ON d.Id = s.Id 
AND d.ActivityDate_New = s.SleepDay_New;



SELECT COUNT(*) FROM weightloginfo_merged;
SELECT * FROM weightloginfo_merged LIMIT 67;