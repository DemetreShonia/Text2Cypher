# Evaluation Report: Detailed + Retrieval

**Run Time:** 2025-07-04 20:35:29

## Summary Metrics

- **Total Cases:** 99
- **Overall Accuracy:** 54.55%
- **Syntactic Correctness:** 80.81%
- **Execution Success:** 71.72%
- **Total Tokens:** 232,053

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
- **Tokens Used:** 1,439
- **Execution Time:** 9.92s
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
WITH p.gender AS gender, COUNT(p) AS count
ORDER BY count DESC
LIMIT 1
RETURN gender AS moreCommonGender, count AS genderCount
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
    "moreCommonGender": "Male",
    "genderCount": 30
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,379
- **Execution Time:** 5.33s
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
MATCH (p:Person {firstName: 'Mark', lastName: 'Johnson'})
RETURN p.nationality AS Nationality
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
    "Nationality": "British"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 6,174
- **Execution Time:** 6.84s
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
- **Tokens Used:** 2,503
- **Execution Time:** 7.08s
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
WHERE l.type = 'City'
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
- **Tokens Used:** 1,540
- **Execution Time:** 6.47s
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
MATCH (jordan:Person {firstName: 'Jordan', lastName: 'Gonzalez'})<-[:IS_PARENT]-(parent:Person)
WHERE parent.gender = 'Male'
RETURN parent.firstName + ' ' + parent.lastName AS daddy
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
    "daddy": "Joseph Maddox"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,740
- **Execution Time:** 7.77s
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
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle {title: 'Data Scientist'})
WHERE h.companyId = c.id AND h.endYear IS NULL
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
- **Tokens Used:** 1,420
- **Execution Time:** 9.31s
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
MATCH (p:Person {firstName: 'Mark', lastName: 'Johnson'})-[w:WORKED_AT]->(c:Company)
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
- **Tokens Used:** 3,186
- **Execution Time:** 5.16s
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
WHERE toLower(p.firstName) = 'mark'
  AND c.industry = 'Technology'
  AND toLower(c.headquarters) CONTAINS 'spain'
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
- **Tokens Used:** 1,384
- **Execution Time:** 6.55s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
MATCH (p:Person)-[:IS_PARENT]->(c:Person)
WHERE toLower(p.nationality) = 'new zealand'
WITH c.firstName AS girlName, COUNT(*) AS nameCount
WHERE toLower(c.gender) = 'female'
RETURN girlName, nameCount
ORDER BY nameCount DESC
LIMIT 1
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: In a WITH/RETURN with DISTINCT or an aggregation, it is not possible to access variables declared before the WITH/RETURN: c (line 4, column 15 (offset: 153))
"WHERE toLower(c.gender) = 'female'"
               ^}
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
- **Tokens Used:** 1,476
- **Execution Time:** 6.80s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
MATCH (p:Person)-[:LIVES_IN]->(loc:Location {country: 'New Zealand'})
WHERE toLower(p.firstName) = 'mia'
AND (p)-[:HAD_POSITION]->(:JobTitle {title: 'Doctor'})
RETURN count(DISTINCT p) AS doctorsNamedMiaInNewZealand
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
    "doctorsNamedMiaInNewZealand": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,514
- **Execution Time:** 6.21s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.TypeError} {message: No such field: years}
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

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
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
- **Tokens Used:** 1,412
- **Execution Time:** 6.84s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 14: 14
**Status:** PASS

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
MATCH (f:FieldOfStudy)<-[s:STUDIED]-(p:Person)-[st:STUDIED_AT]->(e:EducationalInstitution)
WHERE toLower(e.country) = 'yemen'
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
[
  {
    "mostPopularSubject": "Business Administration",
    "studentCount": 3
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 1,438
- **Execution Time:** 6.44s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
RETURN count(DISTINCT p) AS numberOfPeople
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
    "numberOfPeople": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 7,965
- **Execution Time:** 6.24s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'OVER': expected an expression, 'FOREACH', ',', 'AS', 'ORDER BY', 'CALL', 'CREATE', 'LOAD CSV', 'DELETE', 'DETACH', 'FINISH', 'INSERT', 'LIMIT', 'MATCH', 'MERGE', 'NODETACH', 'OFFSET', 'OPTIONAL', 'REMOVE', 'RETURN', 'SET', 'SKIP', 'UNION', 'UNWIND', 'USE', 'WITH' or <EOF> (line 7, column 26 (offset: 162))
"       avg(l.population) OVER () AS averagePopulation"
                          ^}
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

- **Category:** aggregation
- **Difficulty:** easy
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
MATCH (l:Location)<-[r:LIVES_IN]-(p:Person)
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
- **Tokens Used:** 4,441
- **Execution Time:** 5.70s
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
WITH e, COUNT(p) AS studentCount
ORDER BY studentCount DESC
LIMIT 1
RETURN e.name AS MostPopularInstitution, studentCount
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
    "MostPopularInstitution": "Smithstad University",
    "studentCount": 10
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 4,628
- **Execution Time:** 5.12s
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
MATCH (l:Location {name: 'Stephaniemouth', country: 'New Zealand'})
WITH l, l.population AS current_population
MATCH (p:Person)-[r:LIVED_IN|LIVES_IN]->(l)
WHERE (r.startYear IS NOT NULL AND r.startYear >= (date().year - 100)) OR
      (r.since IS NOT NULL AND date(r.since) >= date().subtract(duration('P100Y')))
WITH l, current_population, MIN(CASE
    WHEN r.startYear IS NOT NULL THEN r.startYear
    ELSE date(r.since).year
END) AS earliest_year
RETURN current_population - (current_population / (date().year - earliest_year + 1) * 100) AS population_increase
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '(': expected an expression or ')' (line 5, column 64 (offset: 292))
"      (r.since IS NOT NULL AND date(r.since) >= date().subtract(duration('P100Y')))"
                                                                ^}
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
- **Tokens Used:** 2,925
- **Execution Time:** 8.28s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
WITH p, date() AS currentDate
RETURN avg(duration.between(date(p.birthDate), currentDate).years) AS averageAge
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
- **Tokens Used:** 1,378
- **Execution Time:** 8.02s
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
WITH studiedAbroadAndStayed, count(p) AS totalPopulation
RETURN 
  CASE 
    WHEN toFloat(studiedAbroadAndStayed) / totalPopulation > 0.5 
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
- **Tokens Used:** 1,501
- **Execution Time:** 8.27s
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
    WHEN totalStudiedAbroad > 0 THEN 
      CASE 
        WHEN (studiedAbroadAndReturned * 1.0 / totalStudiedAbroad) > 0.5 
        THEN true 
        ELSE false 
      END
    ELSE null
  END AS isCorrelated
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
    "isCorrelated": false
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,525
- **Execution Time:** 9.92s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 23: 23
**Status:** FAIL

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
MATCH (p:Person)-[s:STUDIED_AT]->(e:EducationalInstitution)
WHERE e.country <> p.nationality
WITH p, e
MATCH (p)-[l:LIVED_IN]->(loc:Location)
WHERE l.startYear > s.endYear AND loc.country <> e.country AND loc.country <> p.nationality
WITH COUNT(DISTINCT p) AS studiedAbroadAndMoved
MATCH (p:Person)
WITH studiedAbroadAndMoved, COUNT(p) AS totalPopulation
RETURN 
  CASE 
    WHEN toFloat(studiedAbroadAndMoved) / totalPopulation > 0.5 
    THEN 'There is a correlation between studying abroad and changing countries again' 
    ELSE 'There is no correlation between studying abroad and changing countries again' 
  END AS result
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Variable `s` not defined (line 5, column 21 (offset: 162))
"WHERE l.startYear > s.endYear AND loc.country <> e.country AND loc.country <> p.nationality"
                     ^}
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,515
- **Execution Time:** 10.99s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
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
     (p)-[:WORKED_AT*1..3]->(c:Company) AS companies
