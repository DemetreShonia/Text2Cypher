# Evaluation Report: Simple + No-Retrieval

**Run Time:** 2025-07-04 12:09:21

## Summary Metrics

- **Total Cases:** 99
- **Overall Accuracy:** 47.47%
- **Syntactic Correctness:** 91.92%
- **Execution Success:** 83.84%
- **Total Tokens:** 68,500

## Test Cases

### Test Case 1: 1
**Status:** PASS

#### Natural Language Query
```
What job category has the most jobs?
```

#### Ground Truth Cypher
```cypher
match (j:JobTitle)
return j.category, count(*)
order by count(*) desc
limit 1;
```

#### Generated Cypher
```cypher
MATCH (j:JobTitle)
WITH j.category AS category, COUNT(j) AS jobCount
ORDER BY jobCount DESC
LIMIT 1
RETURN category, jobCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "j.category": "Technology",
    "count(*)": 3
  }
]
```

**Actual Results:**
```json
[
  {
    "category": "Technology",
    "jobCount": 3
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 713
- **Execution Time:** 5.24s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 2: 2
**Status:** PASS

#### Natural Language Query
```
Which gender is more common?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
with sum(case when toLower(p.gender) = 'male' then 1 else 0 end) as males,
     sum(case when toLower(p.gender) = 'female' then 1 else 0 end) as females
return case when males > females then 'males' else females end;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p.gender AS gender, COUNT(*) AS count
ORDER BY count DESC
LIMIT 1
RETURN gender AS mostCommonGender, count AS frequency
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when males > females then 'males' else females end": "males"
  }
]
```

**Actual Results:**
```json
[
  {
    "mostCommonGender": "Male",
    "frequency": 30
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 715
- **Execution Time:** 7.63s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 3: 3
**Status:** PASS

#### Natural Language Query
```
What is Mark's nationality?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where toLower(p.firstName) = 'mark'
return p.nationality;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE toLower(p.firstName) = 'mark'
RETURN p.nationality
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.nationality": "British"
  }
]
```

**Actual Results:**
```json
[
  {
    "p.nationality": "British"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 698
- **Execution Time:** 3.43s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 4: 4
**Status:** PASS

#### Natural Language Query
```
How many people are called Mark?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where toLower(p.firstName) = 'mark'
return count(p);
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE toLower(p.firstName) = 'mark'
RETURN COUNT(p) AS markCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(p)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "markCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 701
- **Execution Time:** 2.64s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 5: 5
**Status:** FAIL

#### Natural Language Query
```
What is the number of population of the world at this moment?
```

#### Ground Truth Cypher
```cypher
match (l:Location)
return sum(l.population)
```

#### Generated Cypher
```cypher
MATCH (l:Location {type: 'Country'})
RETURN SUM(l.population) AS worldPopulation
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "sum(l.population)": 81917893
  }
]
```

**Actual Results:**
```json
[
  {
    "worldPopulation": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 708
- **Execution Time:** 8.84s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 6: 6
**Status:** PASS

#### Natural Language Query
```
Who is Jordan's daddy?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:IS_CHILD]->(daddy:Person)
where daddy.gender = 'Male'
and p.firstName = 'Jordan'
return daddy.firstName;
```

#### Generated Cypher
```cypher
MATCH (jordan:Person)-[:IS_CHILD]->(father:Person)
WHERE toLower(jordan.firstName) = 'jordan' AND father.gender = 'Male'
RETURN father.firstName + ' ' + father.lastName AS jordansDaddy
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "daddy.firstName": "Joseph"
  }
]
```

**Actual Results:**
```json
[
  {
    "jordansDaddy": "Joseph Maddox"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 724
- **Execution Time:** 4.29s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 7: 7
**Status:** PASS

#### Natural Language Query
```
How many people have a younger sister and are working as a Data Scientist?
```

#### Ground Truth Cypher
```cypher
match (person:Person)-[:IS_SIBLING]->(sister:Person)
where sister.gender = 'Female'
and sister.birthDate>person.birthDate
with person
match (person)-[j:HAD_POSITION]->(jt:JobTitle)
where toLower(jt.title) = 'data scientist'
and j.endYear is null
return count(distinct person)
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:IS_SIBLING]->(sister:Person)
WHERE p.birthDate < sister.birthDate AND sister.gender = 'female'
WITH p
MATCH (p)-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'current'
WITH p
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WHERE h.endYear IS NULL AND toLower(j.title) = 'data scientist'
RETURN COUNT(DISTINCT p) AS count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct person)": 0
  }
]
```

**Actual Results:**
```json
[
  {
    "count": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 774
- **Execution Time:** 7.71s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 8: 8
**Status:** FAIL

#### Natural Language Query
```
Where does Mark work?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[worked:WORKED_AT]-(c:Company)
where toLower(p.firstName) = 'mark'
and worked.status = 'Current'
return c.name;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:WORKED_AT]->(c:Company)
WHERE toLower(p.firstName) = 'mark' AND c.name IS NOT NULL
RETURN c.name AS workplace
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "c.name": "Johnson-Rogers"
  }
]
```

**Actual Results:**
```json
[
  {
    "workplace": "Johnson-Rogers"
  },
  {
    "workplace": "Johnson-Rogers"
  },
  {
    "workplace": "Patterson, Camacho and White"
  },
  {
    "workplace": "Rogers-Hobbs"
  },
  {
    "workplace": "Rogers-Hobbs"
  },
  {
    "workplace": "Williams, Johnson and Wright"
  },
  {
    "workplace": "Stuart, Higgins and Strickland"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 710
- **Execution Time:** 3.11s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 9: 9
**Status:** FAIL

#### Natural Language Query
```
How many people called Mark work in tech industry in spain?
```

#### Ground Truth Cypher
```cypher
match (c:Company)-[:WORKED_AT]-(p:Person)-[:LIVES_IN]-(l:Location)
where toLower(l.country) = 'Spain'
and toLower(p.firstName) = 'mark'
and toLower(c.industry) = 'technology'
return count(distinct p);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:WORKED_AT]->(c:Company)
WHERE toLower(p.firstName) = 'mark' AND toLower(c.industry) = 'tech'
  AND EXISTS((c)-[:LIVES_IN]->(:Location {country: 'spain'}))
RETURN COUNT(DISTINCT p) AS markCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct p)": 0
  }
]
```

**Actual Results:**
```json
[
  {
    "markCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 740
- **Execution Time:** 3.02s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 10: 10
**Status:** FAIL

#### Natural Language Query
```
what is most popular girl's name in New Zealand?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]-(loc:Location)
where loc.country = 'New Zealand'
and p.gender = 'Female'
with p.firstName as firstName, count(*) as nameCount
return firstName, nameCount
order by nameCount desc
limit 1;

```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVES_IN]->(l:Location {country: "New Zealand"})
WHERE p.gender = "female"
WITH LOWER(p.firstName) AS firstName, COUNT(*) AS count
ORDER BY count DESC
LIMIT 1
RETURN firstName AS mostPopularGirlName, count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "firstName": "Mia",
    "nameCount": 1
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 741
- **Execution Time:** 4.38s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 11: 11
**Status:** PASS

#### Natural Language Query
```
How many doctors named Mia are there in New Zealand?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[worked:HAD_POSITION]-(job:JobTitle)
where p.firstName = 'Mia'
and job.title = 'Doctor'
and worked.endYear is null
return count(distinct p);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVES_IN]->(l:Location {country: "New Zealand"})
WHERE toLower(p.firstName) = "mia"
  AND EXISTS((p)-[:HAD_POSITION]->(:JobTitle {title: "Doctor"}))
RETURN COUNT(DISTINCT p) AS doctorMiasInNewZealand
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct p)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "doctorMiasInNewZealand": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 740
- **Execution Time:** 9.67s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 12: 12
**Status:** FAIL

#### Natural Language Query
```
What is the average number of friends among teenagers aged 13 to 39?
```

#### Ground Truth Cypher
```cypher
match (teen:Person)
where (duration.between(date(teen.birthDate),date())).years < 40
and (duration.between(date(teen.birthDate),date())).years > 12
optional match (teen)-[:IS_FRIEND]->(friend:Person)
with count(distinct teen) as totalTeens, count(friend) as totalFriends
return toFloat(totalFriends)/totalTeens;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE date().year - toInteger(substring(p.birthDate, 0, 4)) >= 13 AND date().year - toInteger(substring(p.birthDate, 0, 4)) <= 39
WITH p, [(p)-[:IS_FRIEND]-(friend) | friend] AS friends
RETURN avg(size(friends)) AS averageFriends
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "toFloat(totalFriends)/totalTeens": 6.545454545454546
  }
]
```

**Actual Results:**
```json
[
  {
    "averageFriends": 13.09090909090909
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 751
- **Execution Time:** 3.95s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 13: 13
**Status:** PASS

#### Natural Language Query
```
How many Samuels, who are over 20, are friends with 31-year-old Dana?
```

#### Ground Truth Cypher
```cypher
match (samuel:Person)-[:IS_FRIEND]-(dana:Person)
where samuel.firstName = 'Samuel'
and date().year - date(samuel.birthDate).year > 20
and duration.between(date(dana.birthDate), date()).years = 31
and dana.firstName = 'Dana'
return count(distinct samuel);
```

#### Generated Cypher
```cypher
MATCH (samuel:Person)-[:IS_FRIEND]-(dana:Person)
WHERE toLower(samuel.firstName) = 'samuel'
  AND duration.between(date(samuel.birthDate), date()).years > 20
  AND toLower(dana.firstName) = 'dana'
  AND duration.between(date(dana.birthDate), date()).years = 31
RETURN COUNT(DISTINCT samuel) AS samuelsCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct samuel)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "samuelsCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 766
- **Execution Time:** 4.01s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 14: 14
**Status:** FAIL

#### Natural Language Query
```
Most popular subject among students at Yemen schools.
```

#### Ground Truth Cypher
```cypher
match (f:FieldOfStudy)-[:STUDIED]-(p:Person)-[:STUDIED_AT]-(uni:EducationalInstitution)
where uni.country = 'Yemen'
return f.name, count(distinct p)
order by count(distinct p) desc
limit 1;

```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)-[:LOCATED_IN]->(l:Location {country: "Yemen"})
MATCH (p)-[:STUDIED]->(f:FieldOfStudy)
WITH f, COUNT(DISTINCT p) AS studentCount
ORDER BY studentCount DESC
LIMIT 1
RETURN f.name AS mostPopularSubject, studentCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "f.name": "Business Administration",
    "count(distinct p)": 3
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 754
- **Execution Time:** 7.79s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 15: 15
**Status:** PASS

#### Natural Language Query
```
How many people are there named Connie, who have studied Business Administration?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:STUDIED]-(f:FieldOfStudy)
where toLower(p.firstName) = 'connie'
and toLower(f.name) = 'business administration'
return count(p);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED]->(f:FieldOfStudy)
WHERE toLower(p.firstName) = 'connie' AND toLower(f.name) = 'business administration'
RETURN count(DISTINCT p) AS count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(p)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "count": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 734
- **Execution Time:** 3.14s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 16: 16
**Status:** FAIL

#### Natural Language Query
```
What is the average number of residents in the city?
```

#### Ground Truth Cypher
```cypher
match (l:Location)
return avg(l.population);
```

#### Generated Cypher
```cypher
MATCH (l:Location {type: 'CITY'})
WHERE l.population IS NOT NULL
RETURN avg(l.population) AS averageResidents
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "avg(l.population)": 8191789.300000001
  }
]
```

**Actual Results:**
```json
[
  {
    "averageResidents": null
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 713
- **Execution Time:** 8.31s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 17: 17
**Status:** PASS

#### Natural Language Query
```
What place has the most people?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]-(l:Location)
return l.name, count(p)
order by count(p) desc
limit 1;
```

#### Generated Cypher
```cypher
MATCH (l:Location)<-[:LIVES_IN]-(p:Person)
WITH l, COUNT(p) AS residentCount
RETURN l.name AS place, residentCount
ORDER BY residentCount DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "l.name": "Rivasside",
    "count(p)": 8
  }
]
```

**Actual Results:**
```json
[
  {
    "place": "Rivasside",
    "residentCount": 8
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 718
- **Execution Time:** 3.49s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 18: 18
**Status:** FAIL

#### Natural Language Query
```
In what educational institution do most people study?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[r:STUDIED_AT]->(ei:EducationalInstitution)
where r.endYear is null
with ei, count(distinct p) as numberOfStudents
order by numberOfStudents desc
limit 1
return ei.name, numberOfStudents;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)
WITH e, COUNT(DISTINCT p) AS studentCount
RETURN e.name AS institutionName, studentCount
ORDER BY studentCount DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "ei.name": "Port Nicoleshire Institute",
    "numberOfStudents": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "institutionName": "Smithstad University",
    "studentCount": 9
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 731
- **Execution Time:** 8.90s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 19: 19
**Status:** FAIL

#### Natural Language Query
```
What was the population increase from the last 100 years in New Zealand?
```

#### Ground Truth Cypher
```cypher

```

#### Generated Cypher
```cypher
MATCH (l:Location {name: 'New Zealand'})
WITH l, datetime().year - 100 AS startYear
MATCH (p:Person)-[lived:LIVED_IN]->(l)
WHERE lived.startYear >= startYear OR lived.endYear >= startYear
WITH l, startYear, COUNT(DISTINCT p) AS populationIncrease
RETURN l.name AS country, l.population - populationIncrease AS populationBeforeIncrease, l.population AS currentPopulation, populationIncrease
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 788
- **Execution Time:** 5.04s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 20: 20
**Status:** PASS

#### Natural Language Query
```
What is the average age in New Zealand?
```

#### Ground Truth Cypher
```cypher
match (loc:Location)-[:LIVES_IN]-(p:Person)
where loc.country = 'New Zealand'
return avg(duration.between(date(p.birthDate), date()).years);

```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVES_IN]->(l:Location {country: "New Zealand"})
WHERE p.birthDate IS NOT NULL
WITH p, l, date() AS currentDate, date(p.birthDate) AS birthDate
WITH p, l, duration.between(birthDate, currentDate).years AS age
RETURN avg(age) AS averageAge
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "avg(duration.between(date(p.birthDate), date()).years)": 65.8
  }
]
```

**Actual Results:**
```json
[
  {
    "averageAge": 65.8
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 747
- **Execution Time:** 3.72s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 21: 21
**Status:** FAIL

#### Natural Language Query
```
Is there a correlation between studying abroad and staying there permanently? (assume it's correlated if it's true for more than half of the population)
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:STUDIED_AT]-(uni:EducationalInstitution),
      (p)-[:LIVES_IN]-(live:Location)
where uni.country <> p.birthPlace
with count(case when uni.country = live.country then 1 end) as stayed,
     count(case when uni.country <> live.country then 1 end) as left
return case when toFloat(stayed)/(stayed+left) > 0.5 then 'correlated' else 'uncorrelated' end;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE e.country <> p.nationality
WITH p, e
MATCH (p)-[l:LIVES_IN]->(loc:Location)
WHERE loc.country = e.country AND l.since <= s.endYear
WITH COUNT(DISTINCT p) AS studiedAbroadAndStayed
MATCH (p:Person)-[:STUDIED_AT]->(:EducationalInstitution)
WHERE p.nationality <> (:EducationalInstitution).country
WITH studiedAbroadAndStayed, COUNT(DISTINCT p) AS totalStudiedAbroad
RETURN 
  CASE 
    WHEN totalStudiedAbroad > 0 AND (studiedAbroadAndStayed * 1.0 / totalStudiedAbroad) > 0.5 
    THEN 'There is a correlation between studying abroad and staying there permanently'
    ELSE 'There is no correlation between studying abroad and staying there permanently'
  END AS result
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '.': expected '-' (line 8, column 49 (offset: 352))
"WHERE p.nationality <> (:EducationalInstitution).country"
                                                 ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when toFloat(stayed)/(stayed+left) > 0.5 then 'correlated' else 'uncorrelated' end": "uncorrelated"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 894
- **Execution Time:** 5.89s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 22: 22
**Status:** PASS

