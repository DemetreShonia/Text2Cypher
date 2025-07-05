# Evaluation Report: Detailed + No-Retrieval

**Run Time:** 2025-07-04 19:19:47

## Summary Metrics

- **Total Cases:** 99
- **Overall Accuracy:** 68.69%
- **Syntactic Correctness:** 96.97%
- **Execution Success:** 89.90%
- **Total Tokens:** 132,960

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
RETURN category, jobCount
ORDER BY jobCount DESC
LIMIT 1
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
- **Tokens Used:** 1,339
- **Execution Time:** 4.32s
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
RETURN gender AS most_common_gender, count AS count
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
    "most_common_gender": "Male",
    "count": 30
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,340
- **Execution Time:** 4.48s
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
- **Tokens Used:** 1,324
- **Execution Time:** 1.81s
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
RETURN count(p) AS markCount
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
- **Tokens Used:** 1,327
- **Execution Time:** 1.65s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 5: 5
**Status:** PASS

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
MATCH (l:Location)
RETURN SUM(l.population) AS totalPopulation
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
    "totalPopulation": 81917893
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,329
- **Execution Time:** 2.25s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
- **Tokens Used:** 1,350
- **Execution Time:** 2.96s
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
MATCH (p:Person)-[:IS_SIBLING]->(s:Person)
WHERE p.birthDate < s.birthDate AND s.gender = 'Female'
WITH p
MATCH (p)-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'Current'
WITH p, c
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WHERE h.companyId = c.id AND h.endYear IS NULL AND toLower(j.title) = 'data scientist'
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
- **Tokens Used:** 1,402
- **Execution Time:** 3.65s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 8: 8
**Status:** PASS

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
MATCH (p:Person {firstName: 'Mark'})-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'Current'
RETURN c.name AS CurrentWorkplace
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
    "CurrentWorkplace": "Johnson-Rogers"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,335
- **Execution Time:** 2.54s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 9: 9
**Status:** PASS

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
WHERE toLower(p.firstName) = 'mark' AND toLower(c.industry) = 'technology'
WITH p, c
MATCH (p)-[:LIVES_IN]->(l:Location)
WHERE toLower(l.country) = 'spain'
RETURN COUNT(DISTINCT p) AS marksTechSpain
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
    "marksTechSpain": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,374
- **Execution Time:** 3.19s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 10: 10
**Status:** PASS

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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WHERE toLower(l.country) = 'new zealand' AND p.gender = 'Female'
WITH p.firstName AS girlName, COUNT(*) AS count
ORDER BY count DESC
LIMIT 1
RETURN girlName AS mostPopularGirlName, count
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
[
  {
    "mostPopularGirlName": "Mia",
    "count": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,368
- **Execution Time:** 3.51s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p:Person)-[:HAD_POSITION]->(j:JobTitle), (p)-[:LIVES_IN]->(l:Location)
WHERE toLower(p.firstName) = 'mia'
  AND toLower(j.title) = 'doctor'
  AND toLower(l.country) = 'new zealand'
RETURN COUNT(DISTINCT p) AS doctorMiaCount
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
    "doctorMiaCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,369
- **Execution Time:** 4.72s
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
WITH p, size((p)-[:IS_FRIEND]-()) AS friendCount
RETURN avg(friendCount) AS averageFriends
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 3, column 14 (offset: 160))
"WITH p, size((p)-[:IS_FRIEND]-()) AS friendCount"
              ^}
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 1,375
- **Execution Time:** 2.83s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
WHERE samuel.firstName =~ '(?i)samuel'
  AND dana.firstName =~ '(?i)dana'
  AND duration.between(date(samuel.birthDate), date()).years > 20
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
- **Tokens Used:** 1,390
- **Execution Time:** 2.94s
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
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)-[:LOCATED_IN]->(l:Location {country: 'Yemen'})
MATCH (p)-[:STUDIED]->(f:FieldOfStudy)
WITH f.name AS subject, COUNT(DISTINCT p) AS studentCount
ORDER BY studentCount DESC
LIMIT 1
RETURN subject AS mostPopularSubject, studentCount
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
- **Tokens Used:** 1,384
- **Execution Time:** 3.19s
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
WHERE p.firstName = 'Connie' AND toLower(f.name) = 'business administration'
RETURN COUNT(DISTINCT p) AS count
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
- **Tokens Used:** 1,358
- **Execution Time:** 2.56s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 16: 16
**Status:** PASS

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
MATCH (l:Location)
WHERE l.type = 'City'
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
    "averageResidents": 8191789.300000001
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 1,333
- **Execution Time:** 1.81s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (l:Location)<-[r:LIVES_IN]-(:Person)
WITH l, count(r) AS residentCount
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
- **Tokens Used:** 1,344
- **Execution Time:** 2.15s
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
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WITH e, COUNT(DISTINCT p) AS studentCount
RETURN e.name AS institution, studentCount
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
    "institution": "Smithstad University",
    "studentCount": 9
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,357
- **Execution Time:** 2.53s
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
MATCH (l:Location {name: 'New Zealand', type: 'City'})
WHERE l.population IS NOT NULL
RETURN l.population - COALESCE(
  (l.population * 0.1),  // Assuming 10% of current population as a rough estimate for 100 years ago
  5000  // Minimum population in the schema
) AS population_increase
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
- **Tokens Used:** 1,388
- **Execution Time:** 3.05s
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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WHERE toLower(l.country) = 'new zealand'
WITH p, l, date() AS currentDate
RETURN AVG(duration.between(date(p.birthDate), currentDate).years) AS averageAge
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
- **Tokens Used:** 1,358
- **Execution Time:** 2.31s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 21: 21
**Status:** PASS

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
WHERE loc.country = e.country
WITH count(DISTINCT p) AS studiedAbroadAndStayed
MATCH (p:Person)
WHERE EXISTS((p)-[:STUDIED_AT]->())
WITH studiedAbroadAndStayed, count(p) AS totalStudents
RETURN 
    CASE 
        WHEN toFloat(studiedAbroadAndStayed) / totalStudents > 0.5 
        THEN 'There is a correlation between studying abroad and staying there permanently' 
        ELSE 'There is no correlation between studying abroad and staying there permanently' 
    END AS result
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
[
  {
    "result": "There is no correlation between studying abroad and staying there permanently"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,491
- **Execution Time:** 5.92s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE e.country <> p.nationality
WITH p, e, s
MATCH (p)-[l:LIVES_IN]->(loc:Location)
WHERE loc.country = p.nationality AND date(l.since) > date(toString(s.endYear) + '-01-01')
WITH count(DISTINCT p) AS studiedAbroadAndReturned

MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE e.country <> p.nationality
WITH studiedAbroadAndReturned, count(DISTINCT p) AS totalStudiedAbroad

RETURN 
  CASE 
    WHEN totalStudiedAbroad > 0 AND (studiedAbroadAndReturned * 1.0 / totalStudiedAbroad) > 0.5 
    THEN true 
    ELSE false 
  END AS isCorrelated,
  studiedAbroadAndReturned,
  totalStudiedAbroad
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
    "isCorrelated": false,
    "studiedAbroadAndReturned": 0,
    "totalStudiedAbroad": 31
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,501
- **Execution Time:** 5.41s
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
MATCH (p:Person)
WITH p, [(p)-[:STUDIED_AT]->(edu:EducationalInstitution) | edu.country] AS studyCountries,
     [(p)-[:LIVES_IN|LIVED_IN]->(loc:Location) | loc.country] AS livedCountries
WHERE size(studyCountries) > 0 AND size(livedCountries) > 0
WITH p,
     [country IN studyCountries WHERE country <> p.nationality] AS foreignStudyCountries,
     [country IN livedCountries WHERE country <> p.nationality] AS foreignLivedCountries
WHERE size(foreignStudyCountries) > 0
WITH count(p) AS totalStudiedAbroad,
     count(CASE WHEN size(foreignLivedCountries) > 0 THEN p END) AS studiedAbroadAndMovedAgain
RETURN 
    totalStudiedAbroad,
    studiedAbroadAndMovedAgain,
    toFloat(studiedAbroadAndMovedAgain) / totalStudiedAbroad AS correlationRatio,
    CASE 
        WHEN toFloat(studiedAbroadAndMovedAgain) / totalStudiedAbroad > 0.5 
        THEN 'There is a correlation between studying abroad and changing countries again'
        ELSE 'There is no strong correlation between studying abroad and changing countries again'
    END AS conclusion
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
    "totalStudiedAbroad": 31,
    "studiedAbroadAndMovedAgain": 31,
    "correlationRatio": 1.0,
    "conclusion": "There is a correlation between studying abroad and changing countries again"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,599
- **Execution Time:** 7.64s
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
     endsWith(toLower(p.email), '@yahoo.com') AS isYahooEmail
OPTIONAL MATCH (p)-[w:WORKED_AT]->(c:Company)
OPTIONAL MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WITH p, isYahooEmail, 
     CASE WHEN c.industry = 'Technology' OR j.category = 'Technology' THEN true ELSE false END AS worksInTech
WITH COUNT(p) AS totalPeople,
     SUM(CASE WHEN isYahooEmail AND NOT worksInTech THEN 1 ELSE 0 END) AS yahooNotTech,
     SUM(CASE WHEN isYahooEmail THEN 1 ELSE 0 END) AS totalYahoo
RETURN 
    CASE 
        WHEN totalYahoo > 0 AND yahooNotTech * 1.0 / totalYahoo > 0.5 
        THEN 'There is a correlation between Yahoo! email and not working in tech'
        ELSE 'There is no significant correlation between Yahoo! email and not working in tech'
    END AS result
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Unknown function 'endsWith' (line 3, column 6 (offset: 63))
"     endsWith(toLower(p.email), '@yahoo.com') AS isYahooEmail"
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
- **Tokens Used:** 1,550
- **Execution Time:** 6.07s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 25: 25
**Status:** PASS

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
MATCH (p)-[:IS_CHILD]->(parent:Person)
MATCH (parent)-[:IS_PARENT]->(sibling:Person)
WHERE sibling.gender = 'Female' AND sibling <> p
WITH p, COUNT(DISTINCT sibling) AS sisterCount
RETURN AVG(sisterCount) AS averageSisterCount
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
    "averageSisterCount": 2.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,380
- **Execution Time:** 3.33s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WHERE toLower(christopher.firstName) = 'christopher'
  AND toLower(jessica.firstName) = 'jessica'
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
- **Tokens Used:** 1,370
- **Execution Time:** 2.39s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 27: 27
**Status:** PASS

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
MATCH (p:Person)-[s:STUDIED]->(f:FieldOfStudy)
WITH p, f, s
MATCH (p)-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'Current'
WITH p, f, s, c
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WHERE h.companyId = c.id AND h.endYear IS NULL
WITH p, f, s, j
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
    "peopleWorkingInStudiedField": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,399
- **Execution Time:** 3.45s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WITH p, toLower(p.firstName + '.' + p.lastName) AS nameEmail, toLower(split(p.email, '@')[0]) AS emailUsername
WITH COUNT(p) AS totalPeople, SUM(CASE WHEN nameEmail = emailUsername THEN 1 ELSE 0 END) AS nameEmailCount
RETURN toFloat(nameEmailCount) / totalPeople * 100 AS percentageUsingNameAsEmail
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
    "percentageUsingNameAsEmail": 0.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,392
- **Execution Time:** 3.04s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 29: 29
**Status:** PASS

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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WHERE toLower(p.firstName) = 'jordan'
WITH l.country AS country, COUNT(p) AS count
ORDER BY count DESC
LIMIT 1
RETURN country, count
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "loc.country": "Kazakhstan",
    "count(p)": 1
  }
]
```

**Actual Results:**
```json
[
  {
    "country": "Kazakhstan",
    "count": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,357
- **Execution Time:** 2.16s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (connie:Person)-[:IS_SIBLING]-(sister:Person)
WHERE toLower(connie.firstName) = 'connie'
MATCH (sister)-[worked:HAD_POSITION]->(position:JobTitle)
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
- **Tokens Used:** 1,360
- **Execution Time:** 2.64s
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
WITH p, COUNT(c) AS childCount
MATCH (p)-[:LIVES_IN]->(:Location {name: 'Grenada'})
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
- **Tokens Used:** 1,357
- **Execution Time:** 2.35s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 32: 32
**Status:** PASS

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
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)
WHERE toLower(e.country) = 'french southern territories'
WITH p
MATCH (p)-[:IS_FRIEND]->(friend:Person)-[:WORKED_AT]->(c:Company)
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
- **Tokens Used:** 1,395
- **Execution Time:** 2.83s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p1:Person)-[:WORKED_AT]->(c:Company {industry: 'Education'})
MATCH (p1)-[r:IS_HUSBAND|IS_WIFE]->(p2:Person)-[:LIVES_IN]->(l:Location {name: 'Grenada'})
RETURN COUNT(DISTINCT p1) AS count
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
- **Tokens Used:** 1,372
- **Execution Time:** 2.32s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 34: 34
**Status:** FAIL

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
WITH p, size((p)-[:STUDIED_AT]->()) AS educationCount, size((p)-[:WORKED_AT]->()) AS careerCount
WHERE educationCount > 0 AND careerCount > 0
WITH p, educationCount, careerCount
MATCH (p)-[:STUDIED_AT]->(edu:EducationalInstitution)
WITH p, educationCount, careerCount, collect(edu.name) AS educations
MATCH (p)-[:WORKED_AT]->(comp:Company)
WITH p, educationCount, careerCount, educations, collect(comp.name) AS companies
MATCH (p)-[:STUDIED]->(field:FieldOfStudy)
WITH p, educationCount, careerCount, educations, companies, collect(field.name) AS fields
MATCH (p)-[:HAD_POSITION]->(job:JobTitle)
WITH p, educationCount, careerCount, educations, companies, fields, collect(job.title) AS jobs
WITH p, 
     CASE WHEN any(f IN fields WHERE toLower(f) IN [toLower(j) FOR j IN jobs]) OR
               any(e IN educations WHERE any(c IN companies WHERE toLower(c) CONTAINS toLower(e)))
          THEN 1 ELSE 0 END AS isCorrelated,
     count(p) AS totalPeople