WITH p, lowerEmail, collect(DISTINCT c.industry) AS industries
WHERE any(industry IN industries WHERE toLower(industry) = 'technology')
WITH count(p) AS techWorkers,
     sum(CASE WHEN lowerEmail CONTAINS 'yahoo.com' THEN 1 ELSE 0 END) AS yahooTechWorkers
MATCH (p:Person)
WITH p, toLower(p.email) AS lowerEmail, techWorkers, yahooTechWorkers,
     (p)-[:WORKED_AT*1..3]->(c:Company) AS companies
WITH p, lowerEmail, techWorkers, yahooTechWorkers, collect(DISTINCT c.industry) AS industries
WHERE NOT any(industry IN industries WHERE toLower(industry) = 'technology')
WITH techWorkers, yahooTechWorkers,
     count(p) AS nonTechWorkers,
     sum(CASE WHEN lowerEmail CONTAINS 'yahoo.com' THEN 1 ELSE 0 END) AS yahooNonTechWorkers
RETURN 
  (yahooNonTechWorkers / toFloat(nonTechWorkers) > 0.5 AND yahooTechWorkers / toFloat(techWorkers) <= 0.5) AS isCorrelated,
  yahooTechWorkers, techWorkers, yahooNonTechWorkers, nonTechWorkers
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'c'. (line 3, column 30 (offset: 87))
"     (p)-[:WORKED_AT*1..3]->(c:Company) AS companies"
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
- **Tokens Used:** 6,619
- **Execution Time:** 11.60s
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
MATCH (p:Person)
WHERE toLower(p.firstName) = 'charles'
WITH p, size([(p)-[:IS_SIBLING]-(sibling:Person) WHERE sibling.gender = 'Female' | sibling]) AS sisterCount
RETURN avg(sisterCount) AS averageSisterCount
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
    "averageSisterCount": 4.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,404
- **Execution Time:** 7.70s
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
MATCH (c:Person {firstName: 'Christopher'})-[f:IS_FRIEND]-(j:Person {firstName: 'Jessica'})
WHERE toLower(c.firstName) = 'christopher' AND toLower(j.firstName) = 'jessica'
RETURN count(DISTINCT c) as christophersWithJessicaFriend
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
    "christophersWithJessicaFriend": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 7,378
- **Execution Time:** 7.28s
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
WHERE EXISTS((p)-[:WORKED_AT]->(:Company))
WITH p, f, s
MATCH (p)-[w:WORKED_AT]->(c:Company)
WHERE w.status = 'Current'
WITH p, f, c
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WHERE h.companyId = c.id AND h.endYear IS NULL
WITH p, f, j
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
- **Tokens Used:** 2,705
- **Execution Time:** 7.98s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 28: 28
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'count': expected an expression (line 12, column 59 (offset: 663))
"RETURN emailType, count, toFloat(count) / toFloat((SELECT count(*) FROM (MATCH (p:Person) RETURN p))) * 100 AS percentage"
                                                           ^}
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

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)-[:LOCATED_IN]->(c:Country)
WHERE toLower(p.firstName) = 'jordan'
WITH c.name AS country, COUNT(p) AS count
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,385
- **Execution Time:** 7.26s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
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
MATCH (connie:Person)-[:IS_SIBLING]-(sister:Person)
WHERE toLower(connie.firstName) = 'connie'
MATCH (sister)-[worked:WORKED_AT]->(company:Company)
MATCH (sister)-[position:HAD_POSITION]->(jobTitle:JobTitle)
WHERE position.companyId = company.id
RETURN DISTINCT jobTitle.title AS Position
ORDER BY Position
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
    "Position": "CTO"
  },
  {
    "Position": "Data Scientist"
  },
  {
    "Position": "Director"
  },
  {
    "Position": "Doctor"
  },
  {
    "Position": "Lawyer"
  },
  {
    "Position": "Manager"
  },
  {
    "Position": "Professor"
  },
  {
    "Position": "Teacher"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 8,436
- **Execution Time:** 8.49s
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
WHERE EXISTS((p)-[:LIVES_IN]->(:Location {name: 'Grenada'}))
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
- **Tokens Used:** 1,381
- **Execution Time:** 5.19s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `e` not defined (line 6, column 21 (offset: 242))
"WITH DISTINCT p, f, e, c"
                     ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
MATCH (p:Person)-[:WORKED_AT]->(c:Company {industry: 'Education'})
MATCH (p)-[:IS_HUSBAND|IS_WIFE]->(spouse:Person)-[:LIVES_IN]->(l:Location {name: 'Grenada'})
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
- **Tokens Used:** 1,394
- **Execution Time:** 6.74s
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
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)
MATCH (p)-[:STUDIED]->(f:FieldOfStudy)
MATCH (p)-[w:WORKED_AT]->(c:Company)
MATCH (p)-[h:HAD_POSITION]->(j:JobTitle)
WITH p, f, c, j,
     toLower(f.name) AS studyField,
     toLower(c.industry) AS workIndustry,
     toLower(j.category) AS jobCategory
WITH p,
     CASE
         WHEN studyField CONTAINS workIndustry OR
              studyField CONTAINS jobCategory OR
              workIndustry CONTAINS studyField OR
              jobCategory CONTAINS studyField
         THEN 1
         ELSE 0
     END AS isCorrelated
WITH sum(isCorrelated) AS correlatedCount, count(p) AS totalCount
RETURN 
    CASE 
        WHEN toFloat(correlatedCount) / totalCount > 0.5 
        THEN 'Education and career are correlated'
        ELSE 'Education and career are not correlated'
    END AS result
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
    "result": "Education and career are not correlated"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 10,102
- **Execution Time:** 11.51s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
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
- **Execution Time:** 7.20s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 36: 36
**Status:** PASS

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
MATCH path = (matthew)-[:IS_FRIEND*1..10]-(person:Person)
WHERE all(r IN relationships(path) WHERE type(r) = 'IS_FRIEND')
WITH DISTINCT person
RETURN COUNT(DISTINCT person) = COUNT(person) AS allConnected
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
[
  {
    "allConnected": true
  }
]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 4,826
- **Execution Time:** 6.53s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.DatabaseError.Statement.ExecutionFailed} {message: The shortest path algorithm does not work when the start and end nodes are the same. This can happen if you
perform a shortestPath search after a cartesian product that might have the same start and end nodes for some
of the rows passed to shortestPath. If you would rather not experience this exception, and can accept the
possibility of missing results for those rows, disable this in the Neo4j configuration by setting
`dbms.cypher.forbid_shortestpath_common_nodes` to false. If you cannot accept missing results, and really want the
shortestPath between two common nodes, then re-write the query using a standard Cypher variable length pattern
expression followed by ordering by path length and limiting to one result.}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
WITH p, COUNT(DISTINCT w) AS jobCount, c.country AS country
WHERE country IS NOT NULL
WITH country, AVG(jobCount) AS avgJobs
RETURN country, round(avgJobs, 2) AS averageJobsPerPerson
ORDER BY averageJobsPerPerson DESC
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 2,326
- **Execution Time:** 7.76s
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
RETURN DISTINCT m.firstName, m.lastName, w.firstName AS wife_firstName, w.birthDate AS wife_birthDate, s.firstName AS sister_firstName, s.birthDate AS sister_birthDate
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
- **Tokens Used:** 1,421
- **Execution Time:** 6.63s
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
MATCH (loc:Location)<-[l:LIVES_IN]-(p:Person)
WITH loc, 
     COUNT(CASE WHEN p.gender = 'Male' THEN 1 END) AS maleCount,
     COUNT(CASE WHEN p.gender = 'Female' THEN 1 END) AS femaleCount