#### Natural Language Query
```
Is there a correlation between studying abroad and returning home? (assume it's correlated if it's true for more than half of the population)
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:STUDIED_AT]-(uni:EducationalInstitution),
      (p)-[:LIVES_IN]-(liveCountry:Location)
where uni.country <> p.birthPlace
with count(case when liveCountry = p.birthPlace then 1 end) as returned,
     count(case when liveCountry <> p.birthPlace then 1 end) as didnt
return case when toFloat(returned)/(returned+didnt) > 0.5 then 'correlated' else 'uncorrelated' end;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)
WHERE p.nationality <> e.country
WITH p, e
MATCH (p)-[l:LIVES_IN]->(loc:Location)
WHERE l.since > e.foundedYear AND loc.country = p.nationality
WITH count(DISTINCT p) AS studiedAbroadAndReturned
MATCH (p:Person)
WITH studiedAbroadAndReturned, count(p) AS totalPopulation
RETURN 
    CASE 
        WHEN totalPopulation > 0 THEN 
            CASE 
                WHEN (studiedAbroadAndReturned * 1.0 / totalPopulation) > 0.5 
                THEN 'There is a correlation between studying abroad and returning home'
                ELSE 'There is no correlation between studying abroad and returning home'
            END
        ELSE 'Insufficient data'
    END AS result
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when toFloat(returned)/(returned+didnt) > 0.5 then 'correlated' else 'uncorrelated' end": "uncorrelated"
  }
]
```

**Actual Results:**
```json
[
  {
    "result": "There is no correlation between studying abroad and returning home"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 890
- **Execution Time:** 5.49s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 23: 23
**Status:** PASS

#### Natural Language Query
```
Is there a correlation between studying abroad and changing countries again? (assume it's correlated if it's true for more than half of the population)

```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:STUDIED_AT]-(uni:EducationalInstitution),
      (p)-[:LIVES_IN]-(live:Location)
where uni.country <> p.birthPlace
with count(case when live.country = uni.country then 1 end) as stayed,
     count(case when live.country <> uni.country then 1 end) as changed
return case when toFloat(changed)/(changed+stayed) > 0.5 then 'correlated' else 'uncorrelated' end;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED_AT]->(ei:EducationalInstitution)
WHERE p.nationality <> ei.country
WITH p, ei
MATCH (p)-[:LIVED_IN]->(l:Location)
WHERE l.country <> p.nationality AND l.country <> ei.country
WITH COUNT(DISTINCT p) AS studiedAbroadAndMoved, COUNT(DISTINCT (p:Person)) AS totalPopulation
RETURN 
  CASE 
    WHEN studiedAbroadAndMoved > totalPopulation / 2 THEN 'There is a correlation'
    ELSE 'There is no correlation'
  END AS correlation,
  studiedAbroadAndMoved AS peopleStudiedAbroadAndMoved,
  totalPopulation
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when toFloat(changed)/(changed+stayed) > 0.5 then 'correlated' else 'uncorrelated' end": "correlated"
  }
]
```

**Actual Results:**
```json
[
  {
    "correlation": "There is a correlation",
    "peopleStudiedAbroadAndMoved": 24,
    "totalPopulation": 1
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 842
- **Execution Time:** 5.72s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 24: 24
**Status:** FAIL

#### Natural Language Query
```
Is there a correlation between the email of the person being Yahoo! and that person not working in the tech field? (assume it's correlated if it's true for more than half of the population)
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:HAD_POSITION]-(job:JobTitle)
where toLower(p.email) ends with '@yahoo.com'
with count(case when job.category = 'Technology' then 1 end) as tech,
     count(case when job.category <> 'Techonology' then 1 end) as notTech
return case when tech+notTech = 0 then 'no yahoo mails' when toFloat(tech)/(tech+notTech) > 0.5 then 'correlated' else 'uncorrelated' end;

```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p, toLower(p.email) AS lowerEmail, 
     (p)-[:WORKED_AT]->(:Company)-[:HAD_POSITION]->(j:JobTitle) AS workHistory
WITH p, 
     CASE 
       WHEN lowerEmail CONTAINS 'yahoo.com' THEN true 
       ELSE false 
     END AS isYahooEmail,
     CASE 
       WHEN any(job IN workHistory WHERE toLower(job.category) = 'tech') THEN false 
       ELSE true 
     END AS notInTechField
WITH count(p) AS totalPopulation,
     sum(CASE WHEN isYahooEmail AND notInTechField THEN 1 ELSE 0 END) AS yahooNotTechCount,
     sum(CASE WHEN isYahooEmail THEN 1 ELSE 0 END) AS yahooCount
RETURN 
  CASE 
    WHEN yahooCount > 0 AND (yahooNotTechCount * 1.0 / yahooCount) > 0.5 THEN 'Correlated'
    ELSE 'Not correlated'
  END AS correlation,
  yahooCount AS totalYahooUsers,
  yahooNotTechCount AS yahooUsersNotInTech,
  totalPopulation AS totalPopulation
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'j'. (line 3, column 53 (offset: 110))
"     (p)-[:WORKED_AT]->(:Company)-[:HAD_POSITION]->(j:JobTitle) AS workHistory"
                                                     ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when tech+notTech = 0 then 'no yahoo mails' when toFloat(tech)/(tech+notTech) > 0.5 then 'correlated' else 'uncorrelated' end": "no yahoo mails"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 934
- **Execution Time:** 10.03s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 25: 25
**Status:** FAIL

#### Natural Language Query
```
On average, how many sisters do people called Charles have?
```

#### Ground Truth Cypher
```cypher
match (charles:Person)
where charles.firstName = 'Charles'
optional match (charles)-[:IS_SIBLING]->(sister:Person)
where sister.gender = 'Female'
with charles, count(sister) as sisters
return avg(sisters)