WITH sum(isCorrelated) AS correlatedCount, totalPeople
RETURN 
    CASE WHEN toFloat(correlatedCount) / toFloat(totalPeople) > 0.5 
    THEN 'Education and career are correlated for more than half of the population.' 
    ELSE 'Education and career are not correlated for more than half of the population.' 
    END AS result
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'WHEN': expected an expression, 'FOREACH', ',', 'AS', 'ORDER BY', 'CALL', 'CREATE', 'LOAD CSV', 'DELETE', 'DETACH', 'FINISH', 'INSERT', 'LIMIT', 'MATCH', 'MERGE', 'NODETACH', 'OFFSET', 'OPTIONAL', 'REMOVE', 'RETURN', 'SET', 'SKIP', 'UNION', 'UNWIND', 'USE', 'WHERE', 'WITH' or <EOF> (line 14, column 11 (offset: 727))
"     CASE WHEN any(f IN fields WHERE toLower(f) IN [toLower(j) FOR j IN jobs]) OR"
           ^}
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 1,652
- **Execution Time:** 7.17s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
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
- **Execution Time:** 3.82s
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
MATCH path = (matthew)-[:IS_FRIEND*1..10]-(connected:Person)
WHERE all(r IN relationships(path) WHERE type(r) = 'IS_FRIEND')
WITH DISTINCT connected
RETURN count(connected) = (MATCH (p:Person) RETURN count(p))
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'RETURN': expected an expression or ')' (line 6, column 45 (offset: 252))
"RETURN count(connected) = (MATCH (p:Person) RETURN count(p))"
                                             ^}
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
- **Tokens Used:** 1,396
- **Execution Time:** 2.84s
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
MATCH (start:Person)-[:LIVES_IN]->(:Location {country: 'New Zealand'})
WITH collect(start) AS nz_residents
MATCH (company:Company)
WHERE company.name IN ['Johnson-Rogers, Hooper PLC', 'Patterson, Camacho and White', 'Rogers-Hobbs', 'Ruiz Ltd']
WITH nz_residents, collect(company) AS target_companies
MATCH (end:Person)-[:WORKED_AT]->(company)
WHERE company IN target_companies AND end.status = 'Current'
WITH nz_residents, collect(end) AS target_employees
UNWIND nz_residents AS start
UNWIND target_employees AS end
MATCH path = shortestPath((start)-[*..10]-(end))
WHERE all(r IN relationships(path) WHERE type(r) <> 'WORKED_AT')
WITH avg(length(path)) AS avg_hops
RETURN round(avg_hops, 2) AS average_hops
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
    "average_hops": null
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 1,520
- **Execution Time:** 17.78s
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
MATCH (p:Person)-[w:WORKED_AT]->(c:Company)
WITH p, c.country AS country, COUNT(DISTINCT w.companyId) AS jobCount
WITH country, AVG(jobCount) AS avgJobs
RETURN country, avgJobs
ORDER BY avgJobs DESC
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
    "country": null,
    "avgJobs": 0.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 1,366
- **Execution Time:** 2.91s
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
MATCH (m:Person {gender: 'Male'})-[:IS_HUSBAND]->(w:Person {gender: 'Female'}),
      (m)-[:IS_SIBLING]->(s:Person {gender: 'Female'})
WHERE date(w.birthDate) < date(s.birthDate)
RETURN DISTINCT m.firstName, m.lastName, w.firstName AS wife_firstName, w.lastName AS wife_lastName, s.firstName AS sister_firstName, s.lastName AS sister_lastName
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
- **Tokens Used:** 1,398
- **Execution Time:** 3.87s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 40: 40
**Status:** PASS

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
MATCH (l:Location)<-[r:LIVES_IN]-(p:Person)
WITH l, COUNT(CASE WHEN p.gender = 'Male' THEN 1 END) AS maleCount,
     COUNT(CASE WHEN p.gender = 'Female' THEN 1 END) AS femaleCount