WHERE maleCount > femaleCount
RETURN loc.name AS Location, maleCount, femaleCount
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
- **Tokens Used:** 4,394
- **Execution Time:** 7.94s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 41: 41
**Status:** FAIL

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
MATCH (l:Location)<-[r:LIVES_IN]-(:Person)
WITH l, COUNT(CASE WHEN r.gender = 'Male' THEN 1 END) AS menCount,
     COUNT(CASE WHEN r.gender = 'Female' THEN 1 END) AS womenCount
WHERE menCount > womenCount
RETURN l.name AS location, menCount, womenCount, l.population AS totalPopulation
ORDER BY menCount DESC
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
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 2,537
- **Execution Time:** 7.39s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 42: 42
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `s` not defined (line 10, column 35 (offset: 364))
"RETURN e, foreignStudentCount, p, s"
                                   ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
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
MATCH (edu:EducationalInstitution)<-[:STUDIED_AT]-(student:Person)
WHERE student.nationality <> edu.country
WITH edu, COUNT(DISTINCT student) AS foreignStudentCount
ORDER BY foreignStudentCount DESC
LIMIT 5
RETURN edu.name AS educationInstitution, foreignStudentCount
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
    "educationInstitution": "Smithstad University",
    "foreignStudentCount": 9
  },
  {
    "educationInstitution": "South Jeffrey Institute",
    "foreignStudentCount": 8
  },
  {
    "educationInstitution": "Priceshire Institute",
    "foreignStudentCount": 7
  },
  {
    "educationInstitution": "Castanedachester Institute",
    "foreignStudentCount": 6
  },
  {
    "educationInstitution": "Port Nicoleshire Institute",
    "foreignStudentCount": 5
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 2,503
- **Execution Time:** 6.79s
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
RETURN w.firstName + ' ' + w.lastName AS Wife, w.birthDate AS WifeBirthDate,
       h.firstName + ' ' + h.lastName AS Husband, h.birthDate AS HusbandBirthDate
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
    "WifeBirthDate": "1934-01-16",
    "Husband": "Johnny Campos",
    "HusbandBirthDate": "1943-03-10"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** easy
- **Tokens Used:** 1,602
- **Execution Time:** 5.78s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 45: 45
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '|': expected an expression, ',' or ']' (line 10, column 70 (offset: 483))
"       [(oldestMarriedPerson.person)-[r:IS_HUSBAND|IS_WIFE]-(spouse) | spouse.firstName + ' ' + spouse.lastName] AS spouseName"
                                                                      ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
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
MATCH (p:Person)
WHERE NOT (p)-[:IS_CHILD]->()
WITH p
MATCH path = (p)-[:IS_PARENT*0..10]->(descendant:Person)
WITH p, COLLECT(DISTINCT descendant) + p AS familyMembers
WHERE ALL(member IN familyMembers WHERE (member)-[:WORKED_AT]->(:Company))
RETURN p.firstName + ' ' + p.lastName AS FamilyRoot, 
       SIZE(familyMembers) AS FamilySize, 
       COLLECT(DISTINCT member.firstName + ' ' + member.lastName) AS WorkingFamilyMembers
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Variable `member` not defined (line 9, column 25 (offset: 365))
"       COLLECT(DISTINCT member.firstName + ' ' + member.lastName) AS WorkingFamilyMembers"
                         ^}
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
- **Tokens Used:** 8,833
- **Execution Time:** 8.78s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
    (p)-[:IS_HUSBAND|IS_WIFE|IS_PARENT|IS_CHILD|IS_SIBLING|IS_FRIEND|STUDIED_AT|STUDIED|WORKED_AT|HAD_POSITION|LIVES_IN|LIVED_IN]-()
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
- **Tokens Used:** 1,371
- **Execution Time:** 7.07s
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
- **Execution Time:** 6.88s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 49: 49
**Status:** PASS

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
     size([(p)-[:IS_SIBLING]-() | 1]) AS siblingCount,
     size([(p)-[:IS_CHILD]->()-[:IS_SIBLING]-()-[:IS_PARENT]->() | 1]) AS cousinCount
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
    "name": "Juan Calderon",
    "cousinCount": 4,
    "siblingCount": 0
  },
  {
    "name": "Debra Clark",
    "cousinCount": 4,
    "siblingCount": 0
  },
  {
    "name": "Joseph Maddox",
    "cousinCount": 4,
    "siblingCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,403
- **Execution Time:** 7.26s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.TypeError} {message: Expected a string value for `toLower`, but got: Long(1991); consider converting it to a string with toString().}
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