```

#### Generated Cypher
```cypher
MATCH (p:Person {firstName: 'Charles'})
WITH p, [(p)-[:IS_SIBLING]-(sibling:Person) WHERE sibling.gender = 'Female' | sibling] AS sisters
RETURN avg(size(sisters)) AS avgSisters
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "avg(sisters)": 2.0
  }
]
```

**Actual Results:**
```json
[
  {
    "avgSisters": 4.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 732
- **Execution Time:** 4.60s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 26: 26
**Status:** PASS

#### Natural Language Query
```
How many Christophers are there that have or have had a friend named Jessica
```

#### Ground Truth Cypher
```cypher
match (christopher:Person)-[:IS_FRIEND]->(jessica:Person)
where christopher.firstName = 'Christopher'
and jessica.firstName = 'Jessica'
return count(distinct christopher);
```

#### Generated Cypher
```cypher
MATCH (christopher:Person)-[:IS_FRIEND]-(jessica:Person)
WHERE toLower(christopher.firstName) = 'christopher' AND toLower(jessica.firstName) = 'jessica'
RETURN COUNT(DISTINCT christopher) AS christopherCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct christopher)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "christopherCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 743
- **Execution Time:** 12.45s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 27: 27
**Status:** FAIL

#### Natural Language Query
```
How many people work in the same field they studied in?
```

#### Ground Truth Cypher
```cypher
match (f:FieldOfStudy)-[:STUDIED]-(p:Person)-[a:HAD_POSITION]-(job:JobTitle)
where f.category = job.category
and a.endYear is null
return count(distinct(p));
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED]->(f:FieldOfStudy)
WITH p, f
MATCH (p)-[:WORKED_AT]->(c:Company)
WITH p, f, c
MATCH (p)-[:HAD_POSITION]->(j:JobTitle)
WHERE toLower(f.category) = toLower(j.category)
RETURN COUNT(DISTINCT p) AS peopleWorkingInStudiedField
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct(p))": 0
  }
]
```

**Actual Results:**
```json
[
  {
    "peopleWorkingInStudiedField": 3
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 748
- **Execution Time:** 10.20s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 28: 28
**Status:** PASS

#### Natural Language Query
```
What percentage of people use their name as their email?

```

#### Ground Truth Cypher
```cypher
match (p:Person)
with count(p) as totalPeople,
     count(case when p.email is not null and toLower(p.email) contains toLower(p.firstName) then 1 end) as nameEmail
return toFloat(nameEmail) / totalPeople * 100;

```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE p.email IS NOT NULL AND p.firstName IS NOT NULL AND p.lastName IS NOT NULL
WITH p, toLower(p.firstName + '.' + p.lastName) AS namePart, toLower(split(p.email, '@')[0]) AS emailPart
WITH COUNT(CASE WHEN namePart = emailPart THEN 1 END) AS matchCount, COUNT(p) AS totalCount
RETURN toFloat(matchCount) / totalCount * 100 AS percentage
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "toFloat(nameEmail) / totalPeople * 100": 0.0
  }
]
```

**Actual Results:**
```json
[
  {
    "percentage": 0.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 776
- **Execution Time:** 12.61s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 29: 29
**Status:** FAIL

#### Natural Language Query
```
In which country are the most amount of people named Jordan?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]-(loc:Location)
where p.firstName = 'Jordan'
return loc.country, count(p)
order by count(p)
limit 1;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Claude API Error: Error code: 529 - {'type': 'error', 'error': {'type': 'overloaded_error', 'message': 'Overloaded'}}
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 33.90s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 30: 30
**Status:** PASS

#### Natural Language Query
```
What positions has Connie's sister worked as?
```

#### Ground Truth Cypher
```cypher
match (friend:Person)-[:IS_SIBLING]->(sister:Person)-[worked:HAD_POSITION]-(job:JobTitle)
where toLower(friend.firstName) = 'connie'
return distinct job.title;
```

#### Generated Cypher
```cypher
MATCH (connie:Person)-[:IS_SIBLING]->(sister:Person)-[worked:HAD_POSITION]->(position:JobTitle)
WHERE toLower(connie.firstName) = 'connie'
RETURN DISTINCT position.title AS SisterPositions
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "job.title": "Data Scientist"
  },
  {
    "job.title": "CTO"
  },
  {
    "job.title": "Doctor"
  },
  {
    "job.title": "Lawyer"
  },
  {
    "job.title": "Teacher"
  },
  {
    "job.title": "Manager"
  },
  {
    "job.title": "Director"
  },
  {
    "job.title": "Professor"
  }
]
```

**Actual Results:**
```json
[
  {
    "SisterPositions": "Data Scientist"
  },
  {
    "SisterPositions": "CTO"
  },
  {
    "SisterPositions": "Doctor"
  },
  {
    "SisterPositions": "Lawyer"
  },
  {
    "SisterPositions": "Teacher"
  },
  {
    "SisterPositions": "Manager"
  },
  {
    "SisterPositions": "Director"
  },
  {
    "SisterPositions": "Professor"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 731
- **Execution Time:** 17.61s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 31: 31
**Status:** FAIL

#### Natural Language Query
```
How many children on average does a parent have in Grenada?
```

#### Ground Truth Cypher
```cypher
match (child:Person)-[:IS_CHILD]->(parent:Person)-[:LIVES_IN]-(loc:Location)
where loc.country = 'Grenada'
with parent, count(child) as children
return avg(children);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:IS_PARENT]->(c:Person)
WHERE toLower(p.nationality) = 'grenada'
WITH p, COUNT(c) AS childCount
RETURN AVG(childCount) AS averageChildrenPerParent
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "avg(children)": 2.0
  }
]
```

**Actual Results:**
```json
[
  {
    "averageChildrenPerParent": null
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 728
- **Execution Time:** 6.66s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 32: 32
**Status:** FAIL

#### Natural Language Query
```
How many people have studied in universities located in French Southern Territories and have friends who work in finance?
```

#### Ground Truth Cypher
```cypher
match (uni:EducationalInstitution)-[:STUDIED_AT]-(p:Person)-[:IS_FRIEND]-(friend:Person)-[:HAD_POSITION]-(job:JobTitle)
where toLower(uni.country) = 'french southern territories'
and toLower(job.category) = 'finance'
return count(distinct p);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:STUDIED_AT]->(u:EducationalInstitution)-[:LIVES_IN]->(l:Location {country: "French Southern Territories"})
WITH p
MATCH (p)-[:IS_FRIEND]->(f:Person)-[:WORKED_AT]->(c:Company)
WHERE toLower(c.industry) = 'finance'
RETURN COUNT(DISTINCT p) AS peopleCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct p)": 8
  }
]
```

**Actual Results:**
```json
[
  {
    "peopleCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 771
- **Execution Time:** 10.01s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 33: 33
**Status:** FAIL

#### Natural Language Query
```
How many people have worked in the education industry and is married to someone who lives in Grenada?
```

#### Ground Truth Cypher
```cypher
match (job:JobTitle)-[:HAD_POSITION]-(p:Person)-[:IS_WIFE|IS_HUSBAND]->(spouse:Person)-[:LIVES_IN]-(loc:Location)
where loc.country = 'Grenada'
and job.category = 'Education'
return count(distinct p);

```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:WORKED_AT]->(c:Company {industry: 'education'})
WHERE EXISTS((p)-[:IS_HUSBAND|IS_WIFE]-(:Person)-[:LIVES_IN]->(:Location {name: 'Grenada'}))
RETURN COUNT(DISTINCT p) AS count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(distinct p)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "count": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 746
- **Execution Time:** 25.12s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 34: 34
**Status:** PASS

#### Natural Language Query
```
How correlated are education and career? (assume it's correlated if it's true for more than half of the population)
```

#### Ground Truth Cypher
```cypher
match (job:JobTitle)-[:HAD_POSITION]-(p:Person)
optional match (p)-[:STUDIED_AT]-(uni:EducationalInstitution)
with count(case when uni.id is not null then 1 end) as studied,
     count(case when uni.id is null then 1 end) as didnt
return case when toFloat(studied)/(studied+didnt) > 0.5 then 'correlated' else 'uncorrelated' end;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH count(p) as totalPopulation
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)
WITH totalPopulation, p, collect(e) as educations
MATCH (p)-[:WORKED_AT]->(c:Company)
WITH totalPopulation, p, educations, collect(c) as companies
WHERE size(educations) > 0 AND size(companies) > 0
WITH totalPopulation, count(p) as correlatedCount
RETURN 
  CASE 
    WHEN (correlatedCount * 1.0 / totalPopulation) > 0.5 
    THEN 'Education and career are correlated' 
    ELSE 'Education and career are not correlated' 
  END as result, 
  round((correlatedCount * 100.0 / totalPopulation), 2) as percentageCorrelated
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when toFloat(studied)/(studied+didnt) > 0.5 then 'correlated' else 'uncorrelated' end": "correlated"
  }
]
```

**Actual Results:**
```json
[
  {
    "result": "Education and career are correlated",
    "percentageCorrelated": 60.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 858
- **Execution Time:** 26.02s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 35: 35
**Status:** FAIL

#### Natural Language Query
```
How are Matthew and Theresa related?
```

#### Ground Truth Cypher
```cypher
match (matthew:Person), (theresa:Person), p = shortestPath((matthew)-[*]-(theresa))
where matthew.firstName = 'Matthew'
and theresa.firstName = 'Theresa'
return p;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Path is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 10.44s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 36: 36
**Status:** FAIL

#### Natural Language Query
```
Is it possible to get all people from just one person's friends' friends (and so on)? One of the person's name is Matthew.
```

#### Ground Truth Cypher
```cypher
match (n:Person)
with count(n) as allPeople
match (p:Person)
where p.firstName = 'Matthew'
with allPeople, p
match (p)-[:IS_FRIEND*0..]-(friend:Person)
with allPeople, count(distinct friend) as friends
return case when friends = allPeople then 'Yes' else 'No' end;

```

#### Generated Cypher
```cypher
MATCH (matthew:Person {firstName: 'Matthew'})
WITH matthew
CALL apoc.path.subgraphAll(matthew, {
  relationshipFilter: 'IS_FRIEND',
  maxLevel: 10
}) YIELD nodes
WITH DISTINCT nodes AS allConnectedPeople
UNWIND allConnectedPeople AS person
RETURN person.firstName + ' ' + person.lastName AS fullName
ORDER BY fullName
```

#### Error Analysis
```
{code: Neo.ClientError.Procedure.ProcedureNotFound} {message: There is no procedure with the name `apoc.path.subgraphAll` registered for this database instance. Please ensure you've spelled the procedure name correctly and that the procedure is properly deployed.}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "case when friends = allPeople then 'Yes' else 'No' end": "Yes"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 782
- **Execution Time:** 4.83s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 37: 37
**Status:** FAIL

#### Natural Language Query
```
On average, how many hops does it take from people living in New Zealand to people working in Johnson-Rogers, Hooper PLC, Patterson, Camacho and White, Rogers-Hobbs, or Ruiz Ltd

```

#### Ground Truth Cypher
```cypher
match (kutaiseli:Person)-[:LIVES_IN]-(kutaisi:Location), (maangeli:Person)-[:WORKED_AT]-(maang:Company), path = shortestPath((kutaiseli)-[*]-(maangeli))
where toLower(kutaisi.country) = 'new zealand'
and maang.name in ['Johnson-Rogers', 'Hooper PLC', 'Patterson, Camacho and White', 'Rogers-Hobbs', 'Ruiz Ltd']
and kutaiseli <> maangeli
return avg(length(path));
```

#### Generated Cypher
```cypher
MATCH (nz:Location {name: 'New Zealand'})
MATCH (p1:Person)-[:LIVES_IN]->(nz)
MATCH (c:Company) WHERE c.name IN ['Johnson-Rogers, Hooper PLC', 'Patterson, Camacho and White', 'Rogers-Hobbs', 'Ruiz Ltd']
MATCH (p2:Person)-[:WORKED_AT]->(c)
WITH p1, p2
MATCH path = shortestPath((p1)-[:IS_FRIEND*1..6]-(p2))
WHERE all(r IN relationships(path) WHERE type(r) = 'IS_FRIEND')
RETURN avg(length(path)) AS averageHops
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "avg(length(path))": 1.7906432748538008
  }
]
```

**Actual Results:**
```json
[
  {
    "averageHops": null
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 819
- **Execution Time:** 4.96s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 38: 38
**Status:** FAIL

#### Natural Language Query
```
Based on country, how many different jobs did a person have on average?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]->(loc:Location)
where loc.country is not null
optional match (p)-[:HAD_POSITION]->(jt:JobTitle)
with p, loc.country as countryName, count(distinct jt.title) as numberOfDistinctJobs
return countryName, avg(numberOfDistinctJobs) as averageDistinctJobsPerPersonInCountry
order by averageDistinctJobsPerPersonInCountry desc;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WITH p, l.country AS country
MATCH (p)-[w:WORKED_AT]->(c:Company)
WITH p, country, COLLECT(DISTINCT w.companyId) AS companies
RETURN country, AVG(SIZE(companies)) AS avgJobsPerPerson
ORDER BY avgJobsPerPerson DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "countryName": "Korea",
    "averageDistinctJobsPerPersonInCountry": 5.142857142857143
  },
  {
    "countryName": "Kazakhstan",
    "averageDistinctJobsPerPersonInCountry": 5.0
  },
  {
    "countryName": "Seychelles",
    "averageDistinctJobsPerPersonInCountry": 4.5
  },
  {
    "countryName": "New Zealand",
    "averageDistinctJobsPerPersonInCountry": 4.4
  },
  {
    "countryName": "Kiribati",
    "averageDistinctJobsPerPersonInCountry": 4.0
  },
  {
    "countryName": "Grenada",
    "averageDistinctJobsPerPersonInCountry": 4.0
  },
  {
    "countryName": "Cape Verde",
    "averageDistinctJobsPerPersonInCountry": 4.0
  },
  {
    "countryName": "Greenland",
    "averageDistinctJobsPerPersonInCountry": 3.75
  },
  {
    "countryName": "Burundi",
    "averageDistinctJobsPerPersonInCountry": 3.6666666666666665
  },
  {
    "countryName": "Syrian Arab Republic",
    "averageDistinctJobsPerPersonInCountry": 3.5
  }
]
```

**Actual Results:**
```json
[
  {
    "country": "New Zealand",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Kiribati",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Korea",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Seychelles",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Kazakhstan",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Grenada",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Burundi",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Cape Verde",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Greenland",
    "avgJobsPerPerson": 0.0
  },
  {
    "country": "Syrian Arab Republic",
    "avgJobsPerPerson": 0.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 754
- **Execution Time:** 4.05s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 39: 39
**Status:** FAIL

#### Natural Language Query
```
Find all men who married spouses older than their sisters
```

#### Ground Truth Cypher
```cypher
match (sister:Person)<-[:IS_SIBLING]-(man:Person)-[:IS_WIFE|IS_HUSBAND]->(spouse:Person)
where toLower(sister.gender) = 'female'
and toLower(man.gender) = 'male'
and spouse.birthDate < sister.birthDate
return man.firstName
```

#### Generated Cypher
```cypher
MATCH (m:Person {gender: 'Male'})-[:IS_HUSBAND]->(w:Person)
WHERE m.birthDate < w.birthDate
WITH m, w
MATCH (m)-[:IS_SIBLING]->(s:Person {gender: 'Female'})
WHERE m.birthDate > s.birthDate
RETURN DISTINCT m.firstName + ' ' + m.lastName AS Man,
       w.firstName + ' ' + w.lastName AS Wife,
       s.firstName + ' ' + s.lastName AS Sister
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "man.firstName": "Charles"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 771
- **Execution Time:** 3.89s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 40: 40
**Status:** FAIL

#### Natural Language Query
```
Find locations such that more men than women live there.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]-(l:Location)
with l.name as location, sum(case when toLower(p.gender) = 'male' then 1 else 0 end) as males, sum(case when toLower(p.gender) = 'female' then 1 else 0 end) as females
where males>females
return location
```

#### Generated Cypher
```cypher
MATCH (l:Location)<-[:LIVES_IN]-(p:Person)
WITH l, COUNT(CASE WHEN p.gender = 'male' THEN 1 END) AS maleCount,
     COUNT(CASE WHEN p.gender = 'female' THEN 1 END) AS femaleCount
WHERE maleCount > femaleCount
RETURN l.name AS LocationName, maleCount, femaleCount
ORDER BY maleCount - femaleCount DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "location": "Stephaniemouth"
  },
  {
    "location": "Rivasside"
  },
  {
    "location": "Lake Michelle"
  },
  {
    "location": "Simsview"
  },
  {
    "location": "Patricialand"
  },
  {
    "location": "East Patrick"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 762
- **Execution Time:** 4.09s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 41: 41
**Status:** PASS

#### Natural Language Query
```
Find locations where more men than women live, and display the population of men and women in such places.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]-(l:Location)
with l.name as location, sum(case when toLower(p.gender) = 'male' then 1 else 0 end) as males, sum(case when toLower(p.gender) = 'female' then 1 else 0 end) as females
where males>females
return location, males, females;
```

#### Generated Cypher
```cypher
MATCH (l:Location)<-[:LIVES_IN]-(p:Person)
WITH l, 
     COUNT(CASE WHEN toLower(p.gender) = 'male' THEN p END) AS maleCount,
     COUNT(CASE WHEN toLower(p.gender) = 'female' THEN p END) AS femaleCount
WHERE maleCount > femaleCount
RETURN l.name AS Location, 
       l.population AS TotalPopulation, 
       maleCount AS MalePopulation, 
       femaleCount AS FemalePopulation
ORDER BY l.population DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "location": "Stephaniemouth",
    "males": 3,
    "females": 2
  },
  {
    "location": "Rivasside",
    "males": 5,
    "females": 3
  },
  {
    "location": "Lake Michelle",
    "males": 5,
    "females": 2
  },
  {
    "location": "Simsview",
    "males": 5,
    "females": 1
  },
  {
    "location": "Patricialand",
    "males": 2,
    "females": 1
  },
  {
    "location": "East Patrick",
    "males": 4,
    "females": 2
  }
]
```

**Actual Results:**
```json
[
  {
    "Location": "Patricialand",
    "TotalPopulation": 12819117,
    "MalePopulation": 2,
    "FemalePopulation": 1
  },
  {
    "Location": "Stephaniemouth",
    "TotalPopulation": 11636146,
    "MalePopulation": 3,
    "FemalePopulation": 2
  },
  {
    "Location": "Lake Michelle",
    "TotalPopulation": 9619364,
    "MalePopulation": 5,
    "FemalePopulation": 2
  },
  {
    "Location": "Simsview",
    "TotalPopulation": 9234763,
    "MalePopulation": 5,
    "FemalePopulation": 1
  },
  {
    "Location": "East Patrick",
    "TotalPopulation": 4875083,
    "MalePopulation": 4,
    "FemalePopulation": 2
  },
  {
    "Location": "Rivasside",
    "TotalPopulation": 3376763,
    "MalePopulation": 5,
    "FemalePopulation": 3
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 800
- **Execution Time:** 5.06s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 42: 42
**Status:** PASS

#### Natural Language Query
```
Return top 3 education institutions with most foreign students.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[lived:LIVED_IN]-(l:Location)
order by p, lived.startYear
with p, collect(l.country)[0] as firstCountry
match (p)-[:STUDIED_AT]-(e:EducationalInstitution)
where firstCountry <> e.country
with e.name as institution, count(*) as foreignStudents
order by foreignStudents desc
limit 3
return institution, foreignStudents;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE toLower(p.nationality) <> toLower(e.country)
WITH e, COUNT(DISTINCT p) AS foreignStudentCount
ORDER BY foreignStudentCount DESC
LIMIT 3
RETURN e.name AS institution, e.country AS country, foreignStudentCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "institution": "South Jeffrey Institute",
    "foreignStudents": 6
  },
  {
    "institution": "Priceshire Institute",
    "foreignStudents": 6
  },
  {
    "institution": "Port Nicoleshire Institute",
    "foreignStudents": 5
  }
]
```

**Actual Results:**
```json
[
  {
    "institution": "Smithstad University",
    "country": "French Southern Territories",
    "foreignStudentCount": 9
  },
  {
    "institution": "South Jeffrey Institute",
    "country": "Jordan",
    "foreignStudentCount": 8
  },
  {
    "institution": "Priceshire Institute",
    "country": "Yemen",
    "foreignStudentCount": 7
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 757
- **Execution Time:** 5.03s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 43: 43
**Status:** PASS

#### Natural Language Query
```
Return education institutions with most foreign students
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[lived:LIVED_IN]-(l:Location)
order by p, lived.startYear
with p, collect(l.country)[0] as firstCountry
match (p)-[:STUDIED_AT]-(e:EducationalInstitution)
where firstCountry <> e.country
with e.name as institution, count(*) as foreignStudents
order by foreignStudents desc
return institution;
```

#### Generated Cypher
```cypher
MATCH (ei:EducationalInstitution)<-[:STUDIED_AT]-(p:Person)
WHERE toLower(p.nationality) <> toLower(ei.country)
WITH ei, COUNT(DISTINCT p) AS foreignStudentCount
ORDER BY foreignStudentCount DESC
LIMIT 10
RETURN ei.name AS institution, ei.country, foreignStudentCount
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "institution": "South Jeffrey Institute"
  },
  {
    "institution": "Priceshire Institute"
  },
  {
    "institution": "Castanedachester Institute"
  },
  {
    "institution": "Port Nicoleshire Institute"
  },
  {
    "institution": "Smithstad University"
  }
]
```

**Actual Results:**
```json
[
  {
    "institution": "Smithstad University",
    "ei.country": "French Southern Territories",
    "foreignStudentCount": 9
  },
  {
    "institution": "South Jeffrey Institute",
    "ei.country": "Jordan",
    "foreignStudentCount": 8
  },
  {
    "institution": "Priceshire Institute",
    "ei.country": "Yemen",
    "foreignStudentCount": 7
  },
  {
    "institution": "Castanedachester Institute",
    "ei.country": "Mauritania",
    "foreignStudentCount": 6
  },
  {
    "institution": "Port Nicoleshire Institute",
    "ei.country": "Hong Kong",
    "foreignStudentCount": 5
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 753
- **Execution Time:** 3.58s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 44: 44
**Status:** PASS

#### Natural Language Query
```
Who's older than their husband?
```

#### Ground Truth Cypher
```cypher
match (husband:Person)-[:IS_HUSBAND]->(spouse:Person)
where husband.birthDate > spouse.birthDate
return spouse.firstName
```

#### Generated Cypher
```cypher
MATCH (w:Person)-[:IS_WIFE]->(h:Person)
WHERE date(w.birthDate) < date(h.birthDate)
RETURN w.firstName + ' ' + w.lastName AS Wife, h.firstName + ' ' + h.lastName AS Husband,
       w.birthDate AS WifeBirthDate, h.birthDate AS HusbandBirthDate
ORDER BY w.birthDate
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "spouse.firstName": "Charles"
  }
]
```

**Actual Results:**
```json
[
  {
    "Wife": "Charles Taylor",
    "Husband": "Johnny Campos",
    "WifeBirthDate": "1934-01-16",
    "HusbandBirthDate": "1943-03-10"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** easy
- **Tokens Used:** 746
- **Execution Time:** 4.24s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 45: 45
**Status:** PASS

#### Natural Language Query
```
Find the oldest married person in each city.
```

#### Ground Truth Cypher
```cypher
match (l:Location)
where toLower(l.type) = 'city'
optional match (l)-[:LIVES_IN]-(p:Person)-[:IS_HUSBAND|IS_WIFE]->(spouse:Person)
with l.name as city, p
order by city, p.birthDate
with city, collect(p)[0] as oldestMarriedPerson
return city, oldestMarriedPerson.firstName
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVES_IN]->(city:Location)
WHERE EXISTS((p)-[:IS_HUSBAND|IS_WIFE]-())
WITH city, p, p.birthDate AS birthDate
ORDER BY birthDate
WITH city, COLLECT(p)[0] AS oldestPerson
RETURN city.name AS City, oldestPerson.firstName + ' ' + oldestPerson.lastName AS OldestMarriedPerson, oldestPerson.birthDate AS BirthDate
ORDER BY city.name
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "city": "East Patrick",
    "oldestMarriedPerson.firstName": null
  },
  {
    "city": "Karenview",
    "oldestMarriedPerson.firstName": "Savannah"
  },
  {
    "city": "Lake Justinview",
    "oldestMarriedPerson.firstName": "Mark"
  },
  {
    "city": "Lake Michelle",
    "oldestMarriedPerson.firstName": "Kevin"
  },
  {
    "city": "North Robert",
    "oldestMarriedPerson.firstName": "Juan"
  },
  {
    "city": "Patricialand",
    "oldestMarriedPerson.firstName": null
  },
  {
    "city": "Perryborough",
    "oldestMarriedPerson.firstName": "Michael"
  },
  {
    "city": "Rivasside",
    "oldestMarriedPerson.firstName": null
  },
  {
    "city": "Simsview",
    "oldestMarriedPerson.firstName": "Charles"
  },
  {
    "city": "Stephaniemouth",
    "oldestMarriedPerson.firstName": "Johnny"
  }
]
```

**Actual Results:**
```json
[
  {
    "City": "Karenview",
    "OldestMarriedPerson": "Savannah Delacruz",
    "BirthDate": "1935-02-12"
  },
  {
    "City": "Lake Justinview",
    "OldestMarriedPerson": "Mark Johnson",
    "BirthDate": "1928-06-16"
  },
  {
    "City": "Lake Michelle",
    "OldestMarriedPerson": "Kevin Johnson",
    "BirthDate": "1929-11-07"
  },
  {
    "City": "North Robert",
    "OldestMarriedPerson": "Juan Calderon",
    "BirthDate": "1948-05-13"
  },
  {
    "City": "Perryborough",
    "OldestMarriedPerson": "Michael Robinson",
    "BirthDate": "2000-03-19"
  },
  {
    "City": "Simsview",
    "OldestMarriedPerson": "Charles Taylor",
    "BirthDate": "1934-01-16"
  },
  {
    "City": "Stephaniemouth",
    "OldestMarriedPerson": "Johnny Campos",
    "BirthDate": "1943-03-10"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 770
- **Execution Time:** 5.12s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 46: 46
**Status:** FAIL

#### Natural Language Query
```
Family trees where everyone works.
```

#### Ground Truth Cypher
```cypher
match (root)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING*0..50]-(member:Person)
with root, collect(distinct member) as familyMembers
where all(member in familyMembers where exists {
        (member)-[:WORKED_AT]->(c:Company)
        })
and size(familyMembers) > 1
return root.firstName + ' ' + root.lastName as familyRoot,
       [member in familyMembers | member.firstName + ' ' + member.lastName] as employedFamilyMembers
       order by size(familyMembers) desc;
```

#### Generated Cypher
```cypher
MATCH (root:Person)
WHERE NOT (:Person)-[:IS_PARENT]->(root)
WITH root
MATCH path = (root)-[:IS_PARENT*0..3]->(descendant:Person)
WITH DISTINCT root, COLLECT(DISTINCT descendant) AS familyMembers
WHERE ALL(member IN familyMembers WHERE EXISTS((member)-[:WORKED_AT]->(:Company)))
AND SIZE(familyMembers) > 1
RETURN root.firstName + ' ' + root.lastName AS FamilyHead, 
       SIZE(familyMembers) AS FamilySize,
       [member IN familyMembers | member.firstName + ' ' + member.lastName] AS WorkingFamilyMembers
ORDER BY FamilySize DESC
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[
  {
    "FamilyHead": "Mark Johnson",
    "FamilySize": 8,
    "WorkingFamilyMembers": [
      "Mark Johnson",
      "Connie Lawrence",
      "Mia Sutton",
      "Charles Taylor",
      "Juan Calderon",
      "Debra Clark",
      "Joseph Maddox",
      "Jordan Gonzalez"
    ]
  },
  {
    "FamilyHead": "Kevin Johnson",
    "FamilySize": 8,
    "WorkingFamilyMembers": [
      "Kevin Johnson",
      "Connie Lawrence",
      "Mia Sutton",
      "Charles Taylor",
      "Juan Calderon",
      "Debra Clark",
      "Joseph Maddox",
      "Jordan Gonzalez"
    ]
  },
  {
    "FamilyHead": "Johnny Campos",
    "FamilySize": 3,
    "WorkingFamilyMembers": [
      "Johnny Campos",
      "Joseph Maddox",
      "Jordan Gonzalez"
    ]
  },
  {
    "FamilyHead": "Anna Davis",
    "FamilySize": 2,
    "WorkingFamilyMembers": [
      "Anna Davis",
      "Juan Calderon"
    ]
  },
  {
    "FamilyHead": "Jessica Chavez",
    "FamilySize": 2,
    "WorkingFamilyMembers": [
      "Jessica Chavez",
      "Jordan Gonzalez"
    ]
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 814
- **Execution Time:** 5.55s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 47: 47
**Status:** PASS

#### Natural Language Query
```
Find isolated individuals.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where not exists { (p)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING]-(p2:Person) }
and not exists { (p)-[:IS_FRIEND]-() }
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE NOT EXISTS {
    (p)-[:IS_FRIEND|WORKED_AT|HAD_POSITION|LIVES_IN|LIVED_IN|IS_HUSBAND|IS_PARENT|STUDIED_AT|STUDIED|IS_WIFE|IS_CHILD|IS_SIBLING]-()
}
RETURN p
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 724
- **Execution Time:** 3.10s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 48: 48
**Status:** FAIL

#### Natural Language Query
```
Find second cousins.
```

#### Ground Truth Cypher
```cypher
match (a:Person)-[:IS_CHILD]->(pa1:Person)-[:IS_CHILD]->(gpa:Person),
      (b:Person)-[:IS_CHILD]->(pb1:Person)-[:IS_CHILD]->(gpb:Person),
      (gpa)-[:IS_CHILD]->(ggp:Person)<-[:IS_CHILD]-(gpb)
where a <> b
and not (a)-[:IS_CHILD]->(:Person)<-[:IS_CHILD]-(b)
and not (a)-[:IS_CHILD]->(:Person)-[:IS_CHILD]->(:Person)<-[:IS_CHILD]-(:Person)<-[:IS_CHILD]-(b)
return a.firstName + ' ' + a.lastName as person1,
       b.firstName + ' ' + b.lastName as person2
       order by person1, person2;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Node is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 5.49s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 49: 49
**Status:** FAIL

#### Natural Language Query
```
Who has more cousins than siblings?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
optional match (p)-[:IS_SIBLING]-(sibling:Person)
with p, count(distinct sibling) AS siblingCount
optional match (p)-[:IS_CHILD]->(parent:Person)-[:IS_SIBLING]->(auntOrUncle:Person)<-[:IS_CHILD]-(cousin:Person)
with p, siblingCount, count(distinct cousin) as cousinCount
where (cousinCount > siblingCount)
return p.firstName, siblingCount, cousinCount;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p,
     size([(p)-[:IS_SIBLING]->(sibling) | sibling]) AS siblingCount,
     size([(p)<-[:IS_CHILD]-(parent)-[:IS_SIBLING]->(uncle_aunt)-[:IS_PARENT]->(cousin) WHERE cousin <> p | cousin]) AS cousinCount
WHERE cousinCount > siblingCount
RETURN p.firstName + ' ' + p.lastName AS name, cousinCount, siblingCount
ORDER BY cousinCount DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Juan",
    "siblingCount": 0,
    "cousinCount": 2
  },
  {
    "p.firstName": "Debra",
    "siblingCount": 0,
    "cousinCount": 2
  },
  {
    "p.firstName": "Joseph",
    "siblingCount": 0,
    "cousinCount": 2
  }
]
```

**Actual Results:**
```json
[
  {
    "name": "Mark Johnson",
    "cousinCount": 6,
    "siblingCount": 0
  },
  {
    "name": "Kevin Johnson",
    "cousinCount": 6,
    "siblingCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 771
- **Execution Time:** 4.70s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 50: 50
**Status:** FAIL

#### Natural Language Query
```
Which siblings studied before being born?
```

#### Ground Truth Cypher
```cypher
match (n)
where 1=2
return n;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_SIBLING]-(p2:Person)
WHERE p1.id < p2.id
WITH p1, p2
MATCH (p1)-[s1:STUDIED_AT]->(e:EducationalInstitution)
MATCH (p2)-[s2:STUDIED_AT]->(e)
WHERE s1.startYear < toInteger(left(p1.birthDate, 4)) OR s2.startYear < toInteger(left(p2.birthDate, 4))
RETURN p1.firstName + ' ' + p1.lastName AS Sibling1, p2.firstName + ' ' + p2.lastName AS Sibling2, e.name AS Institution,
       CASE WHEN s1.startYear < toInteger(left(p1.birthDate, 4)) THEN p1.firstName + ' ' + p1.lastName
            ELSE p2.firstName + ' ' + p2.lastName END AS StudiedBeforeBirth
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** paradox
- **Difficulty:** hard
- **Tokens Used:** 825
- **Execution Time:** 5.51s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 51: 51
**Status:** FAIL

#### Natural Language Query
```
Who's the oldest person without their family?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where not (p)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING]-(:Person)
return p.firstName
order by p.birthDate
limit 1;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Node is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 32.66s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 52: 52
**Status:** PASS

#### Natural Language Query
```
Who's the youngest person with kids?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:IS_PARENT]->(c:Person)
return p.firstName
order by p.birthDate desc
limit 1;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:IS_PARENT]->(child:Person)
WITH p, COUNT(child) AS childCount, p.birthDate AS birthDate
WHERE childCount > 0
RETURN p.firstName + ' ' + p.lastName AS youngestParent, birthDate
ORDER BY birthDate DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Michael"
  }
]
```

**Actual Results:**
```json
[
  {
    "youngestParent": "Michael Robinson",
    "birthDate": "2000-03-19"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 738
- **Execution Time:** 3.18s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 53: 53
**Status:** FAIL

#### Natural Language Query
```
Who is the most well traveled person?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVED_IN|LIVES_IN]->(loc:Location)
with p, count(distinct loc) as locationCount
order by locationCount desc
limit 1
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p, size((p)-[:LIVED_IN]->()) + size((p)-[:LIVES_IN]->()) AS totalLocations
RETURN p.firstName + ' ' + p.lastName AS mostTraveledPerson, totalLocations
ORDER BY totalLocations DESC
LIMIT 1
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 30))
"WITH p, size((p)-[:LIVED_IN]->()) + size((p)-[:LIVES_IN]->()) AS totalLocations"
              ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Johnny"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 734