WHERE maleCount > femaleCount
RETURN l.name AS Location, maleCount, femaleCount
ORDER BY (maleCount - femaleCount) DESC
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
[
  {
    "Location": "Simsview",
    "maleCount": 5,
    "femaleCount": 1
  },
  {
    "Location": "Lake Michelle",
    "maleCount": 5,
    "femaleCount": 2
  },
  {
    "Location": "Rivasside",
    "maleCount": 5,
    "femaleCount": 3
  },
  {
    "Location": "East Patrick",
    "maleCount": 4,
    "femaleCount": 2
  },
  {
    "Location": "Stephaniemouth",
    "maleCount": 3,
    "femaleCount": 2
  },
  {
    "Location": "Patricialand",
    "maleCount": 2,
    "femaleCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,387
- **Execution Time:** 3.39s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (l:Location)<-[r:LIVES_IN]-(p:Person)
WITH l, 
     COUNT(CASE WHEN p.gender = 'Male' THEN p END) AS maleCount,
     COUNT(CASE WHEN p.gender = 'Female' THEN p END) AS femaleCount
WHERE maleCount > femaleCount
RETURN l.name AS location, maleCount, femaleCount, l.population AS totalPopulation
ORDER BY (maleCount - femaleCount) DESC
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
    "location": "Simsview",
    "maleCount": 5,
    "femaleCount": 1,
    "totalPopulation": 9234763
  },
  {
    "location": "Lake Michelle",
    "maleCount": 5,
    "femaleCount": 2,
    "totalPopulation": 9619364
  },
  {
    "location": "Rivasside",
    "maleCount": 5,
    "femaleCount": 3,
    "totalPopulation": 3376763
  },
  {
    "location": "East Patrick",
    "maleCount": 4,
    "femaleCount": 2,
    "totalPopulation": 4875083
  },
  {
    "location": "Stephaniemouth",
    "maleCount": 3,
    "femaleCount": 2,
    "totalPopulation": 11636146
  },
  {
    "location": "Patricialand",
    "maleCount": 2,
    "femaleCount": 1,
    "totalPopulation": 12819117
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 1,410
- **Execution Time:** 3.34s
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
- **Tokens Used:** 1,383
- **Execution Time:** 2.94s
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
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE toLower(p.nationality) <> toLower(e.country)
WITH e, COUNT(DISTINCT p) AS foreignStudentCount
ORDER BY foreignStudentCount DESC
LIMIT 10
RETURN e.name AS EducationalInstitution, e.country AS Country, foreignStudentCount
ORDER BY foreignStudentCount DESC
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
    "EducationalInstitution": "Smithstad University",
    "Country": "French Southern Territories",
    "foreignStudentCount": 9
  },
  {
    "EducationalInstitution": "South Jeffrey Institute",
    "Country": "Jordan",
    "foreignStudentCount": 8
  },
  {
    "EducationalInstitution": "Priceshire Institute",
    "Country": "Yemen",
    "foreignStudentCount": 7
  },
  {
    "EducationalInstitution": "Castanedachester Institute",
    "Country": "Mauritania",
    "foreignStudentCount": 6
  },
  {
    "EducationalInstitution": "Port Nicoleshire Institute",
    "Country": "Hong Kong",
    "foreignStudentCount": 5
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,392
- **Execution Time:** 3.14s
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
MATCH (wife:Person)-[:IS_WIFE]->(husband:Person)
WHERE date(wife.birthDate) < date(husband.birthDate)
RETURN wife.firstName + ' ' + wife.lastName AS OlderWife, husband.firstName + ' ' + husband.lastName AS YoungerHusband, wife.birthDate AS WifeBirthDate, husband.birthDate AS HusbandBirthDate
ORDER BY WifeBirthDate
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
    "OlderWife": "Charles Taylor",
    "YoungerHusband": "Johnny Campos",
    "WifeBirthDate": "1934-01-16",
    "HusbandBirthDate": "1943-03-10"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** easy
- **Tokens Used:** 1,385
- **Execution Time:** 3.26s
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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WHERE EXISTS((p)-[:IS_HUSBAND]->()) OR EXISTS((p)-[:IS_WIFE]->())
WITH l, p, p.birthDate AS birthDate
ORDER BY birthDate
WITH l, COLLECT(p)[0] AS oldestMarriedPerson
RETURN l.name AS city, oldestMarriedPerson.firstName + ' ' + oldestMarriedPerson.lastName AS oldestMarriedPerson, oldestMarriedPerson.birthDate AS birthDate
ORDER BY birthDate
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
    "city": "Lake Justinview",
    "oldestMarriedPerson": "Mark Johnson",
    "birthDate": "1928-06-16"
  },
  {
    "city": "Lake Michelle",
    "oldestMarriedPerson": "Kevin Johnson",
    "birthDate": "1929-11-07"
  },
  {
    "city": "Simsview",
    "oldestMarriedPerson": "Charles Taylor",
    "birthDate": "1934-01-16"
  },
  {
    "city": "Karenview",
    "oldestMarriedPerson": "Savannah Delacruz",
    "birthDate": "1935-02-12"
  },
  {
    "city": "Stephaniemouth",
    "oldestMarriedPerson": "Johnny Campos",
    "birthDate": "1943-03-10"
  },
  {
    "city": "North Robert",
    "oldestMarriedPerson": "Juan Calderon",
    "birthDate": "1948-05-13"
  },
  {
    "city": "Perryborough",
    "oldestMarriedPerson": "Michael Robinson",
    "birthDate": "2000-03-19"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,406
- **Execution Time:** 3.43s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 46: 46
**Status:** PASS

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
WITH COLLECT(DISTINCT descendant) AS familyMembers
WHERE ALL(member IN familyMembers WHERE EXISTS((member)-[:WORKED_AT]->(:Company)))
WITH familyMembers
MATCH (member:Person)-[:IS_PARENT]->(child:Person)
WHERE member IN familyMembers AND child IN familyMembers
RETURN DISTINCT member.firstName + ' ' + member.lastName AS Parent,
       child.firstName + ' ' + child.lastName AS Child,
       [(member)-[w:WORKED_AT]->(c:Company) | c.name] AS ParentCompanies,
       [(child)-[w:WORKED_AT]->(c:Company) | c.name] AS ChildCompanies
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
- **Tokens Used:** 1,472
- **Execution Time:** 4.72s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
    MATCH (p)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING|IS_FRIEND|STUDIED_AT|STUDIED|WORKED_AT|HAD_POSITION|LIVES_IN|LIVED_IN]-()
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
- **Tokens Used:** 1,351
- **Execution Time:** 2.26s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 48: 48
**Status:** PASS

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
MATCH (person1:Person)
MATCH (person2:Person)
WHERE person1 <> person2
MATCH (person1)-[:IS_CHILD*2]->(grandparent1:Person)
MATCH (person2)-[:IS_CHILD*2]->(grandparent2:Person)
MATCH (grandparent1)-[:IS_SIBLING]->(grandparent2)
WHERE NOT (person1)-[:IS_SIBLING]-(person2)
AND NOT (person1)-[:IS_CHILD|IS_PARENT*1..2]-(person2)
RETURN DISTINCT person1, person2
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

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 1,393
- **Execution Time:** 3.54s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
     size([(p)-[:IS_SIBLING]-(sibling) | sibling]) AS siblingCount,
     size([(p)<-[:IS_CHILD]-(:Person)<-[:IS_PARENT]-(grandparent)-[:IS_PARENT]->(:Person)-[:IS_PARENT]->(cousin:Person) 
           WHERE NOT (p)-[:IS_SIBLING]-(cousin) | cousin]) AS cousinCount
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
    "cousinCount": 12,
    "siblingCount": 0
  },
  {
    "name": "Kevin Johnson",
    "cousinCount": 12,
    "siblingCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,412
- **Execution Time:** 4.28s
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
MATCH (p2)-[s2:STUDIED_AT]->(e:EducationalInstitution)
WHERE s1.startYear < toInteger(substring(p1.birthDate, 0, 4)) OR s2.startYear < toInteger(substring(p2.birthDate, 0, 4))
RETURN p1.firstName + ' ' + p1.lastName AS Sibling1, p2.firstName + ' ' + p2.lastName AS Sibling2, e.name AS Institution, 
       CASE 
         WHEN s1.startYear < toInteger(substring(p1.birthDate, 0, 4)) THEN p1.firstName + ' ' + p1.lastName
         ELSE p2.firstName + ' ' + p2.lastName
       END AS StudiedBeforeBirth
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
- **Tokens Used:** 1,466
- **Execution Time:** 5.99s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 51: 51
**Status:** PASS

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
MATCH (p:Person)
WHERE NOT EXISTS((p)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING]-())
WITH p, date(p.birthDate) AS birthDate
ORDER BY birthDate ASC
LIMIT 1
RETURN p.firstName + ' ' + p.lastName AS oldestPersonWithoutFamily, p.birthDate AS birthDate
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Andrew"
  }
]
```

**Actual Results:**
```json
[
  {
    "oldestPersonWithoutFamily": "Andrew Diaz",
    "birthDate": "1926-01-22"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,374
- **Execution Time:** 2.78s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WITH p, child, date(p.birthDate) AS birthDate
ORDER BY birthDate DESC
LIMIT 1
RETURN p.firstName + ' ' + p.lastName AS youngestParent, p.birthDate AS birthDate, COUNT(child) AS numberOfChildren
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
    "birthDate": "2000-03-19",
    "numberOfChildren": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,367
- **Execution Time:** 2.66s
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
WITH p, size((p)-[:LIVED_IN]->()) + size((p)-[:LIVES_IN]->()) AS total_locations
ORDER BY total_locations DESC
LIMIT 1
RETURN p.firstName + ' ' + p.lastName AS most_traveled_person, total_locations
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 30))
"WITH p, size((p)-[:LIVED_IN]->()) + size((p)-[:LIVES_IN]->()) AS total_locations"
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
- **Tokens Used:** 1,361
- **Execution Time:** 2.37s
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
- **Tokens Used:** 1,354
- **Execution Time:** 2.63s
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
WITH p, [(p)-[:LIVED_IN]->(l:Location) | l] + [(p)-[:LIVES_IN]->(l:Location) | l] AS locations
WHERE size(apoc.coll.toSet(locations)) = 3
RETURN p.firstName + ' ' + p.lastName AS name, size(apoc.coll.toSet(locations)) AS locationChanges
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Unknown function 'apoc.coll.toSet' (line 3, column 12 (offset: 123))
"WHERE size(apoc.coll.toSet(locations)) = 3"
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
- **Tokens Used:** 1,373
- **Execution Time:** 3.04s
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
MATCH (p1:Person)-[f:IS_FRIEND]-(p2:Person)
WHERE toLower(f.since) CONTAINS 'facebook'
RETURN p1, p2
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
- **Tokens Used:** 1,334
- **Execution Time:** 1.81s
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
MATCH (p:Person)-[r:HAD_POSITION]->(j:JobTitle)
WHERE toLower(j.title) =~ '.*cher$'
RETURN DISTINCT p.firstName, p.lastName, j.title
ORDER BY p.lastName, p.firstName
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
    "p.firstName": "William",
    "p.lastName": "Brady",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Juan",
    "p.lastName": "Calderon",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Jessica",
    "p.lastName": "Chavez",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Savannah",
    "p.lastName": "Delacruz",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Jordan",
    "p.lastName": "Gonzalez",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Tracey",
    "p.lastName": "Hickman",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Nathaniel",
    "p.lastName": "Khan",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "David",
    "p.lastName": "Lee",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Joseph",
    "p.lastName": "Maddox",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Michael",
    "p.lastName": "Orr",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Angel",
    "p.lastName": "Riggs",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Ryan",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Theresa",
    "p.lastName": "Vazquez",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Samuel",
    "p.lastName": "Wagner",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Crystal",
    "p.lastName": "Whitehead",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Joseph",
    "p.lastName": "Williams",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Todd",
    "p.lastName": "Wilson",
    "j.title": "Teacher"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,353
- **Execution Time:** 2.59s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 58: 58
**Status:** PASS

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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WHERE toLower(p.birthPlace) = toLower(l.name)
  AND EXISTS((p)-[:LIVES_IN]->(:Location))
RETURN p.firstName, p.lastName, l.name AS currentCity
LIMIT 100
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
- **Tokens Used:** 1,362
- **Execution Time:** 2.39s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p1:Person)-[:IS_SIBLING]-(p2:Person)
WHERE id(p1) < id(p2)
MATCH (p1)-[s1:STUDIED]->(f:FieldOfStudy)<-[s2:STUDIED]-(p2)
WHERE s1.degree = s2.degree
RETURN p1.firstName + ' ' + p1.lastName AS Sibling1,
       p2.firstName + ' ' + p2.lastName AS Sibling2,
       f.name AS FieldOfStudy,
       s1.degree AS Degree
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
- **Tokens Used:** 1,389
- **Execution Time:** 3.60s
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
- **Tokens Used:** 1,339
- **Execution Time:** 1.68s
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
- **Execution Time:** 1.90s
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
WHERE EXISTS((p)-[:IS_PARENT]->(:Person))
  AND EXISTS((:Person)-[:IS_PARENT]->(p))