- **Category:** paradox
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
- **Tokens Used:** 5,059
- **Execution Time:** 6.64s
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
WITH p, child, p.birthDate AS birthDate
ORDER BY birthDate DESC
RETURN p.firstName + ' ' + p.lastName AS youngestParent, p.birthDate AS birthDate
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
- **Tokens Used:** 6,751
- **Execution Time:** 7.07s
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
MATCH (p)-[lived:LIVED_IN]->(l:Location)
WITH p, collect(l.name) AS lived_locations, total_locations
MATCH (p)-[lives:LIVES_IN]->(current:Location)
RETURN p.firstName + ' ' + p.lastName AS most_traveled_person,
       total_locations AS number_of_locations,
       lived_locations + [current.name] AS locations_lived
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
- **Tokens Used:** 3,826
- **Execution Time:** 6.68s
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
- **Tokens Used:** 5,143
- **Execution Time:** 5.29s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 55: 55
**Status:** PASS

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
WHERE size([(p)-[lived:LIVED_IN]->(l:Location) | lived]) = 3
AND (p)-[:LIVES_IN]->(:Location)
RETURN p.id, p.firstName, p.lastName
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
[
  {
    "p.id": "p3",
    "p.firstName": "Connie",
    "p.lastName": "Lawrence"
  },
  {
    "p.id": "p10",
    "p.firstName": "Charles",
    "p.lastName": "Taylor"
  },
  {
    "p.id": "p11",
    "p.firstName": "Johnny",
    "p.lastName": "Campos"
  },
  {
    "p.id": "p16",
    "p.firstName": "Vanessa",
    "p.lastName": "Patel"
  },
  {
    "p.id": "p19",
    "p.firstName": "Crystal",
    "p.lastName": "Whitehead"
  },
  {
    "p.id": "p24",
    "p.firstName": "Stephanie",
    "p.lastName": "Martin"
  },
  {
    "p.id": "p26",
    "p.firstName": "Thomas",
    "p.lastName": "Schmidt"
  },
  {
    "p.id": "p28",
    "p.firstName": "Eugene",
    "p.lastName": "Green"
  },
  {
    "p.id": "p32",
    "p.firstName": "Steve",
    "p.lastName": "Newton"
  },
  {
    "p.id": "p43",
    "p.firstName": "Tammy",
    "p.lastName": "Ryan"
  },
  {
    "p.id": "p44",
    "p.firstName": "Eric",
    "p.lastName": "Ortiz"
  },
  {
    "p.id": "p49",
    "p.firstName": "Dana",
    "p.lastName": "Douglas"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 2,235
- **Execution Time:** 6.89s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WHERE p1.id < p2.id
RETURN p1.firstName + ' ' + p1.lastName AS Person1, p2.firstName + ' ' + p2.lastName AS Person2, f.since AS FriendshipDate
ORDER BY f.since DESC
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
    "Person1": "Connie Lawrence",
    "Person2": "Michael Orr",
    "FriendshipDate": "2023-12-24"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Michael Orr",
    "FriendshipDate": "2023-12-24"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2023-12-21"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2023-12-21"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2023-10-17"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2023-10-17"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2023-09-21"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2023-09-21"
  },
  {
    "Person1": "April Wise",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2023-09-05"
  },
  {
    "Person1": "April Wise",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2023-09-05"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Donald Jones",
    "FriendshipDate": "2023-08-04"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Donald Jones",
    "FriendshipDate": "2023-08-04"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2023-07-04"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2023-07-04"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "FriendshipDate": "2023-03-06"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Brandi Bailey",
    "FriendshipDate": "2023-03-06"
  },
  {
    "Person1": "April Wise",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2023-03-05"
  },
  {
    "Person1": "April Wise",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2023-03-05"
  },
  {
    "Person1": "David Lee",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2022-12-18"
  },
  {
    "Person1": "David Lee",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2022-12-18"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2022-12-18"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2022-12-18"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2022-12-04"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2022-12-04"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2022-11-07"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2022-11-07"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2022-11-04"
  },
  {
    "Person1": "Anna Davis",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2022-11-04"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2022-10-02"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2022-10-02"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "David Brown",
    "FriendshipDate": "2022-08-31"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "David Brown",
    "FriendshipDate": "2022-08-31"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2022-08-19"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2022-08-19"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Jared David",
    "FriendshipDate": "2022-07-21"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Jared David",
    "FriendshipDate": "2022-07-21"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2022-07-17"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2022-07-17"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2022-07-09"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2022-07-09"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2022-07-02"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2022-07-02"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Anna Davis",
    "FriendshipDate": "2022-06-14"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Anna Davis",
    "FriendshipDate": "2022-06-14"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2022-06-02"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2022-06-02"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "FriendshipDate": "2022-05-05"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox",
    "FriendshipDate": "2022-05-05"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2022-03-18"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2022-03-18"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "FriendshipDate": "2022-01-29"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "David Lee",
    "FriendshipDate": "2022-01-29"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2021-12-14"
  },
  {
    "Person1": "Donald Jones",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2021-12-14"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Tracey Hickman",
    "FriendshipDate": "2021-11-29"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Tracey Hickman",
    "FriendshipDate": "2021-11-29"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2021-10-21"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2021-10-21"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2021-09-13"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2021-09-13"
  },
  {
    "Person1": "David Lee",
    "Person2": "April Wise",
    "FriendshipDate": "2021-07-15"
  },
  {
    "Person1": "David Lee",
    "Person2": "April Wise",
    "FriendshipDate": "2021-07-15"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "FriendshipDate": "2021-06-25"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Donald Jones",
    "FriendshipDate": "2021-06-25"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Anna Davis",
    "FriendshipDate": "2021-06-13"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Anna Davis",
    "FriendshipDate": "2021-06-13"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2021-06-01"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2021-06-01"
  },
  {
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2021-05-25"
  },
  {
    "Person1": "William Brady",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2021-05-25"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "FriendshipDate": "2021-03-22"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Annette Pearson",
    "FriendshipDate": "2021-03-22"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Debra Clark",
    "FriendshipDate": "2021-02-17"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Debra Clark",
    "FriendshipDate": "2021-02-17"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2021-01-08"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2021-01-08"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez",
    "FriendshipDate": "2020-12-28"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Jessica Chavez",
    "FriendshipDate": "2020-12-28"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2020-12-26"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2020-12-26"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2020-11-01"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2020-11-01"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "FriendshipDate": "2020-09-13"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Jared David",
    "FriendshipDate": "2020-09-13"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2020-08-28"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2020-08-28"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2020-08-11"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2020-08-11"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2020-08-02"
  },
  {
    "Person1": "Matthew Marshall",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2020-08-02"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "William Brady",
    "FriendshipDate": "2020-06-21"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "William Brady",
    "FriendshipDate": "2020-06-21"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2020-06-11"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2020-06-11"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Donald Jones",
    "FriendshipDate": "2020-05-15"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Donald Jones",
    "FriendshipDate": "2020-05-15"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Logan Archer",
    "FriendshipDate": "2020-05-11"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Logan Archer",
    "FriendshipDate": "2020-05-11"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Anna Davis",
    "FriendshipDate": "2020-04-26"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Anna Davis",
    "FriendshipDate": "2020-04-26"
  },
  {
    "Person1": "David Lee",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2020-04-06"
  },
  {
    "Person1": "David Lee",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2020-04-06"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2020-04-03"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2020-04-03"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Orr",
    "FriendshipDate": "2020-03-30"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Orr",
    "FriendshipDate": "2020-03-30"
  },
  {
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt",
    "FriendshipDate": "2020-02-15"
  },
  {
    "Person1": "David Brown",
    "Person2": "Thomas Schmidt",
    "FriendshipDate": "2020-02-15"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jeffrey Henderson",
    "FriendshipDate": "2020-02-12"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jeffrey Henderson",
    "FriendshipDate": "2020-02-12"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Michael Orr",
    "FriendshipDate": "2020-01-23"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Michael Orr",
    "FriendshipDate": "2020-01-23"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2019-12-31"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2019-12-31"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Eugene Green",
    "FriendshipDate": "2019-11-08"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Eugene Green",
    "FriendshipDate": "2019-11-08"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Scott Walker",
    "FriendshipDate": "2019-11-06"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Scott Walker",
    "FriendshipDate": "2019-11-06"
  },
  {
    "Person1": "April Wise",
    "Person2": "William Brady",
    "FriendshipDate": "2019-10-20"
  },
  {
    "Person1": "April Wise",
    "Person2": "William Brady",
    "FriendshipDate": "2019-10-20"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
    "FriendshipDate": "2019-10-10"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker",
    "FriendshipDate": "2019-10-10"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Michael Orr",
    "FriendshipDate": "2019-08-10"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Michael Orr",
    "FriendshipDate": "2019-08-10"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2019-08-08"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2019-08-08"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2019-07-10"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2019-07-10"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2019-06-15"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2019-06-15"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2019-05-16"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2019-05-16"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2019-04-11"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2019-04-11"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "April Wise",
    "FriendshipDate": "2019-04-08"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "April Wise",
    "FriendshipDate": "2019-04-08"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2019-04-04"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2019-04-04"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Timothy Walls",
    "FriendshipDate": "2019-03-01"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Timothy Walls",
    "FriendshipDate": "2019-03-01"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2019-02-19"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2019-02-19"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "FriendshipDate": "2019-02-05"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Anna Davis",
    "FriendshipDate": "2019-02-05"
  },
  {
    "Person1": "William Brady",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2019-01-28"
  },
  {
    "Person1": "William Brady",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2019-01-28"
  },
  {
    "Person1": "David Brown",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2018-12-27"
  },
  {
    "Person1": "David Brown",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2018-12-27"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2018-12-18"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2018-12-18"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2018-12-10"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2018-12-10"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2018-12-07"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2018-12-07"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2018-11-03"
  },
  {
    "Person1": "Jeffrey Henderson",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2018-11-03"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Debra Clark",
    "FriendshipDate": "2018-10-28"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Debra Clark",
    "FriendshipDate": "2018-10-28"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2018-07-03"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2018-07-03"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Logan Archer",
    "FriendshipDate": "2018-06-15"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Logan Archer",
    "FriendshipDate": "2018-06-15"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2018-06-03"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2018-06-03"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2018-05-28"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2018-05-28"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Anna Davis",
    "FriendshipDate": "2018-04-24"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Anna Davis",
    "FriendshipDate": "2018-04-24"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2018-03-14"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2018-03-14"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "April Wise",
    "FriendshipDate": "2017-12-31"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "April Wise",
    "FriendshipDate": "2017-12-31"
  },
  {
    "Person1": "Jared David",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2017-12-14"
  },
  {
    "Person1": "Jared David",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2017-12-14"
  },
  {
    "Person1": "David Brown",
    "Person2": "Brandi Bailey",
    "FriendshipDate": "2017-12-03"
  },
  {
    "Person1": "David Brown",
    "Person2": "Brandi Bailey",
    "FriendshipDate": "2017-12-03"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2017-11-08"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2017-11-08"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2017-11-03"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2017-11-03"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2017-10-27"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2017-10-27"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2017-10-27"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2017-10-27"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2017-09-27"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2017-09-27"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2017-09-27"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Rachel Graham",
    "FriendshipDate": "2017-09-27"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Debra Clark",
    "FriendshipDate": "2017-09-16"
  },
  {
    "Person1": "Joseph Williams",
    "Person2": "Debra Clark",
    "FriendshipDate": "2017-09-16"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Jared David",
    "FriendshipDate": "2017-09-09"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Jared David",
    "FriendshipDate": "2017-09-09"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jared David",
    "FriendshipDate": "2017-08-30"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Jared David",
    "FriendshipDate": "2017-08-30"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2017-03-17"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2017-03-17"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2017-02-18"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2017-02-18"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Anna Davis",
    "FriendshipDate": "2016-11-11"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Anna Davis",
    "FriendshipDate": "2016-11-11"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2016-11-04"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Samuel Wagner",
    "FriendshipDate": "2016-11-04"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "FriendshipDate": "2016-09-15"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "William Brady",
    "FriendshipDate": "2016-09-15"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2016-08-31"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2016-08-31"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "William Brady",
    "FriendshipDate": "2016-07-12"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "William Brady",
    "FriendshipDate": "2016-07-12"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "FriendshipDate": "2016-07-04"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "April Wise",
    "FriendshipDate": "2016-07-04"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "FriendshipDate": "2016-07-02"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson",
    "FriendshipDate": "2016-07-02"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2016-06-23"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2016-06-23"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2016-05-15"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2016-05-15"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2016-05-14"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2016-05-14"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2016-05-10"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2016-05-10"
  },
  {
    "Person1": "Jared David",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2016-04-28"
  },
  {
    "Person1": "Jared David",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2016-04-28"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2016-04-24"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2016-04-24"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2016-02-14"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Savannah Delacruz",
    "FriendshipDate": "2016-02-14"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "FriendshipDate": "2016-02-12"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox",
    "FriendshipDate": "2016-02-12"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2015-11-16"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2015-11-16"
  },
  {
    "Person1": "David Brown",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2015-10-24"
  },
  {
    "Person1": "David Brown",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2015-10-24"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Anna Davis",
    "FriendshipDate": "2015-07-06"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Anna Davis",
    "FriendshipDate": "2015-07-06"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2015-05-14"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2015-05-14"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Debra Clark",
    "FriendshipDate": "2015-04-06"
  },
  {
    "Person1": "Todd Wilson",
    "Person2": "Debra Clark",
    "FriendshipDate": "2015-04-06"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "FriendshipDate": "2015-02-06"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Thomas Schmidt",
    "FriendshipDate": "2015-02-06"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Steve Newton",
    "FriendshipDate": "2014-11-23"
  },
  {
    "Person1": "Cheryl Robinson",
    "Person2": "Steve Newton",
    "FriendshipDate": "2014-11-23"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-11-18"
  },
  {
    "Person1": "Angel Riggs",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-11-18"
  },
  {
    "Person1": "Jared David",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2014-10-13"
  },
  {
    "Person1": "Jared David",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2014-10-13"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2014-10-04"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton",
    "FriendshipDate": "2014-10-04"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2014-09-21"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2014-09-21"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-09-11"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-09-11"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Michael Orr",
    "FriendshipDate": "2014-08-09"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Michael Orr",
    "FriendshipDate": "2014-08-09"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2014-07-25"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2014-07-25"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Jared David",
    "FriendshipDate": "2014-06-27"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Jared David",
    "FriendshipDate": "2014-06-27"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2014-06-22"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2014-06-22"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2014-06-02"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2014-06-02"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2014-03-26"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2014-03-26"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2014-03-06"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2014-03-06"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-02-28"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Debra Clark",
    "FriendshipDate": "2014-02-28"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2014-02-21"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2014-02-21"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2014-02-08"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2014-02-08"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-12-20"
  },
  {
    "Person1": "Kevin Johnson",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-12-20"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2013-12-11"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2013-12-11"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2013-11-19"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2013-11-19"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2013-10-16"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Christopher Miller",
    "FriendshipDate": "2013-10-16"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2013-10-01"
  },
  {
    "Person1": "Timothy Walls",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2013-10-01"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2013-09-15"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Mia Sutton",
    "FriendshipDate": "2013-09-15"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2013-08-10"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2013-08-10"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2013-04-28"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz",
    "FriendshipDate": "2013-04-28"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "William Brady",
    "FriendshipDate": "2013-03-11"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "William Brady",
    "FriendshipDate": "2013-03-11"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2013-03-06"
  },
  {
    "Person1": "Rachel Graham",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2013-03-06"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-02-28"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-02-28"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-01-19"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2013-01-19"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2012-10-14"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2012-10-14"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Jeffrey Henderson",
    "FriendshipDate": "2012-09-22"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Jeffrey Henderson",
    "FriendshipDate": "2012-09-22"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2012-08-06"
  },
  {
    "Person1": "Logan Archer",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2012-08-06"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2012-04-12"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Theresa Vazquez",
    "FriendshipDate": "2012-04-12"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2012-03-24"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2012-03-24"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "FriendshipDate": "2012-03-23"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "April Wise",
    "FriendshipDate": "2012-03-23"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Michael Orr",
    "FriendshipDate": "2012-03-22"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Michael Orr",
    "FriendshipDate": "2012-03-22"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Debra Clark",
    "FriendshipDate": "2012-03-14"
  },
  {
    "Person1": "Michael Orr",
    "Person2": "Debra Clark",
    "FriendshipDate": "2012-03-14"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Scott Walker",
    "FriendshipDate": "2012-02-08"
  },
  {
    "Person1": "Brandi Bailey",
    "Person2": "Scott Walker",
    "FriendshipDate": "2012-02-08"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2012-01-20"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Ryan",
    "FriendshipDate": "2012-01-20"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Kevin Johnson",
    "FriendshipDate": "2012-01-16"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Kevin Johnson",
    "FriendshipDate": "2012-01-16"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2011-12-27"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2011-12-27"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise",
    "FriendshipDate": "2011-12-22"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise",
    "FriendshipDate": "2011-12-22"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2011-11-21"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Williams",
    "FriendshipDate": "2011-11-21"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2011-10-25"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Juan Calderon",
    "FriendshipDate": "2011-10-25"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2011-10-06"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2011-10-06"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Jordan Gonzalez",
    "FriendshipDate": "2011-09-29"
  },
  {
    "Person1": "Jessica Chavez",
    "Person2": "Jordan Gonzalez",
    "FriendshipDate": "2011-09-29"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2011-09-17"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2011-09-17"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2011-08-09"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Eric Ortiz",
    "FriendshipDate": "2011-08-09"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2011-08-05"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2011-08-05"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2011-07-29"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Angel Riggs",
    "FriendshipDate": "2011-07-29"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2011-06-28"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Cheryl Robinson",
    "FriendshipDate": "2011-06-28"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2011-06-15"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Connie Lawrence",
    "FriendshipDate": "2011-06-15"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Steve Newton",
    "FriendshipDate": "2011-05-12"
  },
  {
    "Person1": "Nathaniel Khan",
    "Person2": "Steve Newton",
    "FriendshipDate": "2011-05-12"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "FriendshipDate": "2011-05-09"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker",
    "FriendshipDate": "2011-05-09"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Anna Davis",
    "FriendshipDate": "2011-04-06"
  },
  {
    "Person1": "Jordan Gonzalez",
    "Person2": "Anna Davis",
    "FriendshipDate": "2011-04-06"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "FriendshipDate": "2011-01-25"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos",
    "FriendshipDate": "2011-01-25"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2010-09-18"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Dana Douglas",
    "FriendshipDate": "2010-09-18"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "FriendshipDate": "2010-09-12"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel",
    "FriendshipDate": "2010-09-12"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Logan Archer",
    "FriendshipDate": "2010-08-12"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Logan Archer",
    "FriendshipDate": "2010-08-12"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2010-07-26"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2010-07-26"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2010-05-16"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Michael Robinson",
    "FriendshipDate": "2010-05-16"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2010-05-06"
  },
  {
    "Person1": "Theresa Vazquez",
    "Person2": "Matthew Marshall",
    "FriendshipDate": "2010-05-06"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2010-03-08"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Todd Wilson",
    "FriendshipDate": "2010-03-08"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "FriendshipDate": "2010-01-14"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Timothy Walls",
    "FriendshipDate": "2010-01-14"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Stephanie Martin",
    "FriendshipDate": "2010-01-05"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Stephanie Martin",
    "FriendshipDate": "2010-01-05"
  }
]
```

#### Additional Information

- **Category:** Inconclusive
- **Difficulty:** medium
- **Tokens Used:** 3,286
- **Execution Time:** 6.95s
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
    "p.firstName": "Juan",
    "p.lastName": "Calderon",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Savannah",
    "p.lastName": "Delacruz",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Joseph",
    "p.lastName": "Maddox",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Jessica",
    "p.lastName": "Chavez",
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
    "p.firstName": "Crystal",
    "p.lastName": "Whitehead",
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
    "p.firstName": "Samuel",
    "p.lastName": "Wagner",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Theresa",
    "p.lastName": "Vazquez",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Todd",
    "p.lastName": "Wilson",
    "j.title": "Teacher"
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Ryan",
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
    "p.firstName": "Joseph",
    "p.lastName": "Williams",
    "j.title": "Teacher"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,366
- **Execution Time:** 5.15s
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
- **Tokens Used:** 1,383
- **Execution Time:** 5.42s
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
- **Tokens Used:** 1,411
- **Execution Time:** 6.73s
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
RETURN p.firstName AS PalindromicName
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
    "PalindromicName": "Anna"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,366
- **Execution Time:** 3.71s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 61: 62
**Status:** PASS

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
MATCH (p:Person)
WHERE EXISTS((p)<-[:IS_PARENT]-()) AND EXISTS((p)-[:IS_PARENT]->())
RETURN p.firstName AS firstName, p.lastName AS lastName, p.id AS id
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
    "firstName": "Connie",
    "lastName": "Lawrence",
    "id": "p3"
  },
  {
    "firstName": "Mia",
    "lastName": "Sutton",
    "id": "p7"
  },
  {
    "firstName": "Charles",
    "lastName": "Taylor",
    "id": "p10"
  },
  {
    "firstName": "Joseph",
    "lastName": "Maddox",
    "id": "p12"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 2,746
- **Execution Time:** 4.34s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
  AND EXISTS((p)<-[:IS_PARENT]-(:Person))
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
- **Tokens Used:** 5,842
- **Execution Time:** 5.70s
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
WHERE (p1)-[:LIVES_IN]->(:Location)<>(:Location)<-[:LIVES_IN]-(p2)
RETURN p1.firstName + ' ' + p1.lastName AS Partner1, p2.firstName + ' ' + p2.lastName AS Partner2,
       [(p1)-[:LIVES_IN]->(l1:Location) | l1.name][0] AS City1,
       [(p2)-[:LIVES_IN]->(l2:Location) | l2.name][0] AS City2
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It should therefore only be used in contexts that evaluate to a boolean, e.g. inside the function exists() or in a WHERE-clause. No other uses are allowed, instead they should be replaced by a pattern comprehension. (line 2, column 7 (offset: 59))
"WHERE (p1)-[:LIVES_IN]->(:Location)<>(:Location)<-[:LIVES_IN]-(p2)"
       ^}
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
[]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 3,581
- **Execution Time:** 7.43s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
MATCH (p1:Person)-[f1:IS_FRIEND]-(p2:Person)-[f2:IS_FRIEND]-(p3:Person)-[f3:IS_FRIEND]-(p1)
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
- **Tokens Used:** 3,492
- **Execution Time:** 8.21s
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
WITH p, s.degree AS degree, COUNT(DISTINCT e) AS count
RETURN degree, COUNT(p) AS peopleCount, SUM(count) AS totalDegrees
ORDER BY peopleCount DESC
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
- **Tokens Used:** 2,124
- **Execution Time:** 5.17s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 66: 67
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Type mismatch: expected List<T> but was String (line 2, column 7 (offset: 23))
"WHERE toLower(p.firstName)[0] = toLower(p.lastName)[0]"
       ^}
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

- **Category:** pattern_matching
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
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
- **Tokens Used:** 1,448
- **Execution Time:** 7.73s
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
- **Tokens Used:** 4,995
- **Execution Time:** 6.35s
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
- **Tokens Used:** 1,380
- **Execution Time:** 6.27s
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
WHERE u.foundedYear < 1800
RETURN u.name, u.type, u.foundedYear, u.country
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
    "u.type": "College",
    "u.foundedYear": 1571,
    "u.country": "Hong Kong"
  },
  {
    "u.name": "Priceshire Institute",
    "u.type": "Institute",
    "u.foundedYear": 1619,
    "u.country": "Yemen"
  },
  {
    "u.name": "Castanedachester Institute",
    "u.type": "College",
    "u.foundedYear": 1730,
    "u.country": "Mauritania"
  },
  {
    "u.name": "Smithstad University",
    "u.type": "College",
    "u.foundedYear": 1787,
    "u.country": "French Southern Territories"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,364
- **Execution Time:** 5.24s
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
- **Tokens Used:** 2,021
- **Execution Time:** 7.72s
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
WHERE j.category = 'Management'
RETURN DISTINCT j.title
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
- **Tokens Used:** 4,397
- **Execution Time:** 4.09s
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
- **Tokens Used:** 2,679
- **Execution Time:** 3.92s
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
- **Tokens Used:** 1,384
- **Execution Time:** 6.37s
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
[
  {
    "City": "Karenview",
    "Population": 13126125
  },
  {
    "City": "Patricialand",
    "Population": 12819117
  },
  {
    "City": "Stephaniemouth",
    "Population": 11636146
  },
  {
    "City": "Perryborough",
    "Population": 10639534
  },
  {
    "City": "Lake Michelle",
    "Population": 9619364
  },
  {
    "City": "Simsview",
    "Population": 9234763
  },
  {
    "City": "Lake Justinview",
    "Population": 6060072
  },
  {
    "City": "East Patrick",
    "Population": 4875083
  },
  {
    "City": "Rivasside",
    "Population": 3376763
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,602
- **Execution Time:** 4.38s
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
RETURN p.firstName + ' ' + p.lastName AS graduate
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
    "graduate": "Samuel Wagner"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,836
- **Execution Time:** 5.11s
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
MATCH (p1:Person)-[r:IS_HUSBAND|IS_WIFE]->(p2:Person)
WITH p1, p2, r, abs(duration.between(date(p1.birthDate), date(p2.birthDate)).years) AS ageDifference
ORDER BY ageDifference DESC
LIMIT 5
RETURN p1.firstName + ' ' + p1.lastName AS Partner1, 
       p2.firstName + ' ' + p2.lastName AS Partner2, 
       type(r) AS RelationshipType, 
       ageDifference
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
    "Partner1": "Michael Robinson",
    "Partner2": "Mia Sutton",
    "RelationshipType": "IS_WIFE",
    "ageDifference": 28
  },
  {
    "Partner1": "Mia Sutton",
    "Partner2": "Michael Robinson",
    "RelationshipType": "IS_HUSBAND",
    "ageDifference": 28
  },
  {
    "Partner1": "Savannah Delacruz",
    "Partner2": "Juan Calderon",
    "RelationshipType": "IS_HUSBAND",
    "ageDifference": 13
  },
  {
    "Partner1": "Juan Calderon",
    "Partner2": "Savannah Delacruz",
    "RelationshipType": "IS_WIFE",
    "ageDifference": 13
  },
  {
    "Partner1": "Jessica Chavez",
    "Partner2": "Joseph Maddox",
    "RelationshipType": "IS_HUSBAND",
    "ageDifference": 12
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 2,181
- **Execution Time:** 6.01s
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
- **Tokens Used:** 1,904
- **Execution Time:** 5.36s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `f` not defined (line 8, column 22 (offset: 269))
"WITH p1, p2, c1, c2, f, w1, w2"
                      ^}
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

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
WHERE w.startYear < s.endYear
RETURN DISTINCT p.firstName, p.lastName, e.name AS institute, c.name AS company,
       w.startYear AS workStartYear, s.endYear AS studyEndYear
ORDER BY p.firstName, p.lastName
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
    "p.firstName": "Annette",
    "p.lastName": "Pearson",
    "institute": "Priceshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1994,
    "studyEndYear": 1999
  },
  {
    "p.firstName": "Charles",
    "p.lastName": "Taylor",
    "institute": "Priceshire Institute",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1954,
    "studyEndYear": 1957
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institute": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1970,
    "studyEndYear": 1975
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institute": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1970,
    "studyEndYear": 1979
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institute": "Smithstad University",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1976,
    "studyEndYear": 1979
  },
  {
    "p.firstName": "Christopher",
    "p.lastName": "Miller",
    "institute": "Castanedachester Institute",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1948,
    "studyEndYear": 1953
  },
  {
    "p.firstName": "Connie",
    "p.lastName": "Lawrence",
    "institute": "Castanedachester Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1949,
    "studyEndYear": 1953
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institute": "Priceshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2019
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institute": "Priceshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 2016,
    "studyEndYear": 2019
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institute": "Port Nicoleshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2021
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institute": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 2016,
    "studyEndYear": 2021
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institute": "Castanedachester Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2015
  },
  {
    "p.firstName": "David",
    "p.lastName": "Lee",
    "institute": "Castanedachester Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 1970,
    "studyEndYear": 1972
  },
  {
    "p.firstName": "Debra",
    "p.lastName": "Clark",
    "institute": "Port Nicoleshire Institute",
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 2001,
    "studyEndYear": 2004
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "institute": "Smithstad University",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1990,
    "studyEndYear": 1991
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "institute": "Smithstad University",
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 1986,
    "studyEndYear": 1991
  },
  {
    "p.firstName": "Eric",
    "p.lastName": "Ortiz",
    "institute": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1978,
    "studyEndYear": 1980
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "institute": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1961,
    "studyEndYear": 1967
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "institute": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1966,
    "studyEndYear": 1967
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "institute": "South Jeffrey Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1995,
    "studyEndYear": 1997
  },
  {
    "p.firstName": "Samuel",
    "p.lastName": "Wagner",
    "institute": "Priceshire Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2015,
    "studyEndYear": 2016
  },
  {
    "p.firstName": "Scott",
    "p.lastName": "Walker",
    "institute": "Priceshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1962,
    "studyEndYear": 1965
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Patton",
    "institute": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1955,
    "studyEndYear": 1956
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Ryan",
    "institute": "Priceshire Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2002,
    "studyEndYear": 2003
  },
  {
    "p.firstName": "Theresa",
    "p.lastName": "Vazquez",
    "institute": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1956,
    "studyEndYear": 1957
  },
  {
    "p.firstName": "Thomas",
    "p.lastName": "Schmidt",
    "institute": "South Jeffrey Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1946,
    "studyEndYear": 1950
  },
  {
    "p.firstName": "Timothy",
    "p.lastName": "Walls",
    "institute": "Smithstad University",
    "company": "Rogers-Hobbs",
    "workStartYear": 1982,
    "studyEndYear": 1984
  },
  {
    "p.firstName": "Todd",
    "p.lastName": "Wilson",
    "institute": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 2006,
    "studyEndYear": 2009
  },
  {
    "p.firstName": "Tracey",
    "p.lastName": "Hickman",
    "institute": "Smithstad University",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2009,
    "studyEndYear": 2013
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "institute": "Priceshire Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1981,
    "studyEndYear": 1984
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 5,412
- **Execution Time:** 6.57s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 81: 82
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `p` not defined (line 7, column 45 (offset: 273))
"WITH f, AVG(duration) AS avgDuration, COUNT(p) AS studentCount"
                                             ^}
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

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 82: 83
**Status:** PASS

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
MATCH (parent:Person)-[:IS_PARENT]->(child:Person),
      (parent)-[parentWork:WORKED_AT]->(company:Company),
      (child)-[childWork:WORKED_AT]->(company)
WHERE parentWork.status = 'Current' AND childWork.status = 'Current'
RETURN parent.firstName + ' ' + parent.lastName AS Parent,
       child.firstName + ' ' + child.lastName AS Child,
       company.name AS Company
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
    "Child": "Charles Taylor",
    "Company": "Johnson-Rogers"
  },
  {
    "Parent": "Kevin Johnson",
    "Child": "Connie Lawrence",
    "Company": "Ruiz Ltd"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 3,397
- **Execution Time:** 9.12s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 83: 84
**Status:** FAIL

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
WHERE (p1)-[:STUDIED_AT]->(u:EducationalInstitution) AND (p2)-[:STUDIED_AT]->(u)
WITH p1, p2, u, [(p1)-[:IS_PARENT*1..3]->(x:Person) | x] AS familyLine
WHERE size(familyLine) >= 3
RETURN DISTINCT p1.firstName + ' ' + p1.lastName AS Ancestor, 
       p2.firstName + ' ' + p2.lastName AS Descendant, 
       u.name AS University, 
       size(familyLine) AS Generations
ORDER BY Generations DESC, Ancestor, Descendant
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'u'. (line 2, column 28 (offset: 76))
"WHERE (p1)-[:STUDIED_AT]->(u:EducationalInstitution) AND (p2)-[:STUDIED_AT]->(u)"
                            ^}
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
[]
```