- **Execution Time:** 5.35s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 54: 54
**Status:** FAIL

#### Natural Language Query
```
Who is the most popular person with their friends?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:IS_FRIEND]-(:Person)
with p, count(*) as friendCount
order by friendCount desc
limit 1
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p, size((p)-[:IS_FRIEND]-()) AS friendCount
ORDER BY friendCount DESC
LIMIT 1
RETURN p.firstName + ' ' + p.lastName AS mostPopularPerson, friendCount
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 30))
"WITH p, size((p)-[:IS_FRIEND]-()) AS friendCount"
              ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Eric"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 728
- **Execution Time:** 3.02s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 55: 55
**Status:** FAIL

#### Natural Language Query
```
Find people who have changed location 3 times.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN|LIVED_IN]-(l:Location)
with p, count(l) as locations
where locations > 3
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WITH p, [(p)-[:LIVED_IN]->(l:Location) | l] AS locations
WHERE size(locations) = 3
RETURN p.firstName + ' ' + p.lastName AS name, [loc.name for loc in locations] AS livedInLocations
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'for': expected an expression, ',' or ']' (line 4, column 58 (offset: 157))
"RETURN p.firstName + ' ' + p.lastName AS name, [loc.name for loc in locations] AS livedInLocations"
                                                          ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Johnny"
  },
  {
    "p.firstName": "Stephanie"
  },
  {
    "p.firstName": "Thomas"
  },
  {
    "p.firstName": "Eric"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Vanessa"
  },
  {
    "p.firstName": "Eugene"
  },
  {
    "p.firstName": "Steve"
  },
  {
    "p.firstName": "Tammy"
  },
  {
    "p.firstName": "Charles"
  },
  {
    "p.firstName": "Connie"
  },
  {
    "p.firstName": "Crystal"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 734
- **Execution Time:** 3.80s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 56: 56
**Status:** FAIL

#### Natural Language Query
```
Show people who are friends on Facebook.
```

#### Ground Truth Cypher
```cypher
match (n)
 where 1=2
return n;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[r:IS_FRIEND]->(p2:Person)
WHERE toLower(r.since) CONTAINS 'facebook'
RETURN p1.firstName + ' ' + p1.lastName AS Person1, p2.firstName + ' ' + p2.lastName AS Person2
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** Inconclusive
- **Difficulty:** medium
- **Tokens Used:** 728
- **Execution Time:** 3.32s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 57: 57
**Status:** PASS

#### Natural Language Query
```
List people whose jobs rhyme with the word preacher.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:HAD_POSITION]->(jt:JobTitle)
where toLower(jt.title) ends with 'eacher'
return distinct p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:HAD_POSITION]->(j:JobTitle)
WHERE toLower(j.title) =~ '.*cher$'
RETURN DISTINCT p.firstName + ' ' + p.lastName AS name, j.title AS job
ORDER BY name
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Juan"
  },
  {
    "p.firstName": "Savannah"
  },
  {
    "p.firstName": "Mia"
  },
  {
    "p.firstName": "Johnny"
  },
  {
    "p.firstName": "Joseph"
  },
  {
    "p.firstName": "Jessica"
  },
  {
    "p.firstName": "Jordan"
  },
  {
    "p.firstName": "Tracey"
  },
  {
    "p.firstName": "Crystal"
  },
  {
    "p.firstName": "Nathaniel"
  },
  {
    "p.firstName": "David"
  },
  {
    "p.firstName": "Samuel"
  },
  {
    "p.firstName": "Theresa"
  },
  {
    "p.firstName": "William"
  },
  {
    "p.firstName": "Todd"
  },
  {
    "p.firstName": "Tammy"
  },
  {
    "p.firstName": "Michael"
  },
  {
    "p.firstName": "Angel"
  }
]
```

**Actual Results:**
```json
[
  {
    "name": "Angel Riggs",
    "job": "Teacher"
  },
  {
    "name": "Crystal Whitehead",
    "job": "Teacher"
  },
  {
    "name": "David Lee",
    "job": "Teacher"
  },
  {
    "name": "Jessica Chavez",
    "job": "Teacher"
  },
  {
    "name": "Johnny Campos",
    "job": "Teacher"
  },
  {
    "name": "Jordan Gonzalez",
    "job": "Teacher"
  },
  {
    "name": "Joseph Maddox",
    "job": "Teacher"
  },
  {
    "name": "Joseph Williams",
    "job": "Teacher"
  },
  {
    "name": "Juan Calderon",
    "job": "Teacher"
  },
  {
    "name": "Mia Sutton",
    "job": "Teacher"
  },
  {
    "name": "Michael Orr",
    "job": "Teacher"
  },
  {
    "name": "Nathaniel Khan",
    "job": "Teacher"
  },
  {
    "name": "Samuel Wagner",
    "job": "Teacher"
  },
  {
    "name": "Savannah Delacruz",
    "job": "Teacher"
  },
  {
    "name": "Tammy Ryan",
    "job": "Teacher"
  },
  {
    "name": "Theresa Vazquez",
    "job": "Teacher"
  },
  {
    "name": "Todd Wilson",
    "job": "Teacher"
  },
  {
    "name": "Tracey Hickman",
    "job": "Teacher"
  },
  {
    "name": "William Brady",
    "job": "Teacher"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 727
- **Execution Time:** 3.42s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 58: 58
**Status:** FAIL

#### Natural Language Query
```
Find people currently living in a city they were born in.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:LIVES_IN]->(loc:Location)
where p.birthPlace = loc.name
return p.firstName;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Claude API Error: Error code: 529 - {'type': 'error', 'error': {'type': 'overloaded_error', 'message': 'Overloaded'}}
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 34.26s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 59: 60
**Status:** PASS

#### Natural Language Query
```
Find siblings who studied the same things.
```

#### Ground Truth Cypher
```cypher
match (a:Person)-[:IS_SIBLING]->(b:Person),
(a)-[:STUDIED]->(fieldA:FieldOfStudy),
(b)-[:STUDIED]->(fieldB:FieldOfStudy)
where fieldA.name = fieldB.name
return distinct a.firstName, b.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_SIBLING]->(p2:Person)
WHERE id(p1) < id(p2)
WITH p1, p2
MATCH (p1)-[:STUDIED]->(f:FieldOfStudy)<-[:STUDIED]-(p2)
RETURN p1.firstName + ' ' + p1.lastName AS Sibling1,
       p2.firstName + ' ' + p2.lastName AS Sibling2,
       collect(f.name) AS SharedFields
ORDER BY size(SharedFields) DESC
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 761
- **Execution Time:** 5.11s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 60: 61
**Status:** PASS

#### Natural Language Query
```
Find palindromic first names in the database.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where toLower(p.firstName) = reverse(toLower(p.firstName))
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE toLower(p.firstName) = reverse(toLower(p.firstName))
RETURN p.firstName AS PalindromicFirstName
ORDER BY PalindromicFirstName
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Anna"
  }
]
```

**Actual Results:**
```json
[
  {
    "PalindromicFirstName": "Anna"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 721
- **Execution Time:** 3.33s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 61: 62
**Status:** FAIL

#### Natural Language Query
```
Find all the people who are both a child and a parent.
```

#### Ground Truth Cypher
```cypher
match (child:Person)-[:IS_CHILD]->(p:Person)-[:IS_CHILD]->(parent:Person)
return distinct p.firstName;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Node is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 2.79s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 62: 63
**Status:** PASS

#### Natural Language Query
```
List people who have both a parent and a child in the graph.
```

#### Ground Truth Cypher
```cypher
match (child:Person)-[:IS_CHILD]->(p:Person)-[:IS_CHILD]->(parent:Person)
return distinct p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE EXISTS((p)<-[:IS_PARENT]-(:Person))
  AND EXISTS((p)-[:IS_PARENT]->(:Person))
RETURN p.firstName + ' ' + p.lastName AS name, p.id AS id
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Connie"
  },
  {
    "p.firstName": "Mia"
  },
  {
    "p.firstName": "Charles"
  },
  {
    "p.firstName": "Joseph"
  }
]
```

**Actual Results:**
```json
[
  {
    "name": "Connie Lawrence",
    "id": "p3"
  },
  {
    "name": "Mia Sutton",
    "id": "p7"
  },
  {
    "name": "Charles Taylor",
    "id": "p10"
  },
  {
    "name": "Joseph Maddox",
    "id": "p12"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 727
- **Execution Time:** 2.71s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 63: 64
**Status:** FAIL

#### Natural Language Query
```
Find married couples that live in different cities.
```

#### Ground Truth Cypher
```cypher
match (p1:Person)-[:IS_HUSBAND|IS_WIFE]->(p2:Person),
(p1)-[:LIVES_IN]->(loc1:Location),
(p2)-[:LIVES_IN]->(loc2:Location)
where loc1.name <> loc2.name
and p1.id < p2.id
return p1.firstName, p2.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_HUSBAND|IS_WIFE]->(p2:Person)
WHERE NOT (p1)-[:LIVES_IN]->()<-[:LIVES_IN]-(p2)
WITH p1, p2
MATCH (p1)-[:LIVES_IN]->(l1:Location), (p2)-[:LIVES_IN]->(l2:Location)
WHERE l1 <> l2
RETURN p1.firstName + ' ' + p1.lastName AS Partner1, 
       p2.firstName + ' ' + p2.lastName AS Partner2, 
       l1.name AS City1, 
       l2.name AS City2
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Kevin"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Mia",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Juan",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Johnny"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Jessica"
  }
]
```

**Actual Results:**
```json
[
  {
    "Partner1": "Mark Johnson",
    "Partner2": "Kevin Johnson",
    "City1": "Lake Justinview",
    "City2": "Lake Michelle"
  },
  {
    "Partner1": "Connie Lawrence",
    "Partner2": "Anna Davis",
    "City1": "Lake Justinview",
    "City2": "Lake Michelle"
  },
  {
    "Partner1": "Savannah Delacruz",
    "Partner2": "Juan Calderon",
    "City1": "Karenview",
    "City2": "North Robert"
  },
  {
    "Partner1": "Mia Sutton",
    "Partner2": "Michael Robinson",
    "City1": "Stephaniemouth",
    "City2": "Perryborough"
  },
  {
    "Partner1": "Johnny Campos",
    "Partner2": "Charles Taylor",
    "City1": "Stephaniemouth",
    "City2": "Simsview"
  },
  {
    "Partner1": "Jessica Chavez",
    "Partner2": "Joseph Maddox",
    "City1": "Simsview",
    "City2": "Lake Michelle"
  },
  {
    "Partner1": "Kevin Johnson",
    "Partner2": "Mark Johnson",
    "City1": "Lake Michelle",
    "City2": "Lake Justinview"
  },
  {
    "Partner1": "Anna Davis",
    "Partner2": "Connie Lawrence",
    "City1": "Lake Michelle",
    "City2": "Lake Justinview"
  },
  {
    "Partner1": "Juan Calderon",
    "Partner2": "Savannah Delacruz",
    "City1": "North Robert",
    "City2": "Karenview"
  },
  {
    "Partner1": "Michael Robinson",
    "Partner2": "Mia Sutton",
    "City1": "Perryborough",
    "City2": "Stephaniemouth"
  },
  {
    "Partner1": "Charles Taylor",
    "Partner2": "Johnny Campos",
    "City1": "Simsview",
    "City2": "Stephaniemouth"
  },
  {
    "Partner1": "Joseph Maddox",
    "Partner2": "Jessica Chavez",
    "City1": "Lake Michelle",
    "City2": "Simsview"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 775
- **Execution Time:** 3.84s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 64: 65
**Status:** PASS

#### Natural Language Query
```
Find all friend groups of 3.
```

#### Ground Truth Cypher
```cypher
match (p1:Person)-[:IS_FRIEND]->(p2:Person)-[:IS_FRIEND]->(p3:Person),
      (p3)-[:IS_FRIEND]->(p1)
where p1.id < p2.id
and p2.id < p3.id
return p1.firstName, p2.firstName, p3.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_FRIEND]->(p2:Person)-[:IS_FRIEND]->(p3:Person)-[:IS_FRIEND]->(p1)
WHERE id(p1) < id(p2) AND id(p2) < id(p3)
RETURN p1.firstName + ' ' + p1.lastName AS Person1,
       p2.firstName + ' ' + p2.lastName AS Person2,
       p3.firstName + ' ' + p3.lastName AS Person3
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Johnny",
    "p3.firstName": "William"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Joseph",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Joseph",
    "p3.firstName": "Tammy"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Joseph",
    "p3.firstName": "Joseph"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Jessica",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Jessica",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Jordan",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Vanessa",
    "p3.firstName": "Connie"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Vanessa",
    "p3.firstName": "Joseph"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "David",
    "p3.firstName": "April"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "David",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Annette",
    "p3.firstName": "Jared"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Annette",
    "p3.firstName": "Matthew"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Connie"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Steve"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Cheryl",
    "p3.firstName": "Tammy"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Thomas",
    "p3.firstName": "Anna"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Thomas",
    "p3.firstName": "Brandi"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Thomas",
    "p3.firstName": "Matthew"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Jared",
    "p3.firstName": "Connie"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Jared",
    "p3.firstName": "Angel"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Eugene",
    "p3.firstName": "Anna"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Timothy",
    "p3.firstName": "Debra"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Timothy",
    "p3.firstName": "April"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Connie",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Brandi",
    "p3.firstName": "Anna"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Brandi",
    "p3.firstName": "Scott"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Brandi",
    "p3.firstName": "Matthew"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "April",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "April",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "April",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "April",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Andrew",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Andrew",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Andrew",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Andrew",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "William",
    "p3.firstName": "Rachel"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Tammy",
    "p3.firstName": "Matthew"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Tammy",
    "p3.firstName": "Matthew"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Tammy",
    "p3.firstName": "Dana"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Tammy",
    "p3.firstName": "Dana"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Scott",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Scott",
    "p3.firstName": "Tammy"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Scott",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Scott",
    "p3.firstName": "Dana"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Scott",
    "p3.firstName": "Dana"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Scott",
    "p3.firstName": "Dana"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Anna",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Donald",
    "p3.firstName": "Eric"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Todd",
    "p3.firstName": "Rachel"
  },
  {
    "p1.firstName": "Todd",
    "p2.firstName": "Rachel",
    "p3.firstName": "Debra"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Rachel",
    "p3.firstName": "Angel"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Rachel",
    "p3.firstName": "Angel"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Eric",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Michael",
    "p3.firstName": "Mia"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Michael",
    "p3.firstName": "Debra"
  },
  {
    "p1.firstName": "Eric",
    "p2.firstName": "Michael",
    "p3.firstName": "Debra"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Christopher",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Christopher",
    "p3.firstName": "Juan"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Christopher",
    "p3.firstName": "Mia"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Christopher",
    "p3.firstName": "Mia"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Angel",
    "p3.firstName": "Debra"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Joseph",
    "p3.firstName": "Michael"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Joseph",
    "p3.firstName": "Debra"
  }
]
```

**Actual Results:**
```json
[
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Jessica Chavez"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Timothy Walls"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "Person3": "William Brady"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Vanessa Patel"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Jared David"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "April Wise"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey",
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Tammy Ryan"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 751
- **Execution Time:** 3.20s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 65: 66
**Status:** PASS

#### Natural Language Query
```
Look for all degrees held by people and count them per degree type.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[r:STUDIED]->(f:FieldOfStudy)
return r.degree, count(*);
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE s.degree IS NOT NULL
RETURN LOWER(s.degree) AS degree, COUNT(*) AS count
ORDER BY count DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "r.degree": "Bachelor",
    "count(*)": 32
  },
  {
    "r.degree": "PhD",
    "count(*)": 3
  },
  {
    "r.degree": "Master",
    "count(*)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "degree": "bachelor",
    "count": 32
  },
  {
    "degree": "phd",
    "count": 3
  },
  {
    "degree": "master",
    "count": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 729
- **Execution Time:** 2.55s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 66: 67
**Status:** PASS

#### Natural Language Query
```
Find people with double letter initials, like N.N.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where left(p.firstName, 1) = left(p.lastName, 1)
return p.firstName, p.lastName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE toLower(left(p.firstName, 1)) = toLower(left(p.lastName, 1))
AND size(p.firstName) > 1 AND size(p.lastName) > 1
RETURN p.firstName, p.lastName
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall"
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas"
  }
]
```

**Actual Results:**
```json
[
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall"
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 726
- **Execution Time:** 2.46s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 67: 68
**Status:** PASS

#### Natural Language Query
```
Find names that are both first names and last names in the database.
```

#### Ground Truth Cypher
```cypher
match (p1:Person), (p2:Person)
where p1.firstName = p2.lastName
return distinct p1.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person), (p2:Person)
WHERE toLower(p1.firstName) = toLower(p2.lastName)
RETURN DISTINCT p1.firstName AS name
ORDER BY name
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "David"
  }
]
```

**Actual Results:**
```json
[
  {
    "name": "David"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 723
- **Execution Time:** 2.75s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 68: 69
**Status:** PASS

#### Natural Language Query
```
Find people who are missing birthdates.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where p.birthDate is null
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE p.birthDate IS NULL
RETURN p.id, p.firstName, p.lastName
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 702
- **Execution Time:** 2.44s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 69: 70
**Status:** PASS

#### Natural Language Query
```
Which companies were founded in the same year?
```

#### Ground Truth Cypher
```cypher
match (c1:Company), (c2:Company)
where c1.foundedYear = c2.foundedYear
and c1.id < c2.id
return c1.name, c2.name;
```

#### Generated Cypher
```cypher
MATCH (c1:Company), (c2:Company)
WHERE c1.foundedYear = c2.foundedYear AND id(c1) < id(c2)
RETURN c1.name AS Company1, c2.name AS Company2, c1.foundedYear AS FoundedYear
ORDER BY c1.foundedYear
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 732
- **Execution Time:** 2.86s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 70: 71
**Status:** FAIL

#### Natural Language Query
```
Show me all universities founded before 1800.
```

#### Ground Truth Cypher
```cypher
match (e:EducationalInstitution)
where e.foundedYear < 1800
return e.name;
```

#### Generated Cypher
```cypher
MATCH (u:EducationalInstitution)
WHERE u.type = 'university' AND u.foundedYear < 1800
RETURN u.name, u.foundedYear, u.country
ORDER BY u.foundedYear
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "e.name": "Priceshire Institute"
  },
  {
    "e.name": "Port Nicoleshire Institute"
  },
  {
    "e.name": "Smithstad University"
  },
  {
    "e.name": "Castanedachester Institute"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 721
- **Execution Time:** 2.64s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 71: 72
**Status:** FAIL

#### Natural Language Query
```
Find people who share the same birthday.
```

#### Ground Truth Cypher
```cypher
match (p1:Person), (p2:Person)
where date(p1.birthDate).month = date(p2.birthDate).month
and date(p1.birthDate).day = date(p2.birthDate).day
and p1.id < p2.id
return p1.firstName, p2.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person), (p2:Person)
WHERE p1 <> p2 AND toLower(p1.birthDate) = toLower(p2.birthDate)
RETURN p1.firstName + ' ' + p1.lastName AS Person1, 
       p2.firstName + ' ' + p2.lastName AS Person2, 
       p1.birthDate AS SharedBirthday
ORDER BY SharedBirthday, Person1, Person2
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Joseph"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** easy
- **Tokens Used:** 753
- **Execution Time:** 3.03s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 72: 73
**Status:** PASS

#### Natural Language Query
```
List all job titles in the management category.
```

#### Ground Truth Cypher
```cypher
match (j:JobTitle)
where toLower(j.category) = 'management'
return j.title;
```

#### Generated Cypher
```cypher
MATCH (j:JobTitle)
WHERE toLower(j.category) = 'management'
RETURN j.title AS JobTitle
ORDER BY JobTitle
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "j.title": "CTO"
  }
]
```

**Actual Results:**
```json
[
  {
    "JobTitle": "CTO"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 710
- **Execution Time:** 2.04s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 73: 74
**Status:** PASS

#### Natural Language Query
```
What fields of study belong to the humanities category?
```

#### Ground Truth Cypher
```cypher
match (f:FieldOfStudy)
where toLower(f.category) = 'humanities'
return f.name;
```

#### Generated Cypher
```cypher
MATCH (f:FieldOfStudy)
WHERE toLower(f.category) = 'humanities'
RETURN f.name AS fieldOfStudy
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "f.name": "Medicine"
  },
  {
    "f.name": "Law"
  }
]
```

**Actual Results:**
```json
[
  {
    "fieldOfStudy": "Medicine"
  },
  {
    "fieldOfStudy": "Law"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 710
- **Execution Time:** 2.21s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 74: 75
**Status:** PASS

#### Natural Language Query
```
Find people whose email domain matches their company name.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[:WORKED_AT]-(c:Company)
where toLower(p.email) contains c.name
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:WORKED_AT]->(c:Company)
WHERE toLower(split(p.email, '@')[1]) CONTAINS toLower(c.name)
RETURN p.firstName, p.lastName, p.email, c.name
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** easy
- **Tokens Used:** 725
- **Execution Time:** 2.08s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 75: 76
**Status:** FAIL

#### Natural Language Query
```
Show me all cities with population over 1 million.
```

#### Ground Truth Cypher
```cypher
match (l:Location)
where toLower(l.type) = 'city'
and l.population > 1000000
return l.name;
```

#### Generated Cypher
```cypher
MATCH (l:Location)
WHERE l.type = 'city' AND l.population > 1000000
RETURN l.name AS City, l.population AS Population
ORDER BY l.population DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "l.name": "Stephaniemouth"
  },
  {
    "l.name": "Rivasside"
  },
  {
    "l.name": "Lake Michelle"
  },
  {
    "l.name": "Karenview"
  },
  {
    "l.name": "Simsview"
  },
  {
    "l.name": "Lake Justinview"
  },
  {
    "l.name": "Patricialand"
  },
  {
    "l.name": "East Patrick"
  },
  {
    "l.name": "Perryborough"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 721
- **Execution Time:** 1.84s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 76: 77
**Status:** FAIL

#### Natural Language Query
```
Who graduated from university in 2016?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[s:STUDIED_AT]-(e:EducationalInstitution)
where s.endYear = 2016
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE s.endYear = 2016 AND s.status = 'graduated'
RETURN p.firstName + ' ' + p.lastName AS graduate, e.name AS university
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Samuel"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 727
- **Execution Time:** 3.01s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 77: 78
**Status:** FAIL

#### Natural Language Query
```
Which married couples have the biggest age gap?
```

#### Ground Truth Cypher
```cypher
match (p1:Person)-[:IS_HUSBAND|IS_WIFE]-(p2:Person)
with p1, p2, duration.between(date(p2.birthDate), date(p1.birthDate)) as ageGap
return p1.firstName, p2.firstName
order by ageGap desc
limit 1;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_HUSBAND|IS_WIFE]->(p2:Person)
WHERE p1.birthDate IS NOT NULL AND p2.birthDate IS NOT NULL
WITH p1, p2, date(p1.birthDate) AS bd1, date(p2.birthDate) AS bd2
WITH p1, p2, duration.between(bd1, bd2).years AS ageDiff
RETURN p1.firstName + ' ' + p1.lastName AS Person1, 
       p2.firstName + ' ' + p2.lastName AS Person2, 
       abs(ageDiff) AS AgeDifference
ORDER BY AgeDifference DESC
LIMIT 10
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Mia"
  }
]
```

**Actual Results:**
```json
[
  {
    "Person1": "Michael Robinson",
    "Person2": "Mia Sutton",
    "AgeDifference": 28
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Michael Robinson",
    "AgeDifference": 28
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz",
    "AgeDifference": 13
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Juan Calderon",
    "AgeDifference": 13
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Joseph Maddox",
    "AgeDifference": 12
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Jessica Chavez",
    "AgeDifference": 12
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "AgeDifference": 9
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Charles Taylor",
    "AgeDifference": 9
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Connie Lawrence",
    "AgeDifference": 2
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Anna Davis",
    "AgeDifference": 2
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 788
- **Execution Time:** 3.52s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 78: 79
**Status:** FAIL

#### Natural Language Query
```
Show me people who studied longer than 4 years at university.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[s:STUDIED_AT]-(e:EducationalInstitution)
where s.endYear - s.startYear > 4
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE e.type = 'university' AND s.endYear - s.startYear > 4
RETURN p.firstName + ' ' + p.lastName AS name, e.name AS university, s.startYear AS startYear, s.endYear AS endYear, s.endYear - s.startYear AS yearsStudied
ORDER BY yearsStudied DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Scott"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Cheryl"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 764
- **Execution Time:** 2.97s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 79: 80
**Status:** FAIL

#### Natural Language Query
```
Find friends who work in competing companies in the same industry.
```

#### Ground Truth Cypher
```cypher
match (p1:Person)-[w1:WORKED_AT]-(c1:Company),
      (p2:Person)-[w2:WORKED_AT]-(c2:Company)
where p1.id < p2.id
and c1.id <> c2.id
and c1.industry = c2.industry
and w1.endYear is null
and w2.endYear is null
return p1.firstName, p2.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_FRIEND]->(p2:Person)
WHERE p1 <> p2
MATCH (p1)-[w1:WORKED_AT]->(c1:Company)
MATCH (p2)-[w2:WORKED_AT]->(c2:Company)
WHERE c1 <> c2 AND c1.industry = c2.industry
  AND w1.status = 'CURRENT' AND w2.status = 'CURRENT'
RETURN p1.firstName + ' ' + p1.lastName AS Person1,
       p2.firstName + ' ' + p2.lastName AS Person2,
       c1.name AS Company1,
       c2.name AS Company2,
       c1.industry AS Industry
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Todd",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Vanessa"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Vanessa"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Annette"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Annette"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Annette"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Donald",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Donald",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Tanya"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Tracey"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Angel",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Juan",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Stephanie"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Stephanie"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Angel",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Juan",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Nathaniel"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Jeffrey"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Steve"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Scott"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Todd"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Eric",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Timothy"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Timothy"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Timothy"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Donald",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Angel",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Eugene"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Eugene"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Eugene"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Eugene"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Donald",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Christopher"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 796
- **Execution Time:** 4.21s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 80: 81
**Status:** FAIL

#### Natural Language Query
```
Find people who started working before finishing their studies.
```

#### Ground Truth Cypher
```cypher
match (e:EducationalInstitution)-[s:STUDIED_AT]-(p:Person)-[w:WORKED_AT]-(c:Company)
where w.startYear < s.endYear
return p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution), (p)-[w:WORKED_AT]->(c:Company)
WHERE w.startYear < s.endYear
RETURN DISTINCT p.firstName + ' ' + p.lastName AS name, e.name AS institution, c.name AS company, s.startYear AS studyStartYear, s.endYear AS studyEndYear, w.startYear AS workStartYear
ORDER BY p.lastName, p.firstName
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: In a WITH/RETURN with DISTINCT or an aggregation, it is not possible to access variables declared before the WITH/RETURN: p (line 4, column 10 (offset: 316))
"ORDER BY p.lastName, p.firstName"
          ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Charles"
  },
  {
    "p.firstName": "Annette"
  },
  {
    "p.firstName": "Samuel"
  },
  {
    "p.firstName": "William"
  },
  {
    "p.firstName": "Scott"
  },
  {
    "p.firstName": "Tammy"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Debra"
  },
  {
    "p.firstName": "Johnny"
  },
  {
    "p.firstName": "Johnny"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Tracey"
  },
  {
    "p.firstName": "Cheryl"
  },
  {
    "p.firstName": "Cheryl"
  },
  {
    "p.firstName": "Cheryl"
  },
  {
    "p.firstName": "Timothy"
  },
  {
    "p.firstName": "Donald"
  },
  {
    "p.firstName": "Donald"
  },
  {
    "p.firstName": "Eric"
  },
  {
    "p.firstName": "Connie"
  },
  {
    "p.firstName": "David"
  },
  {
    "p.firstName": "Christopher"
  },
  {
    "p.firstName": "Dana"
  },
  {
    "p.firstName": "Mia"
  },
  {
    "p.firstName": "Thomas"
  },
  {
    "p.firstName": "Theresa"
  },
  {
    "p.firstName": "Tammy"
  },
  {
    "p.firstName": "Todd"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 773
- **Execution Time:** 2.87s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 81: 82
**Status:** PASS

#### Natural Language Query
```
Which field of study has the shortest average study duration?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[s:STUDIED]-(f:FieldOfStudy)
where s.endYear is not null
with f, avg(s.endYear - s.startYear) as studyDuration
return f.name
order by studyDuration
limit 1;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s:STUDIED]->(f:FieldOfStudy)
WITH f, AVG(s.endYear - s.startYear) AS avgDuration
RETURN f.name AS FieldOfStudy, avgDuration
ORDER BY avgDuration ASC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "f.name": "Law"
  }
]
```

**Actual Results:**
```json
[
  {
    "FieldOfStudy": "Law",
    "avgDuration": 3.888888888888889
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 731
- **Execution Time:** 2.31s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 82: 83
**Status:** FAIL

#### Natural Language Query
```
Show me parent-child pairs who work in the same company.
```

#### Ground Truth Cypher
```cypher
match (c:Company)-[w1:WORKED_AT]-(child:Person)-[:IS_CHILD]->(parent:Person)-[w2:WORKED_AT]-(c)
where w1.endYear is null
and w2.endYear is null
return child.firstName, parent.firstName;
```

#### Generated Cypher
```cypher
MATCH (parent:Person)-[:IS_PARENT]->(child:Person)
WHERE EXISTS((parent)-[:WORKED_AT]->(company:Company)<-[:WORKED_AT]-(child))
RETURN parent.firstName + ' ' + parent.lastName AS Parent, 
       child.firstName + ' ' + child.lastName AS Child, 
       company.name AS Company
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'company'. (line 2, column 38 (offset: 88))
"WHERE EXISTS((parent)-[:WORKED_AT]->(company:Company)<-[:WORKED_AT]-(child))"
                                      ^}
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "child.firstName": "Connie",
    "parent.firstName": "Kevin"
  },
  {
    "child.firstName": "Charles",
    "parent.firstName": "Mark"
  }
]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 755
- **Execution Time:** 2.39s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 83: 84
**Status:** PASS

#### Natural Language Query
```
Find family dynasties where multiple generations attended the same university.
```

#### Ground Truth Cypher
```cypher
match path = (p1:Person)-[:IS_CHILD*1..5]->(p2:Person),
      (p1)-[:STUDIED_AT]->(u:EducationalInstitution),
      (p2)-[:STUDIED_AT]->(u)
with collect(distinct p1) + collect(distinct p2) as family
return [p in family | p.firstName];
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_PARENT*1..3]->(p2:Person)
WHERE p1 <> p2
WITH p1, p2
MATCH (p1)-[:STUDIED_AT]->(uni:EducationalInstitution)<-[:STUDIED_AT]-(p2)
WITH DISTINCT p1, p2, uni
MATCH path = (p1)-[:IS_PARENT*1..3]->(p2)
WITH p1, p2, uni, [node IN nodes(path) | node.firstName + ' ' + node.lastName] AS familyMembers
RETURN DISTINCT uni.name AS University, familyMembers AS FamilyDynasty
ORDER BY University, size(familyMembers) DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "[p in family | p.firstName]": [
      "Mia",
      "Kevin"
    ]
  }
]
```

**Actual Results:**
```json
[
  {
    "University": "South Jeffrey Institute",
    "FamilyDynasty": [
      "Kevin Johnson",
      "Mia Sutton"
    ]
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 800
- **Execution Time:** 9.04s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 84: 85
**Status:** PASS

#### Natural Language Query
```
Detect circular migration patterns where people return to their birth country after living abroad.
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[l1:LIVED_IN]->(loc1:Location)
with p, loc1
order by p, l1.startYear
with p, collect(loc1)[0] as origin
match (p)-[l2:LIVED_IN]->(loc2:Location)
where loc2.country <> origin.country
with p, origin, max(l2.startYear) as abroadYear
match (p)-[l3:LIVES_IN]->(loc3:Location)
where l3.startYear > abroadYear and loc3.country = origin.country
return distinct p.firstName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[:LIVED_IN]->(l:Location)
WHERE l.country <> toLower(p.birthPlace)
WITH p, l
MATCH (p)-[:LIVES_IN]->(current:Location)
WHERE toLower(current.country) = toLower(p.birthPlace) AND current.country <> l.country
RETURN p.firstName + ' ' + p.lastName AS name, 
       p.birthPlace AS birthCountry, 
       l.country AS livedCountry, 
       current.country AS currentCountry
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 793
- **Execution Time:** 3.44s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 85: 86
**Status:** FAIL

#### Natural Language Query
```
Find anomalies in educational timelines where people studied multiple degrees simultaneously.
```

#### Ground Truth Cypher
```cypher
match (f1:FieldOfStudy)-[s1:STUDIED]-(p:Person)-[s2:STUDIED]-(f2:FieldOfStudy)
where s1.startYear > s2.startYear
and s1.startYear < s2.endYear
return p.firstName, s1.degree, s2.degree;
```

#### Generated Cypher
```cypher
MATCH (p:Person)-[s1:STUDIED_AT]->(e1:EducationalInstitution)
WITH p, s1, e1
MATCH (p)-[s2:STUDIED_AT]->(e2:EducationalInstitution)
WHERE id(e1) < id(e2) 
  AND ((s1.startYear <= s2.startYear AND s1.endYear >= s2.startYear)
    OR (s2.startYear <= s1.startYear AND s2.endYear >= s1.startYear))
RETURN p.firstName + ' ' + p.lastName AS PersonName,
       e1.name AS Institution1, s1.degree AS Degree1, s1.startYear AS Start1, s1.endYear AS End1,
       e2.name AS Institution2, s2.degree AS Degree2, s2.startYear AS Start2, s2.endYear AS End2
ORDER BY PersonName, Start1, Start2
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Mia",
    "s1.degree": "Bachelor",
    "s2.degree": "Bachelor"
  },
  {
    "p.firstName": "Cheryl",
    "s1.degree": "PhD",
    "s2.degree": "Bachelor"
  },
  {
    "p.firstName": "Dana",
    "s1.degree": "PhD",
    "s2.degree": "Bachelor"
  }
]
```

**Actual Results:**
```json
[
  {
    "PersonName": "Dana Douglas",
    "Institution1": "Priceshire Institute",
    "Degree1": "PhD",
    "Start1": 2014,
    "End1": 2019,
    "Institution2": "Castanedachester Institute",
    "Degree2": "Bachelor",
    "Start2": 2011,
    "End2": 2015
  },
  {
    "PersonName": "Dana Douglas",
    "Institution1": "Priceshire Institute",
    "Degree1": "PhD",
    "Start1": 2014,
    "End1": 2019,
    "Institution2": "Port Nicoleshire Institute",
    "Degree2": "Master",
    "Start2": 2019,
    "End2": 2021
  },
  {
    "PersonName": "Mia Sutton",
    "Institution1": "Castanedachester Institute",
    "Degree1": "Bachelor",
    "Start1": 1991,
    "End1": 1995,
    "Institution2": "South Jeffrey Institute",
    "Degree2": "Bachelor",
    "Start2": 1993,
    "End2": 1997
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 840
- **Execution Time:** 4.92s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 86: 87
**Status:** FAIL

#### Natural Language Query
```
Find people who never changed their location.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where not exists {(p)-[:LIVED_IN]-(l:Location)}
return p.firstName;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Node is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 0
- **Execution Time:** 2.40s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 87: 88
**Status:** PASS

#### Natural Language Query
```
Which company has the smallest number of employees?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[w:WORKED_AT]-(c:Company)
where w.endYear is null
with c, count(distinct p) as workers
order by workers
return c.name
limit 1;
```

#### Generated Cypher
```cypher
MATCH (c:Company)
WHERE c.employees IS NOT NULL
RETURN c.name AS CompanyName, c.employees AS EmployeeCount
ORDER BY c.employees ASC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "c.name": "Hooper PLC"
  }
]
```

**Actual Results:**
```json
[
  {
    "CompanyName": "Ruiz Ltd",
    "EmployeeCount": 92460
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 720
- **Execution Time:** 2.52s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 88: 89
**Status:** PASS

#### Natural Language Query
```
Show me all people with Gmail email addresses.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where toLower(p.email) contains 'gmail'
return p.firstName, p.email;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE p.email CONTAINS '@gmail.com'
RETURN p
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 699
- **Execution Time:** 1.65s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 89: 90
**Status:** FAIL

#### Natural Language Query
```
Find all educational institutions of type 'College'.
```

#### Ground Truth Cypher
```cypher
match (e:EducationalInstitution)
where toLower(e.type) = 'college'
return e.name;
```

#### Generated Cypher
```cypher
None
```

#### Error Analysis
```
Error in test case execution: Object of type Node is not JSON serializable
```

#### Results Comparison

**Expected Results:**
```json
null
```

**Actual Results:**
```json
null
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 0
- **Execution Time:** 2.42s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 90: 91
**Status:** FAIL

#### Natural Language Query
```
List people who are currently unemployed.
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where not exists {(p)-[w:WORKED_AT]-(c:Company)
                   where w.endYear is null}
return p.firstName, p.lastName;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE NOT EXISTS((p)-[:WORKED_AT]->(:Company {status: 'current'}))
  AND NOT EXISTS((p)-[:HAD_POSITION]->(:JobTitle {status: 'current'}))
RETURN p.firstName + ' ' + p.lastName AS unemployedPerson
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Michael",
    "p.lastName": "Robinson"
  },
  {
    "p.firstName": "Jared",
    "p.lastName": "David"
  },
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey"
  }
]
```

**Actual Results:**
```json
[
  {
    "unemployedPerson": "Mark Johnson"
  },
  {
    "unemployedPerson": "Kevin Johnson"
  },
  {
    "unemployedPerson": "Connie Lawrence"
  },
  {
    "unemployedPerson": "Anna Davis"
  },
  {
    "unemployedPerson": "Juan Calderon"
  },
  {
    "unemployedPerson": "Savannah Delacruz"
  },
  {
    "unemployedPerson": "Mia Sutton"
  },
  {
    "unemployedPerson": "Michael Robinson"
  },
  {
    "unemployedPerson": "Debra Clark"
  },
  {
    "unemployedPerson": "Charles Taylor"
  },
  {
    "unemployedPerson": "Johnny Campos"
  },
  {
    "unemployedPerson": "Joseph Maddox"
  },
  {
    "unemployedPerson": "Jessica Chavez"
  },
  {
    "unemployedPerson": "Jordan Gonzalez"
  },
  {
    "unemployedPerson": "Tanya Koch"
  },
  {
    "unemployedPerson": "Vanessa Patel"
  },
  {
    "unemployedPerson": "Tracey Hickman"
  },
  {
    "unemployedPerson": "David Brown"
  },
  {
    "unemployedPerson": "Crystal Whitehead"
  },
  {
    "unemployedPerson": "Nathaniel Khan"
  },
  {
    "unemployedPerson": "Jeffrey Henderson"
  },
  {
    "unemployedPerson": "David Lee"
  },
  {
    "unemployedPerson": "Annette Pearson"
  },
  {
    "unemployedPerson": "Stephanie Martin"
  },
  {
    "unemployedPerson": "Cheryl Robinson"
  },
  {
    "unemployedPerson": "Thomas Schmidt"
  },
  {
    "unemployedPerson": "Jared David"
  },
  {
    "unemployedPerson": "Eugene Green"
  },
  {
    "unemployedPerson": "Timothy Walls"
  },
  {
    "unemployedPerson": "Brandi Bailey"
  },
  {
    "unemployedPerson": "Logan Archer"
  },
  {
    "unemployedPerson": "Steve Newton"
  },
  {
    "unemployedPerson": "Samuel Wagner"
  },
  {
    "unemployedPerson": "April Wise"
  },
  {
    "unemployedPerson": "Theresa Vazquez"
  },
  {
    "unemployedPerson": "Andrew Diaz"
  },
  {
    "unemployedPerson": "William Brady"
  },
  {
    "unemployedPerson": "Tammy Patton"
  },
  {
    "unemployedPerson": "Scott Walker"
  },
  {
    "unemployedPerson": "Donald Jones"
  },
  {
    "unemployedPerson": "Todd Wilson"
  },
  {
    "unemployedPerson": "Rachel Graham"
  },
  {
    "unemployedPerson": "Tammy Ryan"
  },
  {
    "unemployedPerson": "Eric Ortiz"
  },
  {
    "unemployedPerson": "Michael Orr"
  },
  {
    "unemployedPerson": "Matthew Marshall"
  },
  {
    "unemployedPerson": "Christopher Miller"
  },
  {
    "unemployedPerson": "Angel Riggs"
  },
  {
    "unemployedPerson": "Dana Douglas"
  },
  {
    "unemployedPerson": "Joseph Williams"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 736
- **Execution Time:** 2.63s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 91: 92
**Status:** FAIL

#### Natural Language Query
```
Which field of study has the most students enrolled?
```

#### Ground Truth Cypher
```cypher
match (p:Person)-[s:STUDIED]-(f:FieldOfStudy)
where s.endYear is null
with f, count(p) as enrolled
order by enrolled desc
return f.name
limit 1;
```

#### Generated Cypher
```cypher
MATCH (f:FieldOfStudy)<-[:STUDIED]-(p:Person)
WITH f, COUNT(DISTINCT p) AS studentCount
RETURN f.name AS fieldOfStudy, studentCount
ORDER BY studentCount DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "f.name": "Business Administration"
  }
]
```

**Actual Results:**
```json
[
  {
    "fieldOfStudy": "Law",
    "studentCount": 9
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 727
- **Execution Time:** 3.01s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 92: 93
**Status:** FAIL

#### Natural Language Query
```
Find people born in the same decade.
```

#### Ground Truth Cypher
```cypher
match (p1:Person), (p2:Person)
where p1.id < p2.id
and toInteger(date(p1.birthDate).year / 10) = toInteger(date(p2.birthDate).year / 10)
return p1.firstName, p2.firstName, p1.birthDate, p2.birthDate;
```

#### Generated Cypher
```cypher
MATCH (p1:Person), (p2:Person)
WHERE p1 <> p2
  AND toInteger(left(p1.birthDate, 3) + '0') = toInteger(left(p2.birthDate, 3) + '0')
RETURN p1.firstName + ' ' + p1.lastName AS Person1,
       p2.firstName + ' ' + p2.lastName AS Person2,
       toInteger(left(p1.birthDate, 3) + '0') AS Decade
ORDER BY Decade, Person1, Person2
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Kevin",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1929-11-07"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Kevin",
    "p1.birthDate": "1927-12-04",
    "p2.birthDate": "1929-11-07"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Kevin",
    "p1.birthDate": "1927-11-20",
    "p2.birthDate": "1929-11-07"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Connie",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1929-01-23"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Connie",
    "p1.birthDate": "1927-12-04",
    "p2.birthDate": "1929-01-23"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Connie",
    "p1.birthDate": "1927-11-20",
    "p2.birthDate": "1929-01-23"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Connie",
    "p1.birthDate": "1929-11-07",
    "p2.birthDate": "1929-01-23"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Connie",
    "p1.birthDate": "1926-04-29",
    "p2.birthDate": "1929-01-23"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Anna",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Anna",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Anna",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Anna",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Anna",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Anna",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1931-09-23"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Juan",
    "p1.birthDate": "1943-03-10",
    "p2.birthDate": "1948-05-13"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Juan",
    "p1.birthDate": "1949-04-30",
    "p2.birthDate": "1948-05-13"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Juan",
    "p1.birthDate": "1945-06-15",
    "p2.birthDate": "1948-05-13"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Juan",
    "p1.birthDate": "1945-06-20",
    "p2.birthDate": "1948-05-13"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1931-09-23",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1932-12-20",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1930-11-03",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1930-12-01",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Angel",
    "p2.firstName": "Savannah",
    "p1.birthDate": "1932-02-17",
    "p2.birthDate": "1935-02-12"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Mia",
    "p1.birthDate": "1976-07-18",
    "p2.birthDate": "1972-02-14"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Mia",
    "p1.birthDate": "1979-06-01",
    "p2.birthDate": "1972-02-14"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Michael",
    "p1.birthDate": "2005-07-04",
    "p2.birthDate": "2000-03-19"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Michael",
    "p1.birthDate": "2001-12-06",
    "p2.birthDate": "2000-03-19"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Michael",
    "p1.birthDate": "2000-07-21",
    "p2.birthDate": "2000-03-19"
  },
  {
    "p1.firstName": "Todd",
    "p2.firstName": "Debra",
    "p1.birthDate": "1987-01-29",
    "p2.birthDate": "1982-07-31"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Jordan",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1927-12-04"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Vanessa",
    "p1.birthDate": "1964-04-28",
    "p2.birthDate": "1969-12-03"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Tracey",
    "p1.birthDate": "1992-10-03",
    "p2.birthDate": "1991-06-25"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "David",
    "p1.birthDate": "1951-11-13",
    "p2.birthDate": "1957-03-25"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Crystal",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1927-11-20"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Crystal",
    "p1.birthDate": "1927-12-04",
    "p2.birthDate": "1927-11-20"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Nathaniel",
    "p1.birthDate": "1964-04-28",
    "p2.birthDate": "1967-04-08"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Nathaniel",
    "p1.birthDate": "1969-12-03",
    "p2.birthDate": "1967-04-08"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Jeffrey",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1935-09-02"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "David",
    "p1.birthDate": "1943-03-10",
    "p2.birthDate": "1949-04-30"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Stephanie",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1934-09-13"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Stephanie",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1934-09-13"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Cheryl",
    "p1.birthDate": "1951-11-13",
    "p2.birthDate": "1951-09-03"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Cheryl",
    "p1.birthDate": "1957-03-25",
    "p2.birthDate": "1951-09-03"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Thomas",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1926-04-29"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Thomas",
    "p1.birthDate": "1927-12-04",
    "p2.birthDate": "1926-04-29"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Thomas",
    "p1.birthDate": "1927-11-20",
    "p2.birthDate": "1926-04-29"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Thomas",
    "p1.birthDate": "1929-11-07",
    "p2.birthDate": "1926-04-29"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Eugene",
    "p1.birthDate": "2005-07-04",
    "p2.birthDate": "2001-12-06"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Timothy",
    "p1.birthDate": "1964-04-28",
    "p2.birthDate": "1961-10-25"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Timothy",
    "p1.birthDate": "1969-12-03",
    "p2.birthDate": "1961-10-25"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Timothy",
    "p1.birthDate": "1967-04-08",
    "p2.birthDate": "1961-10-25"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Brandi",
    "p1.birthDate": "2005-07-04",
    "p2.birthDate": "2000-07-21"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Brandi",
    "p1.birthDate": "2001-12-06",
    "p2.birthDate": "2000-07-21"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Logan",
    "p1.birthDate": "1943-03-10",
    "p2.birthDate": "1945-06-15"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Logan",
    "p1.birthDate": "1949-04-30",
    "p2.birthDate": "1945-06-15"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Steve",
    "p1.birthDate": "1992-10-03",
    "p2.birthDate": "1999-02-19"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Steve",
    "p1.birthDate": "1991-06-25",
    "p2.birthDate": "1999-02-19"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Samuel",
    "p1.birthDate": "1992-10-03",
    "p2.birthDate": "1994-01-03"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Samuel",
    "p1.birthDate": "1991-06-25",
    "p2.birthDate": "1994-01-03"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Samuel",
    "p1.birthDate": "1999-02-19",
    "p2.birthDate": "1994-01-03"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "April",
    "p1.birthDate": "1992-10-03",
    "p2.birthDate": "1995-10-25"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "April",
    "p1.birthDate": "1991-06-25",
    "p2.birthDate": "1995-10-25"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "April",
    "p1.birthDate": "1999-02-19",
    "p2.birthDate": "1995-10-25"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "April",
    "p1.birthDate": "1994-01-03",
    "p2.birthDate": "1995-10-25"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Theresa",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1933-03-03"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Theresa",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1933-03-03"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Theresa",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1933-03-03"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1928-06-16",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1927-12-04",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1927-11-20",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1929-11-07",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1926-04-29",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Andrew",
    "p1.birthDate": "1929-01-23",
    "p2.birthDate": "1926-01-22"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "William",
    "p1.birthDate": "1964-04-28",
    "p2.birthDate": "1961-11-17"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "William",
    "p1.birthDate": "1969-12-03",
    "p2.birthDate": "1961-11-17"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "William",
    "p1.birthDate": "1967-04-08",
    "p2.birthDate": "1961-11-17"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "William",
    "p1.birthDate": "1961-10-25",
    "p2.birthDate": "1961-11-17"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Tammy",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1933-08-17"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Tammy",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1933-08-17"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Tammy",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1933-08-17"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Tammy",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1933-08-17"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Scott",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1937-05-09"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Scott",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1937-05-09"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Scott",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1937-05-09"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Scott",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1937-05-09"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Scott",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1937-05-09"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Donald",
    "p1.birthDate": "1964-04-28",
    "p2.birthDate": "1968-05-05"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Donald",
    "p1.birthDate": "1969-12-03",
    "p2.birthDate": "1968-05-05"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Donald",
    "p1.birthDate": "1967-04-08",
    "p2.birthDate": "1968-05-05"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "Donald",
    "p1.birthDate": "1961-10-25",
    "p2.birthDate": "1968-05-05"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Donald",
    "p1.birthDate": "1961-11-17",
    "p2.birthDate": "1968-05-05"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Rachel",
    "p1.birthDate": "1931-09-23",
    "p2.birthDate": "1932-12-20"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Tammy",
    "p1.birthDate": "1976-07-18",
    "p2.birthDate": "1979-06-01"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Eric",
    "p1.birthDate": "1951-11-13",
    "p2.birthDate": "1956-04-25"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Eric",
    "p1.birthDate": "1957-03-25",
    "p2.birthDate": "1956-04-25"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Eric",
    "p1.birthDate": "1951-09-03",
    "p2.birthDate": "1956-04-25"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Michael",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Michael",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Michael",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Michael",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Michael",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Michael",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Michael",
    "p1.birthDate": "1931-09-23",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Michael",
    "p1.birthDate": "1932-12-20",
    "p2.birthDate": "1930-11-03"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Matthew",
    "p1.birthDate": "1943-03-10",
    "p2.birthDate": "1945-06-20"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Matthew",
    "p1.birthDate": "1949-04-30",
    "p2.birthDate": "1945-06-20"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Matthew",
    "p1.birthDate": "1945-06-15",
    "p2.birthDate": "1945-06-20"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1931-09-23",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1932-12-20",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Christopher",
    "p1.birthDate": "1930-11-03",
    "p2.birthDate": "1930-12-01"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Angel",
    "p1.birthDate": "1934-01-16",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Angel",
    "p1.birthDate": "1935-09-02",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Angel",
    "p1.birthDate": "1934-09-13",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Angel",
    "p1.birthDate": "1933-03-03",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Angel",
    "p1.birthDate": "1933-08-17",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Angel",
    "p1.birthDate": "1937-05-09",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Angel",
    "p1.birthDate": "1931-09-23",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Angel",
    "p1.birthDate": "1932-12-20",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Angel",
    "p1.birthDate": "1930-11-03",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Angel",
    "p1.birthDate": "1930-12-01",
    "p2.birthDate": "1932-02-17"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Dana",
    "p1.birthDate": "1992-10-03",
    "p2.birthDate": "1993-07-14"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Dana",
    "p1.birthDate": "1991-06-25",
    "p2.birthDate": "1993-07-14"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Dana",
    "p1.birthDate": "1999-02-19",
    "p2.birthDate": "1993-07-14"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Dana",
    "p1.birthDate": "1994-01-03",
    "p2.birthDate": "1993-07-14"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Dana",
    "p1.birthDate": "1995-10-25",
    "p2.birthDate": "1993-07-14"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Joseph",
    "p1.birthDate": "1943-03-10",
    "p2.birthDate": "1942-12-06"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Joseph",
    "p1.birthDate": "1949-04-30",
    "p2.birthDate": "1942-12-06"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Joseph",
    "p1.birthDate": "1945-06-15",
    "p2.birthDate": "1942-12-06"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Joseph",
    "p1.birthDate": "1945-06-20",
    "p2.birthDate": "1942-12-06"
  },
  {
    "p1.firstName": "Juan",
    "p2.firstName": "Joseph",
    "p1.birthDate": "1948-05-13",
    "p2.birthDate": "1942-12-06"
  }
]
```

**Actual Results:**
```json
[
  {
    "Person1": "Andrew Diaz",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Andrew Diaz",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Connie Lawrence",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Crystal Whitehead",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Jordan Gonzalez",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Kevin Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Mark Johnson",
    "Decade": 1920
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Theresa Vazquez",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Angel Riggs",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Anna Davis",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Charles Taylor",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Christopher Miller",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Jeffrey Henderson",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Michael Orr",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Rachel Graham",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Savannah Delacruz",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Scott Walker",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Stephanie Martin",
    "Decade": 1930
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Tammy Patton",
    "Decade": 1930
  },
  {
    "Person1": "David Lee",
    "Person2": "Johnny Campos",
    "Decade": 1940
  },
  {
    "Person1": "David Lee",
    "Person2": "Joseph Williams",
    "Decade": 1940
  },
  {
    "Person1": "David Lee",
    "Person2": "Juan Calderon",
    "Decade": 1940
  },
  {
    "Person1": "David Lee",
    "Person2": "Logan Archer",
    "Decade": 1940
  },
  {
    "Person1": "David Lee",
    "Person2": "Matthew Marshall",
    "Decade": 1940
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "David Lee",
    "Decade": 1940
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Williams",
    "Decade": 1940
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Juan Calderon",
    "Decade": 1940
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Logan Archer",
    "Decade": 1940
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Matthew Marshall",
    "Decade": 1940
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "David Lee",
    "Decade": 1940
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Johnny Campos",
    "Decade": 1940
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Juan Calderon",
    "Decade": 1940
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Logan Archer",
    "Decade": 1940
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Matthew Marshall",
    "Decade": 1940
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "David Lee",
    "Decade": 1940
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Decade": 1940
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Williams",
    "Decade": 1940
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Logan Archer",
    "Decade": 1940
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Matthew Marshall",
    "Decade": 1940
  },
  {
    "Person1": "Logan Archer",
    "Person2": "David Lee",
    "Decade": 1940
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Johnny Campos",
    "Decade": 1940
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Joseph Williams",
    "Decade": 1940
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Juan Calderon",
    "Decade": 1940
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Matthew Marshall",
    "Decade": 1940
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "David Lee",
    "Decade": 1940
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Johnny Campos",
    "Decade": 1940
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Joseph Williams",
    "Decade": 1940
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Juan Calderon",
    "Decade": 1940
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Logan Archer",
    "Decade": 1940
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "David Brown",
    "Decade": 1950
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Eric Ortiz",
    "Decade": 1950
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Jessica Chavez",
    "Decade": 1950
  },
  {
    "Person1": "David Brown",
    "Person2": "Cheryl Robinson",
    "Decade": 1950
  },
  {
    "Person1": "David Brown",
    "Person2": "Eric Ortiz",
    "Decade": 1950
  },
  {
    "Person1": "David Brown",
    "Person2": "Jessica Chavez",
    "Decade": 1950
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Cheryl Robinson",
    "Decade": 1950
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "David Brown",
    "Decade": 1950
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Jessica Chavez",
    "Decade": 1950
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Cheryl Robinson",
    "Decade": 1950
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Brown",
    "Decade": 1950
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Decade": 1950
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Joseph Maddox",
    "Decade": 1960
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Nathaniel Khan",
    "Decade": 1960
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Timothy Walls",
    "Decade": 1960
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Vanessa Patel",
    "Decade": 1960
  },
  {
    "Person1": "Donald Jones",
    "Person2": "William Brady",
    "Decade": 1960
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Donald Jones",
    "Decade": 1960
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Nathaniel Khan",
    "Decade": 1960
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Timothy Walls",
    "Decade": 1960
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Decade": 1960
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "William Brady",
    "Decade": 1960
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Donald Jones",
    "Decade": 1960
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Joseph Maddox",
    "Decade": 1960
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Timothy Walls",
    "Decade": 1960
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Vanessa Patel",
    "Decade": 1960
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "William Brady",
    "Decade": 1960
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Donald Jones",
    "Decade": 1960
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Joseph Maddox",
    "Decade": 1960
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Nathaniel Khan",
    "Decade": 1960
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Vanessa Patel",
    "Decade": 1960
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "William Brady",
    "Decade": 1960
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Donald Jones",
    "Decade": 1960
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Maddox",
    "Decade": 1960
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Nathaniel Khan",
    "Decade": 1960
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Timothy Walls",
    "Decade": 1960
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "William Brady",
    "Decade": 1960
  },
  {
    "Person1": "William Brady",
    "Person2": "Donald Jones",
    "Decade": 1960
  },
  {
    "Person1": "William Brady",
    "Person2": "Joseph Maddox",
    "Decade": 1960
  },
  {
    "Person1": "William Brady",
    "Person2": "Nathaniel Khan",
    "Decade": 1960
  },
  {
    "Person1": "William Brady",
    "Person2": "Timothy Walls",
    "Decade": 1960
  },
  {
    "Person1": "William Brady",
    "Person2": "Vanessa Patel",
    "Decade": 1960
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Mia Sutton",
    "Decade": 1970
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Tammy Ryan",
    "Decade": 1970
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Annette Pearson",
    "Decade": 1970
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Tammy Ryan",
    "Decade": 1970
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "Annette Pearson",
    "Decade": 1970
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "Mia Sutton",
    "Decade": 1970
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson",
    "Decade": 1980
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Debra Clark",
    "Decade": 1980
  },
  {
    "Person1": "April Wise",
    "Person2": "Dana Douglas",
    "Decade": 1990
  },
  {
    "Person1": "April Wise",
    "Person2": "Samuel Wagner",
    "Decade": 1990
  },
  {
    "Person1": "April Wise",
    "Person2": "Steve Newton",
    "Decade": 1990
  },
  {
    "Person1": "April Wise",
    "Person2": "Tanya Koch",
    "Decade": 1990
  },
  {
    "Person1": "April Wise",
    "Person2": "Tracey Hickman",
    "Decade": 1990
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "April Wise",
    "Decade": 1990
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Samuel Wagner",
    "Decade": 1990
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Steve Newton",
    "Decade": 1990
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Tanya Koch",
    "Decade": 1990
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Tracey Hickman",
    "Decade": 1990
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "April Wise",
    "Decade": 1990
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Dana Douglas",
    "Decade": 1990
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Steve Newton",
    "Decade": 1990
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Tanya Koch",
    "Decade": 1990
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Tracey Hickman",
    "Decade": 1990
  },
  {
    "Person1": "Steve Newton",
    "Person2": "April Wise",
    "Decade": 1990
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Dana Douglas",
    "Decade": 1990
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Samuel Wagner",
    "Decade": 1990
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Tanya Koch",
    "Decade": 1990
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Tracey Hickman",
    "Decade": 1990
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "April Wise",
    "Decade": 1990
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Dana Douglas",
    "Decade": 1990
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Samuel Wagner",
    "Decade": 1990
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Steve Newton",
    "Decade": 1990
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Tracey Hickman",
    "Decade": 1990
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise",
    "Decade": 1990
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Dana Douglas",
    "Decade": 1990
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Samuel Wagner",
    "Decade": 1990
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Steve Newton",
    "Decade": 1990
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Tanya Koch",
    "Decade": 1990
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Eugene Green",
    "Decade": 2000
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Jared David",
    "Decade": 2000
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Michael Robinson",
    "Decade": 2000
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Brandi Bailey",
    "Decade": 2000
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Jared David",
    "Decade": 2000
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Michael Robinson",
    "Decade": 2000
  },
  {
    "Person1": "Jared David",
    "Person2": "Brandi Bailey",
    "Decade": 2000
  },
  {
    "Person1": "Jared David",
    "Person2": "Eugene Green",
    "Decade": 2000
  },
  {
    "Person1": "Jared David",
    "Person2": "Michael Robinson",
    "Decade": 2000
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey",
    "Decade": 2000
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Eugene Green",
    "Decade": 2000
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Jared David",
    "Decade": 2000
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 763
- **Execution Time:** 3.85s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 93: 94
**Status:** PASS

#### Natural Language Query
```
Which locations are classified as 'City' type?
```

#### Ground Truth Cypher
```cypher
match (l:Location)
where toLower(l.type) = 'city'
return l.name;
```

#### Generated Cypher
```cypher
MATCH (l:Location)
WHERE l.type = 'City'
RETURN l.name AS CityName, l.country AS Country, l.population AS Population
ORDER BY l.population DESC
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "l.name": "Stephaniemouth"
  },
  {
    "l.name": "Rivasside"
  },
  {
    "l.name": "Lake Michelle"
  },
  {
    "l.name": "Karenview"
  },
  {
    "l.name": "Simsview"
  },
  {
    "l.name": "Lake Justinview"
  },
  {
    "l.name": "Patricialand"
  },
  {
    "l.name": "East Patrick"
  },
  {
    "l.name": "North Robert"
  },
  {
    "l.name": "Perryborough"
  }
]
```

**Actual Results:**
```json
[
  {
    "CityName": "Karenview",
    "Country": "Seychelles",
    "Population": 13126125
  },
  {
    "CityName": "Patricialand",
    "Country": "Burundi",
    "Population": 12819117
  },
  {
    "CityName": "Stephaniemouth",
    "Country": "New Zealand",
    "Population": 11636146
  },
  {
    "CityName": "Perryborough",
    "Country": "Syrian Arab Republic",
    "Population": 10639534
  },
  {
    "CityName": "Lake Michelle",
    "Country": "Korea",
    "Population": 9619364
  },
  {
    "CityName": "Simsview",
    "Country": "Kazakhstan",
    "Population": 9234763
  },
  {
    "CityName": "Lake Justinview",
    "Country": "Grenada",
    "Population": 6060072
  },
  {
    "CityName": "East Patrick",
    "Country": "Cape Verde",
    "Population": 4875083
  },
  {
    "CityName": "Rivasside",
    "Country": "Kiribati",
    "Population": 3376763
  },
  {
    "CityName": "North Robert",
    "Country": "Greenland",
    "Population": 530926
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 720
- **Execution Time:** 2.63s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 94: 95
**Status:** PASS

#### Natural Language Query
```
Find companies founded in the 21st century.
```

#### Ground Truth Cypher
```cypher
match (c:Company)
where c.foundedYear > 2000
return c.name;
```

#### Generated Cypher
```cypher
MATCH (c:Company)
WHERE c.foundedYear >= 2000
RETURN c.name AS CompanyName, c.foundedYear AS FoundedYear
ORDER BY c.foundedYear
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "c.name": "Hooper PLC"
  },
  {
    "c.name": "Stuart, Higgins and Strickland"
  }
]
```

**Actual Results:**
```json
[
  {
    "CompanyName": "Hooper PLC",
    "FoundedYear": 2005
  },
  {
    "CompanyName": "Stuart, Higgins and Strickland",
    "FoundedYear": 2018
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 715
- **Execution Time:** 2.45s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 95: 96
**Status:** PASS

#### Natural Language Query
```
Which industry has the highest average company founding year?
```

#### Ground Truth Cypher
```cypher
match (c:Company)
with c.industry as industry, avg(c.foundedYear) as averageFunded
return industry
order by averageFunded desc
limit 1;
```

#### Generated Cypher
```cypher
MATCH (c:Company)
WHERE c.foundedYear IS NOT NULL AND c.industry IS NOT NULL
WITH c.industry AS industry, AVG(c.foundedYear) AS avgFoundingYear
RETURN industry, avgFoundingYear
ORDER BY avgFoundingYear DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "industry": "Education"
  }
]
```

**Actual Results:**
```json
[
  {
    "industry": "Education",
    "avgFoundingYear": 1957.5
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 741
- **Execution Time:** 2.45s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 96: 97
**Status:** FAIL

#### Natural Language Query
```
Find friends who have never lived in the same location at the same time.
```

#### Ground Truth Cypher
```cypher
match (p1:Person)-[:IS_FRIEND]-(p2:Person)
where p1.id < p2.id
and not exists {(p1)-[:LIVES_IN]-(:Location)-[:LIVES_IN]-(p2)}
and not exists {(p1)-[l1:LIVED_IN|LIVES_IN]-(:Location)-[l2:LIVED_IN|LIVES_IN]-(p2)
               where coalesce(l1.endYear, date().year) > l2.startYear
               and coalesce(l2.endYear, date().year) > l1.startYear}
return distinct p1.firstName, p2.firstName;
```

#### Generated Cypher
```cypher
MATCH (p1:Person)-[:IS_FRIEND]->(p2:Person)
WHERE NOT EXISTS {
    MATCH (p1)-[l1:LIVED_IN]->(loc:Location)<-[l2:LIVED_IN]-(p2)
    WHERE l1.startYear <= l2.endYear AND l1.endYear >= l2.startYear
}
AND p1 <> p2
RETURN p1.firstName + ' ' + p1.lastName AS Person1, 
       p2.firstName + ' ' + p2.lastName AS Person2
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Annette"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Mark",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Rachel"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Kevin",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "Connie",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Anna",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Juan",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Savannah",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Johnny"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Charles",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Jessica"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Johnny",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Vanessa"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Jessica",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Jared"
  },
  {
    "p1.firstName": "Jordan",
    "p2.firstName": "Todd"
  },
  {
    "p1.firstName": "Tanya",
    "p2.firstName": "Tracey"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Kevin"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Jared"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Todd"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Vanessa",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "David"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Tracey",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Thomas"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Brandi"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Jeffrey"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Timothy"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Crystal",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Jeffrey"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Annette"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Cheryl"
  },
  {
    "p1.firstName": "Nathaniel",
    "p2.firstName": "Steve"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Eugene"
  },
  {
    "p1.firstName": "Jeffrey",
    "p2.firstName": "Rachel"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "David",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Jared"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Annette",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Rachel"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Christopher"
  },
  {
    "p1.firstName": "Stephanie",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Steve"
  },
  {
    "p1.firstName": "Cheryl",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Savannah"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Brandi"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Logan"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Scott"
  },
  {
    "p1.firstName": "Thomas",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Connie"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Jared",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Samuel"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Theresa"
  },
  {
    "p1.firstName": "Eugene",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "April"
  },
  {
    "p1.firstName": "Timothy",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Scott"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Brandi",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Logan",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Anna"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Andrew"
  },
  {
    "p1.firstName": "Steve",
    "p2.firstName": "Joseph"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Scott"
  },
  {
    "p1.firstName": "Samuel",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "William"
  },
  {
    "p1.firstName": "April",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Theresa",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Andrew",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Todd"
  },
  {
    "p1.firstName": "William",
    "p2.firstName": "Rachel"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Matthew"
  },
  {
    "p1.firstName": "Tammy",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Donald"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Tammy"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Scott",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Donald",
    "p2.firstName": "Eric"
  },
  {
    "p1.firstName": "Todd",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Todd",
    "p2.firstName": "Rachel"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Rachel",
    "p2.firstName": "Angel"
  },
  {
    "p1.firstName": "Eric",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Eric",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Michael",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Matthew",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Juan"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Mia"
  },
  {
    "p1.firstName": "Christopher",
    "p2.firstName": "Dana"
  },
  {
    "p1.firstName": "Angel",
    "p2.firstName": "Debra"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Michael"
  },
  {
    "p1.firstName": "Joseph",
    "p2.firstName": "Debra"
  }
]
```

**Actual Results:**
```json
[
  {
    "Person1": "Anna Davis",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Mark Johnson"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Kevin Johnson"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Kevin Johnson"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Kevin Johnson"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Kevin Johnson"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Connie Lawrence"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Connie Lawrence"
  },
  {
    "Person1": "Jared David",
    "Person2": "Connie Lawrence"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Connie Lawrence"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Connie Lawrence"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Anna Davis"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Juan Calderon"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Savannah Delacruz"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Savannah Delacruz"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Mia Sutton"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Jared David",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Michael Robinson"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Debra Clark"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "William Brady",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Charles Taylor"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "William Brady",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "David Lee",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "April Wise",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Jessica Chavez"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Jared David",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Jordan Gonzalez"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Tanya Koch"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Tanya Koch"
  },
  {
    "Person1": "Jared David",
    "Person2": "Tanya Koch"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Tanya Koch"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Jared David",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "David Brown",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "April Wise",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "David Brown"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "David Brown"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "David Brown"
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "David Brown"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "David Brown"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "April Wise",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Crystal Whitehead"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Jared David",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Nathaniel Khan"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Jeffrey Henderson"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "David Lee"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee"
  },
  {
    "Person1": "April Wise",
    "Person2": "David Lee"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "David Lee"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "David Lee"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "David Lee"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Jared David",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "April Wise",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "William Brady",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Cheryl Robinson"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Jared David"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Jared David"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Jared David"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Jared David"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Jared David"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jared David"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Jared David"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Eugene Green"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Eugene Green"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Eugene Green"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Eugene Green"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "April Wise",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Timothy Walls"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "David Brown",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Brandi Bailey"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Logan Archer"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Logan Archer"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Logan Archer"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Logan Archer"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Logan Archer"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Steve Newton"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Steve Newton"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Steve Newton"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Steve Newton"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Steve Newton"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "William Brady",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "April Wise"
  },
  {
    "Person1": "David Lee",
    "Person2": "April Wise"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "April Wise"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "April Wise"
  },
  {
    "Person1": "William Brady",
    "Person2": "April Wise"
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "April Wise"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "April Wise"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "David Lee",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "William Brady"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "William Brady"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "William Brady"
  },
  {
    "Person1": "April Wise",
    "Person2": "William Brady"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "William Brady"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "William Brady"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Tammy Ryan",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Donald Jones"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Donald Jones"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Donald Jones"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "William Brady",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "William Brady",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Rachel Graham"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "David Brown",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "April Wise",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "April Wise",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Matthew Marshall"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "David Brown",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Dana Douglas",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Jared David",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Angel Riggs"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "David Lee",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Joseph Williams"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 769
- **Execution Time:** 3.59s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 97: 98
**Status:** PASS

#### Natural Language Query
```
What is the most common birth month?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
with date(p.birthDate).month as birthMonth, count(*) as born
order by born desc
return birthMonth
limit 1;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE p.birthDate IS NOT NULL
WITH split(p.birthDate, '-')[1] AS birthMonth, count(*) AS count
RETURN birthMonth, count
ORDER BY count DESC
LIMIT 1
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "birthMonth": 12
  }
]
```

**Actual Results:**
```json
[
  {
    "birthMonth": "12",
    "count": 6
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 723
- **Execution Time:** 2.49s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 98: 99
**Status:** PASS

#### Natural Language Query
```
How many people have the same first and last name?
```

#### Ground Truth Cypher
```cypher
match (p:Person)
where p.firstName = p.lastName
return count(p);
```

#### Generated Cypher
```cypher
MATCH (p1:Person), (p2:Person)
WHERE p1 <> p2 AND toLower(p1.firstName) = toLower(p2.firstName) AND toLower(p1.lastName) = toLower(p2.lastName)
WITH count(DISTINCT p1) AS count
RETURN count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "count(p)": 0
  }
]
```

**Actual Results:**
```json
[
  {
    "count": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 732
- **Execution Time:** 2.76s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 99: 100
**Status:** FAIL

#### Natural Language Query
```
How many people were born on the sun?
```

#### Ground Truth Cypher
```cypher
match (n)
where 1=2
return n;
```

#### Generated Cypher
```cypher
MATCH (p:Person)
WHERE toLower(p.birthPlace) = 'sun'
RETURN count(p) AS peopleCountBornOnSun
```

#### Results Comparison

**Expected Results:**
```json
[]
```

**Actual Results:**
```json
[
  {
    "peopleCountBornOnSun": 0
  }
]
```

#### Additional Information

- **Category:** paradox
- **Difficulty:** easy
- **Tokens Used:** 705
- **Execution Time:** 2.65s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---