RETURN p.firstName + ' ' + p.lastName AS name, p.id AS id
ORDER BY name
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
    "name": "Charles Taylor",
    "id": "p10"
  },
  {
    "name": "Connie Lawrence",
    "id": "p3"
  },
  {
    "name": "Joseph Maddox",
    "id": "p12"
  },
  {
    "name": "Mia Sutton",
    "id": "p7"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,357
- **Execution Time:** 2.61s
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
WHERE EXISTS((p1)-[:LIVES_IN]->()) AND EXISTS((p2)-[:LIVES_IN]->())
WITH p1, p2
MATCH (p1)-[:LIVES_IN]->(l1:Location), (p2)-[:LIVES_IN]->(l2:Location)
WHERE l1 <> l2
RETURN p1.firstName + ' ' + p1.lastName AS Person1, 
       p2.firstName + ' ' + p2.lastName AS Person2, 
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
    "Person1": "Mark Johnson",
    "Person2": "Kevin Johnson",
    "City1": "Lake Justinview",
    "City2": "Lake Michelle"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Anna Davis",
    "City1": "Lake Justinview",
    "City2": "Lake Michelle"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Juan Calderon",
    "City1": "Karenview",
    "City2": "North Robert"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Michael Robinson",
    "City1": "Stephaniemouth",
    "City2": "Perryborough"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Charles Taylor",
    "City1": "Stephaniemouth",
    "City2": "Simsview"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Joseph Maddox",
    "City1": "Simsview",
    "City2": "Lake Michelle"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Mark Johnson",
    "City1": "Lake Michelle",
    "City2": "Lake Justinview"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Connie Lawrence",
    "City1": "Lake Michelle",
    "City2": "Lake Justinview"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz",
    "City1": "North Robert",
    "City2": "Karenview"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Mia Sutton",
    "City1": "Perryborough",
    "City2": "Stephaniemouth"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "City1": "Simsview",
    "City2": "Stephaniemouth"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Jessica Chavez",
    "City1": "Lake Michelle",
    "City2": "Simsview"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 1,405
- **Execution Time:** 3.66s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 64: 65
**Status:** FAIL

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
MATCH (p1:Person)-[:IS_FRIEND]-(p2:Person)-[:IS_FRIEND]-(p3:Person)-[:IS_FRIEND]-(p1:Person)
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
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "Person3": "Thomas Schmidt"
  },
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
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "Person3": "Brandi Bailey"
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
    "Person3": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Maddox"
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
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Jessica Chavez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Jessica Chavez"
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
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Timothy Walls"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Timothy Walls"
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
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "Person3": "William Brady"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "Person3": "William Brady"
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
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Michael Orr"
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
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Maddox"
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
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Jessica Chavez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos",
    "Person3": "Jessica Chavez"
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
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Timothy Walls"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Timothy Walls"
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
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "Person3": "William Brady"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "Person3": "William Brady"
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
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Michael Orr"
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
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos",
    "Person3": "Joseph Williams"
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
    "Person3": "Vanessa Patel"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Vanessa Patel"
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
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Cheryl Robinson"
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
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
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
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "Person3": "Tammy Patton"
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
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
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
    "Person3": "Vanessa Patel"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Vanessa Patel"
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
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Joseph Maddox",
    "Person3": "Cheryl Robinson"
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
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox",
    "Person3": "Andrew Diaz"
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
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "Person3": "Tammy Patton"
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
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "Person3": "Joseph Williams"
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
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
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
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
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
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
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
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Jordan Gonzalez"
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
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Michael Orr"
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
    "Person1": "Mia Sutton",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jessica Chavez",
    "Person3": "Christopher Miller"
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
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Jordan Gonzalez",
    "Person3": "Cheryl Robinson"
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
    "Person3": "Jared David"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Jared David"
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
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Michael Orr"
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
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Jared David"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Jared David"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Jared David"
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
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel",
    "Person3": "Michael Orr"
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
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "Person3": "Joseph Williams"
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
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Cheryl Robinson"
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
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Andrew Diaz"
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
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Cheryl Robinson"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Cheryl Robinson"
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
    "Person3": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Andrew Diaz"
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
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Crystal Whitehead",
    "Person3": "Christopher Miller"
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
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Jeffrey Henderson",
    "Person3": "Eugene Green"
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
    "Person3": "April Wise"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "April Wise"
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
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "Michael Orr"
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
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "April Wise"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "April Wise"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "April Wise"
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
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "Person3": "Michael Orr"
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
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "David Lee",
    "Person3": "Joseph Williams"
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
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
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
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "Person3": "Jared David"
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
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "Person3": "Matthew Marshall"
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
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
  },
  {
    "Person1": "Mia Sutton",
    "Person2": "Stephanie Martin",
    "Person3": "Christopher Miller"
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
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
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
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "Person3": "Steve Newton"
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
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "Person3": "Tammy Patton"
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
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
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
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
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
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Thomas Schmidt",
    "Person3": "Brandi Bailey"
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
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "Person3": "Matthew Marshall"
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
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "Person3": "Angel Riggs"
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
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "Person3": "April Wise"
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
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey",
    "Person3": "Scott Walker"
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
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey",
    "Person3": "Scott Walker"
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
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Michael Robinson",
    "Person2": "Brandi Bailey",
    "Person3": "Scott Walker"
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
    "Person3": "Scott Walker"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "Person3": "Matthew Marshall"
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
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
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
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
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
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "Person3": "Eric Ortiz"
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
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
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
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
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
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
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
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "Person3": "Rachel Graham"
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
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
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
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
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
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
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
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "Person3": "Matthew Marshall"
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
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton",
    "Person3": "Dana Douglas"
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
    "Person3": "Tammy Ryan"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Tammy Ryan"
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
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Eric Ortiz"
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
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
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
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
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
    "Person3": "Tammy Ryan"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Tammy Ryan"
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
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Eric Ortiz"
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
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "Person3": "Dana Douglas"
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
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "Person3": "Eric Ortiz"
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
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
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
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
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
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson",
    "Person3": "Rachel Graham"
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
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
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
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
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
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "Person3": "Angel Riggs"
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
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
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
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
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
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz",
    "Person3": "Michael Orr"
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
- **Tokens Used:** 1,378
- **Execution Time:** 3.13s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
WITH p, s.degree AS degree, COUNT(*) AS degreeCount
RETURN degree, COUNT(p) AS peopleCount, SUM(degreeCount) AS totalDegrees
ORDER BY totalDegrees DESC
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
    "degree": "Bachelor",
    "peopleCount": 31,
    "totalDegrees": 32
  },
  {
    "degree": "PhD",
    "peopleCount": 3,
    "totalDegrees": 3
  },
  {
    "degree": "Master",
    "peopleCount": 1,
    "totalDegrees": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,368
- **Execution Time:** 3.02s
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
RETURN p.firstName, p.lastName, p.id
ORDER BY p.lastName, p.firstName
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
    "p.lastName": "Bailey",
    "p.id": "p30"
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "p.id": "p49"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall",
    "p.id": "p46"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 1,349
- **Execution Time:** 1.97s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 67: 68
**Status:** FAIL

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
RETURN DISTINCT p1.firstName AS name, 'First Name' AS type1, 'Last Name' AS type2
UNION
MATCH (p1:Person), (p2:Person)
WHERE toLower(p1.lastName) = toLower(p2.firstName)
RETURN DISTINCT p1.lastName AS name, 'Last Name' AS type1, 'First Name' AS type2
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
    "name": "David",
    "type1": "First Name",
    "type2": "Last Name"
  },
  {
    "name": "David",
    "type1": "Last Name",
    "type2": "First Name"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,399
- **Execution Time:** 3.06s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
- **Difficulty:** medium
- **Tokens Used:** 1,321
- **Execution Time:** 2.01s
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
- **Tokens Used:** 1,358
- **Execution Time:** 2.15s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 70: 71
**Status:** PASS

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
WHERE u.type IN ['University', 'College', 'Institute'] AND u.foundedYear < 1800
RETURN u.name, u.foundedYear
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
[
  {
    "u.name": "Port Nicoleshire Institute",
    "u.foundedYear": 1571
  },
  {
    "u.name": "Priceshire Institute",
    "u.foundedYear": 1619
  },
  {
    "u.name": "Castanedachester Institute",
    "u.foundedYear": 1730
  },
  {
    "u.name": "Smithstad University",
    "u.foundedYear": 1787
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,351
- **Execution Time:** 2.63s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
RETURN p1.firstName + ' ' + p1.lastName AS Person1, p2.firstName + ' ' + p2.lastName AS Person2, p1.birthDate AS SharedBirthday
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
- **Tokens Used:** 1,375
- **Execution Time:** 10.95s
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
RETURN j.title
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
    "j.title": "CTO"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,329
- **Execution Time:** 1.79s
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
RETURN f.name
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
    "f.name": "Medicine"
  },
  {
    "f.name": "Law"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,332
- **Execution Time:** 2.06s
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
MATCH (p:Person)-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'Current'
  AND toLower(split(p.email, '@')[1]) CONTAINS toLower(replace(c.name, ' ', ''))
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
- **Tokens Used:** 1,363
- **Execution Time:** 3.06s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 75: 76
**Status:** PASS

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
WHERE l.population > 1000000
RETURN l.name, l.population
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
[
  {
    "l.name": "Karenview",
    "l.population": 13126125
  },
  {
    "l.name": "Patricialand",
    "l.population": 12819117
  },
  {
    "l.name": "Stephaniemouth",
    "l.population": 11636146
  },
  {
    "l.name": "Perryborough",
    "l.population": 10639534
  },
  {
    "l.name": "Lake Michelle",
    "l.population": 9619364
  },
  {
    "l.name": "Simsview",
    "l.population": 9234763
  },
  {
    "l.name": "Lake Justinview",
    "l.population": 6060072
  },
  {
    "l.name": "East Patrick",
    "l.population": 4875083
  },
  {
    "l.name": "Rivasside",
    "l.population": 3376763
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,337
- **Execution Time:** 2.15s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 76: 77
**Status:** PASS

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
WHERE s.endYear = 2016 AND s.status = 'Graduated'
RETURN p.firstName + ' ' + p.lastName AS graduateName, e.name AS university
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
[
  {
    "graduateName": "Samuel Wagner",
    "university": "Priceshire Institute"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,354
- **Execution Time:** 3.27s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (husband:Person)-[:IS_HUSBAND]->(wife:Person)
WHERE husband.gender = 'Male' AND wife.gender = 'Female'
WITH husband, wife, 
     duration.between(date(husband.birthDate), date(wife.birthDate)).years AS ageDifference
RETURN husband.firstName + ' ' + husband.lastName AS husbandName,
       wife.firstName + ' ' + wife.lastName AS wifeName,
       abs(ageDifference) AS ageGap
ORDER BY ageGap DESC
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,413
- **Execution Time:** 3.51s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 78: 79
**Status:** PASS

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
WHERE s.endYear IS NOT NULL AND s.endYear - s.startYear > 4
RETURN p.firstName, p.lastName, e.name, s.startYear, s.endYear, s.endYear - s.startYear AS studyDuration
ORDER BY studyDuration DESC
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
[
  {
    "p.firstName": "Scott",
    "p.lastName": "Walker",
    "e.name": "Priceshire Institute",
    "s.startYear": 1960,
    "s.endYear": 1965,
    "studyDuration": 5
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "e.name": "Priceshire Institute",
    "s.startYear": 2014,
    "s.endYear": 2019,
    "studyDuration": 5
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "e.name": "Smithstad University",
    "s.startYear": 1974,
    "s.endYear": 1979,
    "studyDuration": 5
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,377
- **Execution Time:** 2.60s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p1:Person)-[f:IS_FRIEND]-(p2:Person)
WHERE p1 <> p2
MATCH (p1)-[w1:WORKED_AT]->(c1:Company)
MATCH (p2)-[w2:WORKED_AT]->(c2:Company)
WHERE c1 <> c2
  AND c1.industry = c2.industry
  AND w1.status = 'Current'
  AND w2.status = 'Current'
RETURN p1.firstName + ' ' + p1.lastName AS Person1,
       p2.firstName + ' ' + p2.lastName AS Person2,
       c1.name AS Company1,
       c2.name AS Company2,
       c1.industry AS Industry
LIMIT 10
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
[
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Vanessa Patel",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Vanessa Patel",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Vanessa Patel",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Vanessa Patel",
    "Company1": "Williams, Johnson and Wright",
    "Company2": "Hooper PLC",
    "Industry": "Education"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Anna Davis",
    "Company1": "Stuart, Higgins and Strickland",
    "Company2": "Patterson, Camacho and White",
    "Industry": "Technology"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Anna Davis",
    "Company1": "Stuart, Higgins and Strickland",
    "Company2": "Patterson, Camacho and White",
    "Industry": "Technology"
  },
  {
    "Person1": "April Wise",
    "Person2": "Annette Pearson",
    "Company1": "Stuart, Higgins and Strickland",
    "Company2": "Patterson, Camacho and White",
    "Industry": "Technology"
  },
  {
    "Person1": "April Wise",
    "Person2": "Annette Pearson",
    "Company1": "Stuart, Higgins and Strickland",
    "Company2": "Patterson, Camacho and White",
    "Industry": "Technology"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 1,425
- **Execution Time:** 4.91s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 80: 81
**Status:** PASS

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
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution),
      (p)-[w:WORKED_AT]->(c:Company)
WHERE w.startYear < s.endYear OR s.endYear IS NULL
RETURN DISTINCT p.firstName + ' ' + p.lastName AS name,
       e.name AS institution,
       s.startYear AS studyStartYear,
       s.endYear AS studyEndYear,
       c.name AS company,
       w.startYear AS workStartYear
ORDER BY name
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
[
  {
    "name": "Annette Pearson",
    "institution": "Priceshire Institute",
    "studyStartYear": 1995,
    "studyEndYear": 1999,
    "company": "Ruiz Ltd",
    "workStartYear": 1994
  },
  {
    "name": "Charles Taylor",
    "institution": "Priceshire Institute",
    "studyStartYear": 1953,
    "studyEndYear": 1957,
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1954
  },
  {
    "name": "Cheryl Robinson",
    "institution": "Smithstad University",
    "studyStartYear": 1971,
    "studyEndYear": 1975,
    "company": "Johnson-Rogers",
    "workStartYear": 1970
  },
  {
    "name": "Cheryl Robinson",
    "institution": "Smithstad University",
    "studyStartYear": 1974,
    "studyEndYear": 1979,
    "company": "Johnson-Rogers",
    "workStartYear": 1970
  },
  {
    "name": "Cheryl Robinson",
    "institution": "Smithstad University",
    "studyStartYear": 1974,
    "studyEndYear": 1979,
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1976
  },
  {
    "name": "Christopher Miller",
    "institution": "Castanedachester Institute",
    "studyStartYear": 1949,
    "studyEndYear": 1953,
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1948
  },
  {
    "name": "Connie Lawrence",
    "institution": "Castanedachester Institute",
    "studyStartYear": 1949,
    "studyEndYear": 1953,
    "company": "Rogers-Hobbs",
    "workStartYear": 1949
  },
  {
    "name": "Dana Douglas",
    "institution": "Priceshire Institute",
    "studyStartYear": 2014,
    "studyEndYear": 2019,
    "company": "Rogers-Hobbs",
    "workStartYear": 2012
  },
  {
    "name": "Dana Douglas",
    "institution": "Priceshire Institute",
    "studyStartYear": 2014,
    "studyEndYear": 2019,
    "company": "Ruiz Ltd",
    "workStartYear": 2016
  },
  {
    "name": "Dana Douglas",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 2019,
    "studyEndYear": 2021,
    "company": "Rogers-Hobbs",
    "workStartYear": 2012
  },
  {
    "name": "Dana Douglas",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 2019,
    "studyEndYear": 2021,
    "company": "Ruiz Ltd",
    "workStartYear": 2016
  },
  {
    "name": "Dana Douglas",
    "institution": "Castanedachester Institute",
    "studyStartYear": 2011,
    "studyEndYear": 2015,
    "company": "Rogers-Hobbs",
    "workStartYear": 2012
  },
  {
    "name": "David Lee",
    "institution": "Castanedachester Institute",
    "studyStartYear": 1968,
    "studyEndYear": 1972,
    "company": "Patterson, Camacho and White",
    "workStartYear": 1970
  },
  {
    "name": "Debra Clark",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 2000,
    "studyEndYear": 2004,
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 2001
  },
  {
    "name": "Donald Jones",
    "institution": "Smithstad University",
    "studyStartYear": 1987,
    "studyEndYear": 1991,
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1990
  },
  {
    "name": "Donald Jones",
    "institution": "Smithstad University",
    "studyStartYear": 1987,
    "studyEndYear": 1991,
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 1986
  },
  {
    "name": "Eric Ortiz",
    "institution": "Smithstad University",
    "studyStartYear": 1976,
    "studyEndYear": 1980,
    "company": "Johnson-Rogers",
    "workStartYear": 1978
  },
  {
    "name": "Eugene Green",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 2020,
    "studyEndYear": null,
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 2021
  },
  {
    "name": "Johnny Campos",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 1963,
    "studyEndYear": 1967,
    "company": "Ruiz Ltd",
    "workStartYear": 1961
  },
  {
    "name": "Johnny Campos",
    "institution": "Port Nicoleshire Institute",
    "studyStartYear": 1963,
    "studyEndYear": 1967,
    "company": "Ruiz Ltd",
    "workStartYear": 1966
  },
  {
    "name": "Mia Sutton",
    "institution": "South Jeffrey Institute",
    "studyStartYear": 1993,
    "studyEndYear": 1997,
    "company": "Ruiz Ltd",
    "workStartYear": 1995
  },
  {
    "name": "Samuel Wagner",
    "institution": "Priceshire Institute",
    "studyStartYear": 2012,
    "studyEndYear": 2016,
    "company": "Patterson, Camacho and White",
    "workStartYear": 2015
  },
  {
    "name": "Scott Walker",
    "institution": "Priceshire Institute",
    "studyStartYear": 1960,
    "studyEndYear": 1965,
    "company": "Rogers-Hobbs",
    "workStartYear": 1962
  },
  {
    "name": "Tammy Patton",
    "institution": "South Jeffrey Institute",
    "studyStartYear": 1952,
    "studyEndYear": 1956,
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1955
  },
  {
    "name": "Tammy Ryan",
    "institution": "Priceshire Institute",
    "studyStartYear": 1999,
    "studyEndYear": 2003,
    "company": "Patterson, Camacho and White",
    "workStartYear": 2002
  },
  {
    "name": "Theresa Vazquez",
    "institution": "South Jeffrey Institute",
    "studyStartYear": 1953,
    "studyEndYear": 1957,
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1956
  },
  {
    "name": "Thomas Schmidt",
    "institution": "South Jeffrey Institute",
    "studyStartYear": 1946,
    "studyEndYear": 1950,
    "company": "Rogers-Hobbs",
    "workStartYear": 1946
  },
  {
    "name": "Timothy Walls",
    "institution": "Smithstad University",
    "studyStartYear": 1980,
    "studyEndYear": 1984,
    "company": "Rogers-Hobbs",
    "workStartYear": 1982
  },
  {
    "name": "Todd Wilson",
    "institution": "South Jeffrey Institute",
    "studyStartYear": 2005,
    "studyEndYear": 2009,
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 2006
  },
  {
    "name": "Tracey Hickman",
    "institution": "Smithstad University",
    "studyStartYear": 2009,
    "studyEndYear": 2013,
    "company": "Patterson, Camacho and White",
    "workStartYear": 2009
  },
  {
    "name": "William Brady",
    "institution": "Priceshire Institute",
    "studyStartYear": 1980,
    "studyEndYear": 1984,
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1981
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,410
- **Execution Time:** 3.77s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WHERE s.endYear IS NOT NULL
WITH f, AVG(s.endYear - s.startYear) AS avgDuration
RETURN f.name AS fieldOfStudy, avgDuration
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
    "fieldOfStudy": "Law",
    "avgDuration": 3.888888888888889
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,364
- **Execution Time:** 3.23s
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
WHERE EXISTS((parent)-[:WORKED_AT]->(:Company)<-[:WORKED_AT]-(child))
  AND ANY(r1 IN [(parent)-[w1:WORKED_AT]->() | w1] WHERE r1.status = 'Current')
  AND ANY(r2 IN [(child)-[w2:WORKED_AT]->() | w2] WHERE r2.status = 'Current')
RETURN parent.firstName + ' ' + parent.lastName AS Parent,
       child.firstName + ' ' + child.lastName AS Child,
       [(parent)-[w:WORKED_AT]->(c:Company)<-[:WORKED_AT]-(child) | c.name][0] AS Company
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
[
  {
    "Parent": "Mark Johnson",
    "Child": "Connie Lawrence",
    "Company": "Rogers-Hobbs"
  },
  {
    "Parent": "Mark Johnson",
    "Child": "Mia Sutton",
    "Company": "Patterson, Camacho and White"
  },
  {
    "Parent": "Mark Johnson",
    "Child": "Charles Taylor",
    "Company": "Johnson-Rogers"
  },
  {
    "Parent": "Kevin Johnson",
    "Child": "Connie Lawrence",
    "Company": "Rogers-Hobbs"
  },
  {
    "Parent": "Kevin Johnson",
    "Child": "Mia Sutton",
    "Company": "Ruiz Ltd"
  },
  {
    "Parent": "Kevin Johnson",
    "Child": "Charles Taylor",
    "Company": "Johnson-Rogers"
  },
  {
    "Parent": "Connie Lawrence",
    "Child": "Juan Calderon",
    "Company": "Hooper PLC"
  },
  {
    "Parent": "Anna Davis",
    "Child": "Juan Calderon",
    "Company": "Johnson-Rogers"
  },
  {
    "Parent": "Mia Sutton",
    "Child": "Debra Clark",
    "Company": "Ruiz Ltd"
  },
  {
    "Parent": "Johnny Campos",
    "Child": "Joseph Maddox",
    "Company": "Ruiz Ltd"
  },
  {
    "Parent": "Joseph Maddox",
    "Child": "Jordan Gonzalez",
    "Company": "Rogers-Hobbs"
  },
  {
    "Parent": "Jessica Chavez",
    "Child": "Jordan Gonzalez",
    "Company": "Patterson, Camacho and White"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 1,434
- **Execution Time:** 5.26s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
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
MATCH (p1)-[s1:STUDIED_AT]->(uni:EducationalInstitution)<-[s2:STUDIED_AT]-(p2)
WHERE s1.degree IS NOT NULL AND s2.degree IS NOT NULL
RETURN DISTINCT p1.firstName + ' ' + p1.lastName AS Ancestor,
       p2.firstName + ' ' + p2.lastName AS Descendant,
       uni.name AS University,
       s1.degree AS AncestorDegree,
       s2.degree AS DescendantDegree
ORDER BY uni.name, Ancestor, Descendant
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
    "Ancestor": "Kevin Johnson",
    "Descendant": "Mia Sutton",
    "University": "South Jeffrey Institute",
    "AncestorDegree": "Bachelor",
    "DescendantDegree": "Bachelor"
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 1,435
- **Execution Time:** 4.81s
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
MATCH (p:Person)-[:LIVES_IN]->(currentLocation:Location)
WHERE p.birthPlace <> currentLocation.name
WITH p, currentLocation
MATCH (p)-[:LIVED_IN]->(foreignLocation:Location)
WHERE foreignLocation.country <> p.nationality
WITH p, currentLocation, foreignLocation
MATCH (p)-[:LIVED_IN]->(returnLocation:Location)
WHERE returnLocation.country = p.nationality
  AND returnLocation.name <> p.birthPlace
  AND returnLocation.name = currentLocation.name
RETURN p.id, p.firstName, p.lastName, p.birthPlace, 
       foreignLocation.name AS foreignCountry, 
       returnLocation.name AS returnedTo
ORDER BY p.lastName, p.firstName
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
- **Tokens Used:** 1,478
- **Execution Time:** 4.23s
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
MATCH (p)-[s2:STUDIED_AT]->(e2:EducationalInstitution)
WHERE s1.startYear < s2.endYear AND s2.startYear < s1.endYear
  AND id(e1) < id(e2)
  AND (s1.endYear IS NULL OR s2.endYear IS NULL OR s1.endYear > s2.startYear)
  AND (s2.endYear IS NULL OR s1.endYear IS NULL OR s2.endYear > s1.startYear)
RETURN p.firstName + ' ' + p.lastName AS PersonName,
       e1.name AS Institution1, s1.startYear AS Start1, s1.endYear AS End1, s1.degree AS Degree1,
       e2.name AS Institution2, s2.startYear AS Start2, s2.endYear AS End2, s2.degree AS Degree2
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
    "Start1": 2014,
    "End1": 2019,
    "Degree1": "PhD",
    "Institution2": "Castanedachester Institute",
    "Start2": 2011,
    "End2": 2015,
    "Degree2": "Bachelor"
  },
  {
    "PersonName": "Mia Sutton",
    "Institution1": "Castanedachester Institute",
    "Start1": 1991,
    "End1": 1995,
    "Degree1": "Bachelor",
    "Institution2": "South Jeffrey Institute",
    "Start2": 1993,
    "End2": 1997,
    "Degree2": "Bachelor"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 1,482
- **Execution Time:** 5.07s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 86: 87
**Status:** PASS

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
MATCH (p:Person)
WHERE NOT EXISTS {
    MATCH (p)-[:LIVED_IN]->(:Location)
}
AND EXISTS {
    MATCH (p)-[:LIVES_IN]->(:Location)
}
RETURN p.firstName, p.lastName, p.birthPlace
```

#### Results Comparison

**Expected Results:**
```json
[
  {
    "p.firstName": "Anna"
  },
  {
    "p.firstName": "Mia"
  },
  {
    "p.firstName": "Michael"
  },
  {
    "p.firstName": "Jessica"
  },
  {
    "p.firstName": "Jordan"
  },
  {
    "p.firstName": "David"
  },
  {
    "p.firstName": "Nathaniel"
  },
  {
    "p.firstName": "Jeffrey"
  },
  {
    "p.firstName": "Cheryl"
  },
  {
    "p.firstName": "Jared"
  },
  {
    "p.firstName": "Timothy"
  },
  {
    "p.firstName": "Brandi"
  },
  {
    "p.firstName": "Logan"
  },
  {
    "p.firstName": "William"
  },
  {
    "p.firstName": "Donald"
  },
  {
    "p.firstName": "Rachel"
  },
  {
    "p.firstName": "Matthew"
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
    "p.firstName": "Anna",
    "p.lastName": "Davis",
    "p.birthPlace": "Cassandraton"
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "p.birthPlace": "New Cynthiaside"
  },
  {
    "p.firstName": "Michael",
    "p.lastName": "Robinson",
    "p.birthPlace": "Meganton"
  },
  {
    "p.firstName": "Jessica",
    "p.lastName": "Chavez",
    "p.birthPlace": "Teresaburgh"
  },
  {
    "p.firstName": "Jordan",
    "p.lastName": "Gonzalez",
    "p.birthPlace": "Kathrynside"
  },
  {
    "p.firstName": "David",
    "p.lastName": "Brown",
    "p.birthPlace": "New Angelashire"
  },
  {
    "p.firstName": "Nathaniel",
    "p.lastName": "Khan",
    "p.birthPlace": "Sanchezfort"
  },
  {
    "p.firstName": "Jeffrey",
    "p.lastName": "Henderson",
    "p.birthPlace": "Shieldston"
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "p.birthPlace": "New Jillton"
  },
  {
    "p.firstName": "Jared",
    "p.lastName": "David",
    "p.birthPlace": "New Brooke"
  },
  {
    "p.firstName": "Timothy",
    "p.lastName": "Walls",
    "p.birthPlace": "South Christineshire"
  },
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey",
    "p.birthPlace": "East Mikeburgh"
  },
  {
    "p.firstName": "Logan",
    "p.lastName": "Archer",
    "p.birthPlace": "Lake Lisaport"
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "p.birthPlace": "Port Francisco"
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "p.birthPlace": "Michaelhaven"
  },
  {
    "p.firstName": "Rachel",
    "p.lastName": "Graham",
    "p.birthPlace": "South Rachelborough"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall",
    "p.birthPlace": "Lowehaven"
  },
  {
    "p.firstName": "Angel",
    "p.lastName": "Riggs",
    "p.birthPlace": "South Robertshire"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,354
- **Execution Time:** 2.93s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WITH c, c.employees AS employeeCount
ORDER BY employeeCount ASC
LIMIT 1
RETURN c.name AS CompanyWithSmallestEmployeeCount, employeeCount
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
    "CompanyWithSmallestEmployeeCount": "Ruiz Ltd",
    "employeeCount": 92460
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,350
- **Execution Time:** 2.58s
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
WHERE toLower(p.email) ENDS WITH '@gmail.com'
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
- **Tokens Used:** 1,328
- **Execution Time:** 1.72s
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
- **Execution Time:** 1.55s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 90: 91
**Status:** PASS

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
WHERE NOT EXISTS {
    MATCH (p)-[w:WORKED_AT]->(c:Company)
    WHERE w.status = 'Current'
}
AND NOT EXISTS {
    MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
    WHERE h.endYear IS NULL
}
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
    "unemployedPerson": "Michael Robinson"
  },
  {
    "unemployedPerson": "Jared David"
  },
  {
    "unemployedPerson": "Brandi Bailey"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,374
- **Execution Time:** 2.87s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 91: 92
**Status:** PASS

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
MATCH (f:FieldOfStudy)<-[s:STUDIED]-(p:Person)
WHERE s.status = 'Current'
RETURN f.name AS fieldOfStudy, COUNT(p) AS studentCount
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,353
- **Execution Time:** 2.02s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WHERE p1 <> p2 AND toInteger(left(p1.birthDate, 3) + '0') = toInteger(left(p2.birthDate, 3) + '0')
RETURN p1.firstName + ' ' + p1.lastName AS Person1, p1.birthDate AS BirthDate1,
       p2.firstName + ' ' + p2.lastName AS Person2, p2.birthDate AS BirthDate2
ORDER BY p1.birthDate, p2.birthDate
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
    "BirthDate1": "1926-01-22",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Andrew Diaz",
    "BirthDate1": "1926-01-22",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Andrew Diaz",
    "BirthDate1": "1926-01-22",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Andrew Diaz",
    "BirthDate1": "1926-01-22",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Andrew Diaz",
    "BirthDate1": "1926-01-22",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Andrew Diaz",
    "BirthDate1": "1926-01-22",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Thomas Schmidt",
    "BirthDate1": "1926-04-29",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Crystal Whitehead",
    "BirthDate1": "1927-11-20",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Jordan Gonzalez",
    "BirthDate1": "1927-12-04",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Mark Johnson",
    "BirthDate1": "1928-06-16",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Connie Lawrence",
    "BirthDate1": "1929-01-23",
    "Person2": "Kevin Johnson",
    "BirthDate2": "1929-11-07"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Andrew Diaz",
    "BirthDate2": "1926-01-22"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Thomas Schmidt",
    "BirthDate2": "1926-04-29"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Crystal Whitehead",
    "BirthDate2": "1927-11-20"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Jordan Gonzalez",
    "BirthDate2": "1927-12-04"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Mark Johnson",
    "BirthDate2": "1928-06-16"
  },
  {
    "Person1": "Kevin Johnson",
    "BirthDate1": "1929-11-07",
    "Person2": "Connie Lawrence",
    "BirthDate2": "1929-01-23"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Michael Orr",
    "BirthDate1": "1930-11-03",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Christopher Miller",
    "BirthDate1": "1930-12-01",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Anna Davis",
    "BirthDate1": "1931-09-23",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Angel Riggs",
    "BirthDate1": "1932-02-17",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Rachel Graham",
    "BirthDate1": "1932-12-20",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Theresa Vazquez",
    "BirthDate1": "1933-03-03",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Tammy Patton",
    "BirthDate1": "1933-08-17",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Charles Taylor",
    "BirthDate1": "1934-01-16",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Stephanie Martin",
    "BirthDate1": "1934-09-13",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Savannah Delacruz",
    "BirthDate1": "1935-02-12",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Jeffrey Henderson",
    "BirthDate1": "1935-09-02",
    "Person2": "Scott Walker",
    "BirthDate2": "1937-05-09"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Michael Orr",
    "BirthDate2": "1930-11-03"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Christopher Miller",
    "BirthDate2": "1930-12-01"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Anna Davis",
    "BirthDate2": "1931-09-23"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Angel Riggs",
    "BirthDate2": "1932-02-17"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Rachel Graham",
    "BirthDate2": "1932-12-20"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Theresa Vazquez",
    "BirthDate2": "1933-03-03"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Tammy Patton",
    "BirthDate2": "1933-08-17"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Charles Taylor",
    "BirthDate2": "1934-01-16"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Stephanie Martin",
    "BirthDate2": "1934-09-13"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Savannah Delacruz",
    "BirthDate2": "1935-02-12"
  },
  {
    "Person1": "Scott Walker",
    "BirthDate1": "1937-05-09",
    "Person2": "Jeffrey Henderson",
    "BirthDate2": "1935-09-02"
  },
  {
    "Person1": "Joseph Williams",
    "BirthDate1": "1942-12-06",
    "Person2": "Johnny Campos",
    "BirthDate2": "1943-03-10"
  },
  {
    "Person1": "Joseph Williams",
    "BirthDate1": "1942-12-06",
    "Person2": "Logan Archer",
    "BirthDate2": "1945-06-15"
  },
  {
    "Person1": "Joseph Williams",
    "BirthDate1": "1942-12-06",
    "Person2": "Matthew Marshall",
    "BirthDate2": "1945-06-20"
  },
  {
    "Person1": "Joseph Williams",
    "BirthDate1": "1942-12-06",
    "Person2": "Juan Calderon",
    "BirthDate2": "1948-05-13"
  },
  {
    "Person1": "Joseph Williams",
    "BirthDate1": "1942-12-06",
    "Person2": "David Lee",
    "BirthDate2": "1949-04-30"
  },
  {
    "Person1": "Johnny Campos",
    "BirthDate1": "1943-03-10",
    "Person2": "Joseph Williams",
    "BirthDate2": "1942-12-06"
  },
  {
    "Person1": "Johnny Campos",
    "BirthDate1": "1943-03-10",
    "Person2": "Logan Archer",
    "BirthDate2": "1945-06-15"
  },
  {
    "Person1": "Johnny Campos",
    "BirthDate1": "1943-03-10",
    "Person2": "Matthew Marshall",
    "BirthDate2": "1945-06-20"
  },
  {
    "Person1": "Johnny Campos",
    "BirthDate1": "1943-03-10",
    "Person2": "Juan Calderon",
    "BirthDate2": "1948-05-13"
  },
  {
    "Person1": "Johnny Campos",
    "BirthDate1": "1943-03-10",
    "Person2": "David Lee",
    "BirthDate2": "1949-04-30"
  },
  {
    "Person1": "Logan Archer",
    "BirthDate1": "1945-06-15",
    "Person2": "Joseph Williams",
    "BirthDate2": "1942-12-06"
  },
  {
    "Person1": "Logan Archer",
    "BirthDate1": "1945-06-15",
    "Person2": "Johnny Campos",
    "BirthDate2": "1943-03-10"
  },
  {
    "Person1": "Logan Archer",
    "BirthDate1": "1945-06-15",
    "Person2": "Matthew Marshall",
    "BirthDate2": "1945-06-20"
  },
  {
    "Person1": "Logan Archer",
    "BirthDate1": "1945-06-15",
    "Person2": "Juan Calderon",
    "BirthDate2": "1948-05-13"
  },
  {
    "Person1": "Logan Archer",
    "BirthDate1": "1945-06-15",
    "Person2": "David Lee",
    "BirthDate2": "1949-04-30"
  },
  {
    "Person1": "Matthew Marshall",
    "BirthDate1": "1945-06-20",
    "Person2": "Joseph Williams",
    "BirthDate2": "1942-12-06"
  },
  {
    "Person1": "Matthew Marshall",
    "BirthDate1": "1945-06-20",
    "Person2": "Johnny Campos",
    "BirthDate2": "1943-03-10"
  },
  {
    "Person1": "Matthew Marshall",
    "BirthDate1": "1945-06-20",
    "Person2": "Logan Archer",
    "BirthDate2": "1945-06-15"
  },
  {
    "Person1": "Matthew Marshall",
    "BirthDate1": "1945-06-20",
    "Person2": "Juan Calderon",
    "BirthDate2": "1948-05-13"
  },
  {
    "Person1": "Matthew Marshall",
    "BirthDate1": "1945-06-20",
    "Person2": "David Lee",
    "BirthDate2": "1949-04-30"
  },
  {
    "Person1": "Juan Calderon",
    "BirthDate1": "1948-05-13",
    "Person2": "Joseph Williams",
    "BirthDate2": "1942-12-06"
  },
  {
    "Person1": "Juan Calderon",
    "BirthDate1": "1948-05-13",
    "Person2": "Johnny Campos",
    "BirthDate2": "1943-03-10"
  },
  {
    "Person1": "Juan Calderon",
    "BirthDate1": "1948-05-13",
    "Person2": "Logan Archer",
    "BirthDate2": "1945-06-15"
  },
  {
    "Person1": "Juan Calderon",
    "BirthDate1": "1948-05-13",
    "Person2": "Matthew Marshall",
    "BirthDate2": "1945-06-20"
  },
  {
    "Person1": "Juan Calderon",
    "BirthDate1": "1948-05-13",
    "Person2": "David Lee",
    "BirthDate2": "1949-04-30"
  },
  {
    "Person1": "David Lee",
    "BirthDate1": "1949-04-30",
    "Person2": "Joseph Williams",
    "BirthDate2": "1942-12-06"
  },
  {
    "Person1": "David Lee",
    "BirthDate1": "1949-04-30",
    "Person2": "Johnny Campos",
    "BirthDate2": "1943-03-10"
  },
  {
    "Person1": "David Lee",
    "BirthDate1": "1949-04-30",
    "Person2": "Logan Archer",
    "BirthDate2": "1945-06-15"
  },
  {
    "Person1": "David Lee",
    "BirthDate1": "1949-04-30",
    "Person2": "Matthew Marshall",
    "BirthDate2": "1945-06-20"
  },
  {
    "Person1": "David Lee",
    "BirthDate1": "1949-04-30",
    "Person2": "Juan Calderon",
    "BirthDate2": "1948-05-13"
  },
  {
    "Person1": "Cheryl Robinson",
    "BirthDate1": "1951-09-03",
    "Person2": "Jessica Chavez",
    "BirthDate2": "1951-11-13"
  },
  {
    "Person1": "Cheryl Robinson",
    "BirthDate1": "1951-09-03",
    "Person2": "Eric Ortiz",
    "BirthDate2": "1956-04-25"
  },
  {
    "Person1": "Cheryl Robinson",
    "BirthDate1": "1951-09-03",
    "Person2": "David Brown",
    "BirthDate2": "1957-03-25"
  },
  {
    "Person1": "Jessica Chavez",
    "BirthDate1": "1951-11-13",
    "Person2": "Cheryl Robinson",
    "BirthDate2": "1951-09-03"
  },
  {
    "Person1": "Jessica Chavez",
    "BirthDate1": "1951-11-13",
    "Person2": "Eric Ortiz",
    "BirthDate2": "1956-04-25"
  },
  {
    "Person1": "Jessica Chavez",
    "BirthDate1": "1951-11-13",
    "Person2": "David Brown",
    "BirthDate2": "1957-03-25"
  },
  {
    "Person1": "Eric Ortiz",
    "BirthDate1": "1956-04-25",
    "Person2": "Cheryl Robinson",
    "BirthDate2": "1951-09-03"
  },
  {
    "Person1": "Eric Ortiz",
    "BirthDate1": "1956-04-25",
    "Person2": "Jessica Chavez",
    "BirthDate2": "1951-11-13"
  },
  {
    "Person1": "Eric Ortiz",
    "BirthDate1": "1956-04-25",
    "Person2": "David Brown",
    "BirthDate2": "1957-03-25"
  },
  {
    "Person1": "David Brown",
    "BirthDate1": "1957-03-25",
    "Person2": "Cheryl Robinson",
    "BirthDate2": "1951-09-03"
  },
  {
    "Person1": "David Brown",
    "BirthDate1": "1957-03-25",
    "Person2": "Jessica Chavez",
    "BirthDate2": "1951-11-13"
  },
  {
    "Person1": "David Brown",
    "BirthDate1": "1957-03-25",
    "Person2": "Eric Ortiz",
    "BirthDate2": "1956-04-25"
  },
  {
    "Person1": "Timothy Walls",
    "BirthDate1": "1961-10-25",
    "Person2": "William Brady",
    "BirthDate2": "1961-11-17"
  },
  {
    "Person1": "Timothy Walls",
    "BirthDate1": "1961-10-25",
    "Person2": "Joseph Maddox",
    "BirthDate2": "1964-04-28"
  },
  {
    "Person1": "Timothy Walls",
    "BirthDate1": "1961-10-25",
    "Person2": "Nathaniel Khan",
    "BirthDate2": "1967-04-08"
  },
  {
    "Person1": "Timothy Walls",
    "BirthDate1": "1961-10-25",
    "Person2": "Donald Jones",
    "BirthDate2": "1968-05-05"
  },
  {
    "Person1": "Timothy Walls",
    "BirthDate1": "1961-10-25",
    "Person2": "Vanessa Patel",
    "BirthDate2": "1969-12-03"
  },
  {
    "Person1": "William Brady",
    "BirthDate1": "1961-11-17",
    "Person2": "Timothy Walls",
    "BirthDate2": "1961-10-25"
  },
  {
    "Person1": "William Brady",
    "BirthDate1": "1961-11-17",
    "Person2": "Joseph Maddox",
    "BirthDate2": "1964-04-28"
  },
  {
    "Person1": "William Brady",
    "BirthDate1": "1961-11-17",
    "Person2": "Nathaniel Khan",
    "BirthDate2": "1967-04-08"
  },
  {
    "Person1": "William Brady",
    "BirthDate1": "1961-11-17",
    "Person2": "Donald Jones",
    "BirthDate2": "1968-05-05"
  },
  {
    "Person1": "William Brady",
    "BirthDate1": "1961-11-17",
    "Person2": "Vanessa Patel",
    "BirthDate2": "1969-12-03"
  },
  {
    "Person1": "Joseph Maddox",
    "BirthDate1": "1964-04-28",
    "Person2": "Timothy Walls",
    "BirthDate2": "1961-10-25"
  },
  {
    "Person1": "Joseph Maddox",
    "BirthDate1": "1964-04-28",
    "Person2": "William Brady",
    "BirthDate2": "1961-11-17"
  },
  {
    "Person1": "Joseph Maddox",
    "BirthDate1": "1964-04-28",
    "Person2": "Nathaniel Khan",
    "BirthDate2": "1967-04-08"
  },
  {
    "Person1": "Joseph Maddox",
    "BirthDate1": "1964-04-28",
    "Person2": "Donald Jones",
    "BirthDate2": "1968-05-05"
  },
  {
    "Person1": "Joseph Maddox",
    "BirthDate1": "1964-04-28",
    "Person2": "Vanessa Patel",
    "BirthDate2": "1969-12-03"
  },
  {
    "Person1": "Nathaniel Khan",
    "BirthDate1": "1967-04-08",
    "Person2": "Timothy Walls",
    "BirthDate2": "1961-10-25"
  },
  {
    "Person1": "Nathaniel Khan",
    "BirthDate1": "1967-04-08",
    "Person2": "William Brady",
    "BirthDate2": "1961-11-17"
  },
  {
    "Person1": "Nathaniel Khan",
    "BirthDate1": "1967-04-08",
    "Person2": "Joseph Maddox",
    "BirthDate2": "1964-04-28"
  },
  {
    "Person1": "Nathaniel Khan",
    "BirthDate1": "1967-04-08",
    "Person2": "Donald Jones",
    "BirthDate2": "1968-05-05"
  },
  {
    "Person1": "Nathaniel Khan",
    "BirthDate1": "1967-04-08",
    "Person2": "Vanessa Patel",
    "BirthDate2": "1969-12-03"
  },
  {
    "Person1": "Donald Jones",
    "BirthDate1": "1968-05-05",
    "Person2": "Timothy Walls",
    "BirthDate2": "1961-10-25"
  },
  {
    "Person1": "Donald Jones",
    "BirthDate1": "1968-05-05",
    "Person2": "William Brady",
    "BirthDate2": "1961-11-17"
  },
  {
    "Person1": "Donald Jones",
    "BirthDate1": "1968-05-05",
    "Person2": "Joseph Maddox",
    "BirthDate2": "1964-04-28"
  },
  {
    "Person1": "Donald Jones",
    "BirthDate1": "1968-05-05",
    "Person2": "Nathaniel Khan",
    "BirthDate2": "1967-04-08"
  },
  {
    "Person1": "Donald Jones",
    "BirthDate1": "1968-05-05",
    "Person2": "Vanessa Patel",
    "BirthDate2": "1969-12-03"
  },
  {
    "Person1": "Vanessa Patel",
    "BirthDate1": "1969-12-03",
    "Person2": "Timothy Walls",
    "BirthDate2": "1961-10-25"
  },
  {
    "Person1": "Vanessa Patel",
    "BirthDate1": "1969-12-03",
    "Person2": "William Brady",
    "BirthDate2": "1961-11-17"
  },
  {
    "Person1": "Vanessa Patel",
    "BirthDate1": "1969-12-03",
    "Person2": "Joseph Maddox",
    "BirthDate2": "1964-04-28"
  },
  {
    "Person1": "Vanessa Patel",
    "BirthDate1": "1969-12-03",
    "Person2": "Nathaniel Khan",
    "BirthDate2": "1967-04-08"
  },
  {
    "Person1": "Vanessa Patel",
    "BirthDate1": "1969-12-03",
    "Person2": "Donald Jones",
    "BirthDate2": "1968-05-05"
  },
  {
    "Person1": "Mia Sutton",
    "BirthDate1": "1972-02-14",
    "Person2": "Annette Pearson",
    "BirthDate2": "1976-07-18"
  },
  {
    "Person1": "Mia Sutton",
    "BirthDate1": "1972-02-14",
    "Person2": "Tammy Ryan",
    "BirthDate2": "1979-06-01"
  },
  {
    "Person1": "Annette Pearson",
    "BirthDate1": "1976-07-18",
    "Person2": "Mia Sutton",
    "BirthDate2": "1972-02-14"
  },
  {
    "Person1": "Annette Pearson",
    "BirthDate1": "1976-07-18",
    "Person2": "Tammy Ryan",
    "BirthDate2": "1979-06-01"
  },
  {
    "Person1": "Tammy Ryan",
    "BirthDate1": "1979-06-01",
    "Person2": "Mia Sutton",
    "BirthDate2": "1972-02-14"
  },
  {
    "Person1": "Tammy Ryan",
    "BirthDate1": "1979-06-01",
    "Person2": "Annette Pearson",
    "BirthDate2": "1976-07-18"
  },
  {
    "Person1": "Debra Clark",
    "BirthDate1": "1982-07-31",
    "Person2": "Todd Wilson",
    "BirthDate2": "1987-01-29"
  },
  {
    "Person1": "Todd Wilson",
    "BirthDate1": "1987-01-29",
    "Person2": "Debra Clark",
    "BirthDate2": "1982-07-31"
  },
  {
    "Person1": "Tracey Hickman",
    "BirthDate1": "1991-06-25",
    "Person2": "Tanya Koch",
    "BirthDate2": "1992-10-03"
  },
  {
    "Person1": "Tracey Hickman",
    "BirthDate1": "1991-06-25",
    "Person2": "Dana Douglas",
    "BirthDate2": "1993-07-14"
  },
  {
    "Person1": "Tracey Hickman",
    "BirthDate1": "1991-06-25",
    "Person2": "Samuel Wagner",
    "BirthDate2": "1994-01-03"
  },
  {
    "Person1": "Tracey Hickman",
    "BirthDate1": "1991-06-25",
    "Person2": "April Wise",
    "BirthDate2": "1995-10-25"
  },
  {
    "Person1": "Tracey Hickman",
    "BirthDate1": "1991-06-25",
    "Person2": "Steve Newton",
    "BirthDate2": "1999-02-19"
  },
  {
    "Person1": "Tanya Koch",
    "BirthDate1": "1992-10-03",
    "Person2": "Tracey Hickman",
    "BirthDate2": "1991-06-25"
  },
  {
    "Person1": "Tanya Koch",
    "BirthDate1": "1992-10-03",
    "Person2": "Dana Douglas",
    "BirthDate2": "1993-07-14"
  },
  {
    "Person1": "Tanya Koch",
    "BirthDate1": "1992-10-03",
    "Person2": "Samuel Wagner",
    "BirthDate2": "1994-01-03"
  },
  {
    "Person1": "Tanya Koch",
    "BirthDate1": "1992-10-03",
    "Person2": "April Wise",
    "BirthDate2": "1995-10-25"
  },
  {
    "Person1": "Tanya Koch",
    "BirthDate1": "1992-10-03",
    "Person2": "Steve Newton",
    "BirthDate2": "1999-02-19"
  },
  {
    "Person1": "Dana Douglas",
    "BirthDate1": "1993-07-14",
    "Person2": "Tracey Hickman",
    "BirthDate2": "1991-06-25"
  },
  {
    "Person1": "Dana Douglas",
    "BirthDate1": "1993-07-14",
    "Person2": "Tanya Koch",
    "BirthDate2": "1992-10-03"
  },
  {
    "Person1": "Dana Douglas",
    "BirthDate1": "1993-07-14",
    "Person2": "Samuel Wagner",
    "BirthDate2": "1994-01-03"
  },
  {
    "Person1": "Dana Douglas",
    "BirthDate1": "1993-07-14",
    "Person2": "April Wise",
    "BirthDate2": "1995-10-25"
  },
  {
    "Person1": "Dana Douglas",
    "BirthDate1": "1993-07-14",
    "Person2": "Steve Newton",
    "BirthDate2": "1999-02-19"
  },
  {
    "Person1": "Samuel Wagner",
    "BirthDate1": "1994-01-03",
    "Person2": "Tracey Hickman",
    "BirthDate2": "1991-06-25"
  },
  {
    "Person1": "Samuel Wagner",
    "BirthDate1": "1994-01-03",
    "Person2": "Tanya Koch",
    "BirthDate2": "1992-10-03"
  },
  {
    "Person1": "Samuel Wagner",
    "BirthDate1": "1994-01-03",
    "Person2": "Dana Douglas",
    "BirthDate2": "1993-07-14"
  },
  {
    "Person1": "Samuel Wagner",
    "BirthDate1": "1994-01-03",
    "Person2": "April Wise",
    "BirthDate2": "1995-10-25"
  },
  {
    "Person1": "Samuel Wagner",
    "BirthDate1": "1994-01-03",
    "Person2": "Steve Newton",
    "BirthDate2": "1999-02-19"
  },
  {
    "Person1": "April Wise",
    "BirthDate1": "1995-10-25",
    "Person2": "Tracey Hickman",
    "BirthDate2": "1991-06-25"
  },
  {
    "Person1": "April Wise",
    "BirthDate1": "1995-10-25",
    "Person2": "Tanya Koch",
    "BirthDate2": "1992-10-03"
  },
  {
    "Person1": "April Wise",
    "BirthDate1": "1995-10-25",
    "Person2": "Dana Douglas",
    "BirthDate2": "1993-07-14"
  },
  {
    "Person1": "April Wise",
    "BirthDate1": "1995-10-25",
    "Person2": "Samuel Wagner",
    "BirthDate2": "1994-01-03"
  },
  {
    "Person1": "April Wise",
    "BirthDate1": "1995-10-25",
    "Person2": "Steve Newton",
    "BirthDate2": "1999-02-19"
  },
  {
    "Person1": "Steve Newton",
    "BirthDate1": "1999-02-19",
    "Person2": "Tracey Hickman",
    "BirthDate2": "1991-06-25"
  },
  {
    "Person1": "Steve Newton",
    "BirthDate1": "1999-02-19",
    "Person2": "Tanya Koch",
    "BirthDate2": "1992-10-03"
  },
  {
    "Person1": "Steve Newton",
    "BirthDate1": "1999-02-19",
    "Person2": "Dana Douglas",
    "BirthDate2": "1993-07-14"
  },
  {
    "Person1": "Steve Newton",
    "BirthDate1": "1999-02-19",
    "Person2": "Samuel Wagner",
    "BirthDate2": "1994-01-03"
  },
  {
    "Person1": "Steve Newton",
    "BirthDate1": "1999-02-19",
    "Person2": "April Wise",
    "BirthDate2": "1995-10-25"
  },
  {
    "Person1": "Michael Robinson",
    "BirthDate1": "2000-03-19",
    "Person2": "Brandi Bailey",
    "BirthDate2": "2000-07-21"
  },
  {
    "Person1": "Michael Robinson",
    "BirthDate1": "2000-03-19",
    "Person2": "Eugene Green",
    "BirthDate2": "2001-12-06"
  },
  {
    "Person1": "Michael Robinson",
    "BirthDate1": "2000-03-19",
    "Person2": "Jared David",
    "BirthDate2": "2005-07-04"
  },
  {
    "Person1": "Brandi Bailey",
    "BirthDate1": "2000-07-21",
    "Person2": "Michael Robinson",
    "BirthDate2": "2000-03-19"
  },
  {
    "Person1": "Brandi Bailey",
    "BirthDate1": "2000-07-21",
    "Person2": "Eugene Green",
    "BirthDate2": "2001-12-06"
  },
  {
    "Person1": "Brandi Bailey",
    "BirthDate1": "2000-07-21",
    "Person2": "Jared David",
    "BirthDate2": "2005-07-04"
  },
  {
    "Person1": "Eugene Green",
    "BirthDate1": "2001-12-06",
    "Person2": "Michael Robinson",
    "BirthDate2": "2000-03-19"
  },
  {
    "Person1": "Eugene Green",
    "BirthDate1": "2001-12-06",
    "Person2": "Brandi Bailey",
    "BirthDate2": "2000-07-21"
  },
  {
    "Person1": "Eugene Green",
    "BirthDate1": "2001-12-06",
    "Person2": "Jared David",
    "BirthDate2": "2005-07-04"
  },
  {
    "Person1": "Jared David",
    "BirthDate1": "2005-07-04",
    "Person2": "Michael Robinson",
    "BirthDate2": "2000-03-19"
  },
  {
    "Person1": "Jared David",
    "BirthDate1": "2005-07-04",
    "Person2": "Brandi Bailey",
    "BirthDate2": "2000-07-21"
  },
  {
    "Person1": "Jared David",
    "BirthDate1": "2005-07-04",
    "Person2": "Eugene Green",
    "BirthDate2": "2001-12-06"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 1,389
- **Execution Time:** 3.58s
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
    "CityName": "Stephaniemouth",
    "Country": "New Zealand",
    "Population": 11636146
  },
  {
    "CityName": "Rivasside",
    "Country": "Kiribati",
    "Population": 3376763
  },
  {
    "CityName": "Lake Michelle",
    "Country": "Korea",
    "Population": 9619364
  },
  {
    "CityName": "Karenview",
    "Country": "Seychelles",
    "Population": 13126125
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
    "CityName": "Patricialand",
    "Country": "Burundi",
    "Population": 12819117
  },
  {
    "CityName": "East Patrick",
    "Country": "Cape Verde",
    "Population": 4875083
  },
  {
    "CityName": "North Robert",
    "Country": "Greenland",
    "Population": 530926
  },
  {
    "CityName": "Perryborough",
    "Country": "Syrian Arab Republic",
    "Population": 10639534
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,339
- **Execution Time:** 1.69s
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
RETURN c.name AS CompanyName, c.foundedYear AS FoundedYear, c.industry AS Industry
ORDER BY c.foundedYear DESC
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
    "CompanyName": "Stuart, Higgins and Strickland",
    "FoundedYear": 2018,
    "Industry": "Technology"
  },
  {
    "CompanyName": "Hooper PLC",
    "FoundedYear": 2005,
    "Industry": "Education"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,348
- **Execution Time:** 2.19s
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
- **Tokens Used:** 1,353
- **Execution Time:** 1.99s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 96: 97
**Status:** PASS

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
MATCH (p1:Person)-[f:IS_FRIEND]-(p2:Person)
WHERE id(p1) < id(p2)
WITH p1, p2
OPTIONAL MATCH (p1)-[l1:LIVES_IN|LIVED_IN]->(loc:Location)
WITH p1, p2, collect(l1) AS p1Locations
OPTIONAL MATCH (p2)-[l2:LIVES_IN|LIVED_IN]->(loc:Location)
WITH p1, p2, p1Locations, collect(l2) AS p2Locations
WHERE NONE(l1 IN p1Locations WHERE ANY(l2 IN p2Locations WHERE
  l1.since <= CASE WHEN l2.endYear IS NULL THEN date() ELSE date(toString(l2.endYear) + '-12-31') END AND
  CASE WHEN l1.endYear IS NULL THEN date() ELSE date(toString(l1.endYear) + '-12-31') END >= l2.since
))
RETURN p1.firstName + ' ' + p1.lastName AS Friend1, p2.firstName + ' ' + p2.lastName AS Friend2
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,481
- **Execution Time:** 5.56s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
- **Tokens Used:** 1,341
- **Execution Time:** 2.67s
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
WITH count(DISTINCT p1) AS duplicateCount
RETURN duplicateCount
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
    "duplicateCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,363
- **Execution Time:** 2.28s
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
- **Tokens Used:** 1,331
- **Execution Time:** 2.34s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---