#### Additional Information

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 1,456
- **Execution Time:** 7.92s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
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
MATCH (p:Person)-[:LIVES_IN]->(currentLocation:Location),
      (p)-[:LIVED_IN]->(foreignLocation:Location),
      (p)-[:LIVES_IN]->(birthCountry:Location)
WHERE p.birthPlace = birthCountry.name
  AND foreignLocation.country <> birthCountry.country
  AND currentLocation.country = birthCountry.country
  AND EXISTS((p)-[:LIVED_IN]->(foreignLocation))
RETURN p.firstName + ' ' + p.lastName AS name,
       p.birthPlace AS birthPlace,
       foreignLocation.name AS foreignLocation,
       currentLocation.name AS currentLocation
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
- **Tokens Used:** 1,476
- **Execution Time:** 7.48s
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
MATCH (p:Person)-[s1:STUDIED_AT]->(i1:EducationalInstitution)
WITH p, s1, i1
MATCH (p)-[s2:STUDIED_AT]->(i2:EducationalInstitution)
WHERE id(s1) < id(s2) AND 
      ((s1.startYear <= s2.startYear AND s1.endYear >= s2.startYear) OR
       (s2.startYear <= s1.startYear AND s2.endYear >= s1.startYear))
RETURN p.firstName + ' ' + p.lastName AS PersonName,
       i1.name AS Institution1, s1.degree AS Degree1, s1.startYear AS Start1, s1.endYear AS End1,
       i2.name AS Institution2, s2.degree AS Degree2, s2.startYear AS Start2, s2.endYear AS End2
ORDER BY PersonName
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
    "PersonName": "Cheryl Robinson",
    "Institution1": "Smithstad University",
    "Degree1": "Bachelor",
    "Start1": 1971,
    "End1": 1975,
    "Institution2": "Smithstad University",
    "Degree2": "PhD",
    "Start2": 1974,
    "End2": 1979
  },
  {
    "PersonName": "Dana Douglas",
    "Institution1": "Castanedachester Institute",
    "Degree1": "Bachelor",
    "Start1": 2011,
    "End1": 2015,
    "Institution2": "Priceshire Institute",
    "Degree2": "PhD",
    "Start2": 2014,
    "End2": 2019
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
- **Tokens Used:** 2,286
- **Execution Time:** 10.01s
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
RETURN p.firstName, p.lastName, p.id
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
    "p.id": "p4"
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "p.id": "p7"
  },
  {
    "p.firstName": "Michael",
    "p.lastName": "Robinson",
    "p.id": "p8"
  },
  {
    "p.firstName": "Jessica",
    "p.lastName": "Chavez",
    "p.id": "p13"
  },
  {
    "p.firstName": "Jordan",
    "p.lastName": "Gonzalez",
    "p.id": "p14"
  },
  {
    "p.firstName": "David",
    "p.lastName": "Brown",
    "p.id": "p18"
  },
  {
    "p.firstName": "Nathaniel",
    "p.lastName": "Khan",
    "p.id": "p20"
  },
  {
    "p.firstName": "Jeffrey",
    "p.lastName": "Henderson",
    "p.id": "p21"
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "p.id": "p25"
  },
  {
    "p.firstName": "Jared",
    "p.lastName": "David",
    "p.id": "p27"
  },
  {
    "p.firstName": "Timothy",
    "p.lastName": "Walls",
    "p.id": "p29"
  },
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey",
    "p.id": "p30"
  },
  {
    "p.firstName": "Logan",
    "p.lastName": "Archer",
    "p.id": "p31"
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "p.id": "p37"
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "p.id": "p40"
  },
  {
    "p.firstName": "Rachel",
    "p.lastName": "Graham",
    "p.id": "p42"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall",
    "p.id": "p46"
  },
  {
    "p.firstName": "Angel",
    "p.lastName": "Riggs",
    "p.id": "p48"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 3,237
- **Execution Time:** 4.88s
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
RETURN c.name AS CompanyName, employeeCount
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
    "employeeCount": 92460
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 4,539
- **Execution Time:** 4.80s
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
- **Tokens Used:** 1,349
- **Execution Time:** 4.77s
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
- **Execution Time:** 4.07s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'WHERE': expected an expression, ')' or ',' (line 3, column 51 (offset: 134))
"  AND NOT EXISTS((p)-[:HAD_POSITION]->(:JobTitle) WHERE p.endYear IS NULL)"
                                                   ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `s` not defined (line 10, column 28 (offset: 263))
"RETURN f, studentCount, p, s"
                            ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 7.33s
- **Syntactic Correct:** No
- **Execution Success:** No
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
- **Tokens Used:** 1,651
- **Execution Time:** 3.85s
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
    "FoundedYear": 2018
  },
  {
    "CompanyName": "Hooper PLC",
    "FoundedYear": 2005
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,688
- **Execution Time:** 5.09s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 95: 96
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Invalid use of aggregating function collect(...) in this context (line 6, column 21 (offset: 159))
"WHERE c.industry IN COLLECT(industry)"
                     ^}
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

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `f` not defined (line 12, column 16 (offset: 498))
"RETURN p1, p2, f, loc1, loc2, l1, l2"
                ^}
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
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 97: 98
**Status:** FAIL

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
WITH p.birthDate AS birthDate, SUBSTRING(p.birthDate, 6, 2) AS birthMonth
WITH birthMonth, COUNT(*) AS count
ORDER BY count DESC, birthMonth
RETURN birthMonth, count
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
    "birthMonth": "1-",
    "count": 10
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,419
- **Execution Time:** 6.17s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
WHERE p1.id < p2.id
  AND toLower(p1.firstName) = toLower(p2.firstName)
  AND toLower(p1.lastName) = toLower(p2.lastName)
RETURN count(*) AS sameNameCount
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
    "sameNameCount": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,379
- **Execution Time:** 5.72s
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
RETURN COUNT(p) AS peopleCount
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
    "peopleCount": 0
  }
]
```

#### Additional Information

- **Category:** paradox
- **Difficulty:** easy
- **Tokens Used:** 1,459
- **Execution Time:** 4.83s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---
