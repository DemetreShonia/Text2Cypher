# Evaluation Report: Simple + Retrieval

**Run Time:** 2025-07-04 14:11:49

## Summary Metrics

- **Total Cases:** 99
- **Overall Accuracy:** 45.45%
- **Syntactic Correctness:** 74.75%
- **Execution Success:** 68.69%
- **Total Tokens:** 165,821

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
- **Tokens Used:** 815
- **Execution Time:** 8.64s
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
- **Tokens Used:** 753
- **Execution Time:** 4.64s
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
- **Tokens Used:** 6,510
- **Execution Time:** 6.56s
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
- **Tokens Used:** 6,685
- **Execution Time:** 5.75s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: All sub queries in an UNION must have the same return column names (line 7, column 1 (offset: 177))
"UNION"
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
- **Tokens Used:** 746
- **Execution Time:** 10.99s
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
RETURN COUNT(DISTINCT p) AS peopleWithYoungerSisterAndDataScientist
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
    "peopleWithYoungerSisterAndDataScientist": 0
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 804
- **Execution Time:** 8.31s
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
- **Tokens Used:** 2,931
- **Execution Time:** 5.21s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
WHERE toLower(p.firstName) = 'mark'
  AND toLower(c.industry) = 'tech'
  AND toLower(c.headquarters) = 'spain'
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
- **Tokens Used:** 757
- **Execution Time:** 5.17s
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
- **Tokens Used:** 762
- **Execution Time:** 6.54s
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
MATCH (p:Person)-[:HAD_POSITION]->(j:JobTitle {title: 'Doctor'}),
      (p)-[:LIVES_IN]->(l:Location {country: 'New Zealand'})
WHERE toLower(p.firstName) = 'mia'
RETURN count(DISTINCT p) AS doctorCount
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
    "doctorCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 871
- **Execution Time:** 6.03s
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
WHERE date().year - toInteger(substring(p.birthDate, 0, 4)) >= 13 
  AND date().year - toInteger(substring(p.birthDate, 0, 4)) <= 39
WITH p, size((p)-[:IS_FRIEND]-()) AS friendCount
RETURN avg(friendCount) AS averageFriends
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 4, column 14 (offset: 163))
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
- **Tokens Used:** 1,023
- **Execution Time:** 6.30s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 13: 13
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.TypeError} {message: Invalid input for function 'toInteger()': Expected a String, Float, Integer or Boolean, got: List{String("1993-07-14")}}
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
- **Tokens Used:** 775
- **Execution Time:** 6.60s
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
MATCH (p:Person)-[:STUDIED]->(fos:FieldOfStudy)
WHERE toLower(p.firstName) = 'connie' AND toLower(fos.name) = 'business administration'
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
- **Tokens Used:** 6,656
- **Execution Time:** 6.73s
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
- **Tokens Used:** 734
- **Execution Time:** 5.93s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 17: 17
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 32))
"WITH l, size((l)<-[:LIVES_IN]-()) AS population"
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
- **Tokens Used:** 4,002
- **Execution Time:** 5.05s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: All sub queries in an UNION must have the same return column names (line 9, column 1 (offset: 209))
"UNION"
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

### Test Case 20: 20
**Status:** FAIL

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
MATCH (l:Location {country: "New Zealand"})<-[:LIVES_IN]-(p:Person)
WHERE toLower(l.country) = "new zealand"
WITH l, p, date().year - toInteger(substring(p.birthDate, 0, 4)) AS age
RETURN l.name AS location, AVG(age) AS averageAge
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
    "location": "Stephaniemouth",
    "averageAge": 66.4
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 830
- **Execution Time:** 6.13s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `s` not defined (line 10, column 11 (offset: 357))
"RETURN p, s, e, l, loc, w, c"
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
    WHEN toFloat(studiedAbroadAndReturned) / totalPopulation > 0.5 
    THEN 'There is a correlation between studying abroad and returning home' 
    ELSE 'There is no correlation between studying abroad and returning home' 
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
- **Tokens Used:** 876
- **Execution Time:** 8.29s
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
MATCH (p:Person)-[:STUDIED_AT]->(e:EducationalInstitution)-[:LOCATED_IN]->(studyCountry:Location)
WITH p, studyCountry
MATCH (p)-[:LIVED_IN]->(l:Location)
WHERE l.country <> studyCountry.country
WITH p, studyCountry, collect(DISTINCT l.country) AS livedCountries
WHERE size(livedCountries) > 0
WITH count(p) AS totalStudiedAbroad, 
     sum(CASE WHEN size(livedCountries) > 1 THEN 1 ELSE 0 END) AS movedAgain
RETURN 
    CASE 
        WHEN totalStudiedAbroad > 0 THEN 
            CASE 
                WHEN toFloat(movedAgain) / totalStudiedAbroad > 0.5 
                THEN 'There is a correlation between studying abroad and changing countries again.' 
                ELSE 'There is no correlation between studying abroad and changing countries again.' 
            END 
        ELSE 'Insufficient data to determine correlation.' 
    END AS result
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
    "result": "Insufficient data to determine correlation."
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,826
- **Execution Time:** 9.81s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 3, column 14 (offset: 74))
"WITH p, size((p)-[:WORKED_AT]->(:Company {industry: 'Technology'})) = 0 AS notInTech"
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
MATCH (p:Person)
WHERE toLower(p.firstName) = 'charles'
OPTIONAL MATCH (p)-[:IS_SIBLING]->(sibling:Person)
WHERE sibling.gender = 'Female'
WITH p, count(sibling) AS sisterCount
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
    "averageSisterCount": 2.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 799
- **Execution Time:** 6.67s
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
MATCH (c:Person)-[:IS_FRIEND]-(j:Person)
WHERE toLower(c.firstName) = 'christopher' AND toLower(j.firstName) = 'jessica'
RETURN count(DISTINCT c) AS christophersWithJessicaFriend
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
- **Tokens Used:** 892
- **Execution Time:** 4.84s
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
WHERE toLower(j.category) = toLower(f.category)
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
- **Tokens Used:** 770
- **Execution Time:** 5.51s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
MATCH (p:Person)
WITH p, toLower(p.firstName + '.' + p.lastName) AS nameEmail, toLower(p.email) AS lowercaseEmail
WITH COUNT(p) AS totalPeople, SUM(CASE WHEN nameEmail + '@example.com' = lowercaseEmail OR nameEmail + '@example.org' OR nameEmail + '@example.net' THEN 1 ELSE 0 END) AS nameAsEmailCount
RETURN toFloat(nameAsEmailCount) / totalPeople * 100 AS percentageUsingNameAsEmail
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Type mismatch: expected Boolean but was String (line 3, column 102 (offset: 215))
"WITH COUNT(p) AS totalPeople, SUM(CASE WHEN nameEmail + '@example.com' = lowercaseEmail OR nameEmail + '@example.org' OR nameEmail + '@example.net' THEN 1 ELSE 0 END) AS nameAsEmailCount"
                                                                                                      ^}
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
[]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 2,111
- **Execution Time:** 8.32s
- **Syntactic Correct:** Yes
- **Execution Success:** No
- **Test Case Passed:** No
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
- **Tokens Used:** 753
- **Execution Time:** 6.68s
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
MATCH (p:Person)-[:IS_SIBLING]->(sister:Person)
WHERE toLower(p.firstName) = 'connie'
MATCH (sister)-[w:WORKED_AT]->(company:Company)
MATCH (sister)-[h:HAD_POSITION]->(jobTitle:JobTitle)
WHERE h.companyId = company.id AND h.startYear = w.startYear
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
- **Tokens Used:** 5,936
- **Execution Time:** 6.77s
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
MATCH (parent:Person)-[:IS_PARENT]->(child:Person)-[:LIVES_IN]->(:Location {country: 'Grenada'})
WITH parent, COUNT(child) AS childCount
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
    "averageChildrenPerParent": 1.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 756
- **Execution Time:** 5.10s
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
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `u` not defined (line 5, column 24 (offset: 262))
"WITH DISTINCT p, f, c, u, l"
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `c` not defined (line 4, column 17 (offset: 202))
"WITH p, spouse, c, l"
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
MATCH (p)-[:WORKED_AT]->(c:Company)
MATCH (p)-[:HAD_POSITION]->(j:JobTitle)
WITH p, e, c, j,
     toLower(e.type) AS educationType,
     toLower(j.category) AS jobCategory
WITH COUNT(DISTINCT p) AS totalPeople,
     SUM(CASE WHEN educationType = jobCategory THEN 1 ELSE 0 END) AS matchingPeople
RETURN 
    CASE 
        WHEN toFloat(matchingPeople) / toFloat(totalPeople) > 0.5 
        THEN 'Education and career are correlated' 
        ELSE 'Education and career are not correlated' 
    END AS correlation,
    toFloat(matchingPeople) / toFloat(totalPeople) AS correlationRatio
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
    "correlation": "Education and career are not correlated",
    "correlationRatio": 0.0
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** hard
- **Tokens Used:** 6,752
- **Execution Time:** 7.91s
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
- **Execution Time:** 6.34s
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

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 6.36s
- **Syntactic Correct:** No
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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)
WITH p, l.country AS country, size((p)-[:WORKED_AT]->()) AS jobCount
RETURN country, round(avg(jobCount), 2) AS avgJobs
ORDER BY avgJobs DESC
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 36 (offset: 78))
"WITH p, l.country AS country, size((p)-[:WORKED_AT]->()) AS jobCount"
                                    ^}
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
- **Tokens Used:** 1,209
- **Execution Time:** 6.26s
- **Syntactic Correct:** Yes
- **Execution Success:** No
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
WHERE m.birthDate > w.birthDate
WITH m, w
MATCH (m)-[:IS_SIBLING]->(s:Person {gender: 'Female'})
WHERE m.birthDate < s.birthDate
RETURN DISTINCT m.firstName, m.lastName, w.firstName AS spouse_firstName, w.lastName AS spouse_lastName, s.firstName AS sister_firstName, s.lastName AS sister_lastName
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
- **Tokens Used:** 797
- **Execution Time:** 6.73s
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
MATCH (l:Location)<-[:LIVES_IN]-(p:Person)
WITH l, COUNT(CASE WHEN p.gender = 'Male' THEN 1 END) AS maleCount,
     COUNT(CASE WHEN p.gender = 'Female' THEN 1 END) AS femaleCount
WHERE maleCount > femaleCount
RETURN l.name AS LocationName, l.country AS Country, maleCount, femaleCount
ORDER BY maleCount DESC
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
    "LocationName": "Rivasside",
    "Country": "Kiribati",
    "maleCount": 5,
    "femaleCount": 3
  },
  {
    "LocationName": "Lake Michelle",
    "Country": "Korea",
    "maleCount": 5,
    "femaleCount": 2
  },
  {
    "LocationName": "Simsview",
    "Country": "Kazakhstan",
    "maleCount": 5,
    "femaleCount": 1
  },
  {
    "LocationName": "East Patrick",
    "Country": "Cape Verde",
    "maleCount": 4,
    "femaleCount": 2
  },
  {
    "LocationName": "Stephaniemouth",
    "Country": "New Zealand",
    "maleCount": 3,
    "femaleCount": 2
  },
  {
    "LocationName": "Patricialand",
    "Country": "Burundi",
    "maleCount": 2,
    "femaleCount": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 3,721
- **Execution Time:** 6.66s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 32))
"WITH l, size((l)<-[:LIVES_IN]-(:Person {gender: 'Male'})) AS maleCount,"
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
MATCH (p:Person)-[s:STUDIED_AT]->(ei:EducationalInstitution)
WHERE toLower(p.nationality) <> toLower(ei.country)
WITH ei, COUNT(DISTINCT p) AS foreignStudentCount
ORDER BY foreignStudentCount DESC
LIMIT 3
RETURN ei.name AS institutionName, ei.country AS country, foreignStudentCount
ORDER BY foreignStudentCount DESC
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
    "institutionName": "Smithstad University",
    "country": "French Southern Territories",
    "foreignStudentCount": 9
  },
  {
    "institutionName": "South Jeffrey Institute",
    "country": "Jordan",
    "foreignStudentCount": 8
  },
  {
    "institutionName": "Priceshire Institute",
    "country": "Yemen",
    "foreignStudentCount": 7
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,671
- **Execution Time:** 6.10s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 43: 43
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `s` not defined (line 12, column 36 (offset: 390))
"RETURN ei, foreignStudentCount, p, s"
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
RETURN w.firstName + ' ' + w.lastName AS Wife, h.firstName + ' ' + h.lastName AS Husband, w.birthDate AS WifeBirthDate, h.birthDate AS HusbandBirthDate
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
- **Tokens Used:** 2,375
- **Execution Time:** 5.57s
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
MATCH (p:Person)-[:IS_HUSBAND|IS_WIFE]->(spouse:Person)
MATCH (p)-[:LIVES_IN]->(city:Location)
WITH city, p, spouse, p.birthDate AS birthDate
ORDER BY birthDate
WITH city, COLLECT({person: p, spouse: spouse, birthDate: birthDate})[0] AS oldestCouple
RETURN city.name AS City, oldestCouple.person.firstName + ' ' + oldestCouple.person.lastName AS OldestMarriedPerson, oldestCouple.birthDate AS BirthDate, oldestCouple.spouse.firstName + ' ' + oldestCouple.spouse.lastName AS Spouse
ORDER BY City
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
    "BirthDate": "1935-02-12",
    "Spouse": "Juan Calderon"
  },
  {
    "City": "Lake Justinview",
    "OldestMarriedPerson": "Mark Johnson",
    "BirthDate": "1928-06-16",
    "Spouse": "Kevin Johnson"
  },
  {
    "City": "Lake Michelle",
    "OldestMarriedPerson": "Kevin Johnson",
    "BirthDate": "1929-11-07",
    "Spouse": "Mark Johnson"
  },
  {
    "City": "North Robert",
    "OldestMarriedPerson": "Juan Calderon",
    "BirthDate": "1948-05-13",
    "Spouse": "Savannah Delacruz"
  },
  {
    "City": "Perryborough",
    "OldestMarriedPerson": "Michael Robinson",
    "BirthDate": "2000-03-19",
    "Spouse": "Mia Sutton"
  },
  {
    "City": "Simsview",
    "OldestMarriedPerson": "Charles Taylor",
    "BirthDate": "1934-01-16",
    "Spouse": "Johnny Campos"
  },
  {
    "City": "Stephaniemouth",
    "OldestMarriedPerson": "Johnny Campos",
    "BirthDate": "1943-03-10",
    "Spouse": "Charles Taylor"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 1,623
- **Execution Time:** 6.92s
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
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 7.77s
- **Syntactic Correct:** No
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
- **Tokens Used:** 745
- **Execution Time:** 5.38s
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
WHERE p.cousinCount > p.siblingCount
RETURN p.firstName + ' ' + p.lastName AS name, p.cousinCount AS cousins, p.siblingCount AS siblings
ORDER BY p.cousinCount DESC, p.siblingCount ASC
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 2,625
- **Execution Time:** 6.53s
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
WHERE s1.startYear < toInteger(left(p1.birthDate, 4)) OR s2.startYear < toInteger(left(p2.birthDate, 4))
RETURN p1.firstName + ' ' + p1.lastName AS Sibling1, p2.firstName + ' ' + p2.lastName AS Sibling2, e.name AS Institution
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
- **Tokens Used:** 807
- **Execution Time:** 7.70s
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
- **Execution Time:** 6.21s
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
WITH p, COUNT(child) AS childCount, COLLECT(child) AS children
WHERE childCount > 0
RETURN p.firstName + ' ' + p.lastName AS youngestParent, p.birthDate AS birthDate, childCount, [child IN children | child.firstName + ' ' + child.lastName] AS childrenNames
ORDER BY date(p.birthDate) DESC
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
    "birthDate": "2000-03-19",
    "childCount": 1,
    "childrenNames": [
      "Debra Clark"
    ]
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 1,612
- **Execution Time:** 9.51s
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
RETURN p.firstName + ' ' + p.lastName AS most_traveled_person, total_locations
ORDER BY total_locations DESC
LIMIT 1
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
- **Tokens Used:** 7,087
- **Execution Time:** 6.53s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It can no longer be used inside the function size(), an alternative is to replace size() with COUNT {}. (line 2, column 14 (offset: 30))
"WITH p, size((p)-[:IS_FRIEND]->()) AS friendCount"
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
MATCH (p:Person)-[r:LIVED_IN]->(l:Location)
WITH p, COUNT(DISTINCT l) AS locationCount
WHERE locationCount = 3
RETURN p.firstName + ' ' + p.lastName AS name
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
    "name": "Stephanie Martin"
  },
  {
    "name": "Thomas Schmidt"
  },
  {
    "name": "Eric Ortiz"
  },
  {
    "name": "Dana Douglas"
  },
  {
    "name": "Vanessa Patel"
  },
  {
    "name": "Eugene Green"
  },
  {
    "name": "Steve Newton"
  },
  {
    "name": "Johnny Campos"
  },
  {
    "name": "Tammy Ryan"
  },
  {
    "name": "Crystal Whitehead"
  },
  {
    "name": "Charles Taylor"
  },
  {
    "name": "Connie Lawrence"
  }
]
```

#### Additional Information

- **Category:** aggregation
- **Difficulty:** medium
- **Tokens Used:** 1,052
- **Execution Time:** 5.75s
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
- **Tokens Used:** 750
- **Execution Time:** 5.52s
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
WHERE toLower(j.title) =~ '.*eacher$'
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
- **Tokens Used:** 6,195
- **Execution Time:** 5.97s
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
MATCH (p:Person)-[:LIVES_IN]->(l:Location)<-[:LIVED_IN]-(p)
WHERE toLower(p.birthPlace) = toLower(l.name)
  AND NOT EXISTS((p)-[:LIVED_IN]->(l2:Location) WHERE l2 <> l AND l2.id > l.id)
RETURN p.firstName, p.lastName, l.name AS currentCity
ORDER BY p.lastName, p.firstName
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'WHERE': expected an expression, ')' or ',' (line 3, column 49 (offset: 154))
"  AND NOT EXISTS((p)-[:LIVED_IN]->(l2:Location) WHERE l2 <> l AND l2.id > l.id)"
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
- **Tokens Used:** 776
- **Execution Time:** 6.51s
- **Syntactic Correct:** Yes
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
       COLLECT(f.name) AS SharedFields
ORDER BY SIZE(SharedFields) DESC
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
- **Tokens Used:** 783
- **Execution Time:** 6.40s
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
RETURN DISTINCT p.firstName AS PalindromicFirstName
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
- **Tokens Used:** 6,742
- **Execution Time:** 6.85s
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
- **Tokens Used:** 2,120
- **Execution Time:** 4.79s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 62: 63
**Status:** FAIL

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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It should therefore only be used in contexts that evaluate to a boolean, e.g. inside the function exists() or in a WHERE-clause. No other uses are allowed, instead they should be replaced by a pattern comprehension. (line 7, column 8 (offset: 177))
"       (p)-[:IS_PARENT]->(child),"
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

### Test Case 63: 64
**Status:** PASS

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
WHERE p1.id < p2.id
MATCH (p1)-[l1:LIVES_IN]->(loc1:Location)
MATCH (p2)-[l2:LIVES_IN]->(loc2:Location)
WHERE loc1.id <> loc2.id
RETURN p1.firstName + ' ' + p1.lastName AS Partner1, 
       p2.firstName + ' ' + p2.lastName AS Partner2, 
       loc1.name AS City1, 
       loc2.name AS City2
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
    "Partner1": "Mia Sutton",
    "Partner2": "Michael Robinson",
    "City1": "Stephaniemouth",
    "City2": "Perryborough"
  },
  {
    "Partner1": "Joseph Maddox",
    "Partner2": "Jessica Chavez",
    "City1": "Lake Michelle",
    "City2": "Simsview"
  },
  {
    "Partner1": "Charles Taylor",
    "Partner2": "Johnny Campos",
    "City1": "Simsview",
    "City2": "Stephaniemouth"
  },
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
    "Partner1": "Juan Calderon",
    "Partner2": "Savannah Delacruz",
    "City1": "North Robert",
    "City2": "Karenview"
  }
]
```

#### Additional Information

- **Category:** pattern_matching
- **Difficulty:** medium
- **Tokens Used:** 2,880
- **Execution Time:** 7.17s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: A pattern expression should only be used in order to test the existence of a pattern. It should therefore only be used in contexts that evaluate to a boolean, e.g. inside the function exists() or in a WHERE-clause. No other uses are allowed, instead they should be replaced by a pattern comprehension. (line 6, column 8 (offset: 182))
"       (p1)-[:IS_FRIEND]->(p2),"
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

- **Category:** graph_recursion
- **Difficulty:** hard
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
- **Test Case Passed:** No
- **Infinite Loop:** No

---

### Test Case 65: 66
**Status:** FAIL

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
WITH DISTINCT p, s.degree AS degree
RETURN degree, COUNT(p) AS count
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
    "degree": "Bachelor",
    "count": 31
  },
  {
    "degree": "PhD",
    "count": 3
  },
  {
    "degree": "Master",
    "count": 1
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 773
- **Execution Time:** 5.13s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
- **Tokens Used:** 744
- **Execution Time:** 5.43s
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
- **Tokens Used:** 724
- **Execution Time:** 5.76s
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
- **Tokens Used:** 754
- **Execution Time:** 6.77s
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
- **Tokens Used:** 742
- **Execution Time:** 4.59s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: Variable `birthTimestamp` not defined (line 7, column 57 (offset: 312))
"AND apoc.date.parse(p2.birthDate, 'ms', 'yyyy-MM-dd') = birthTimestamp"
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
- **Difficulty:** easy
- **Tokens Used:** 0
- **Execution Time:** 0.00s
- **Syntactic Correct:** No
- **Execution Success:** No
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
- **Tokens Used:** 3,766
- **Execution Time:** 3.96s
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
RETURN DISTINCT f.name AS fieldOfStudy
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
- **Tokens Used:** 2,055
- **Execution Time:** 4.68s
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
- **Tokens Used:** 747
- **Execution Time:** 4.83s
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
- **Tokens Used:** 743
- **Execution Time:** 9.58s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
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
WHERE s.endYear = 2016 AND toLower(s.status) = 'graduated'
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
- **Tokens Used:** 2,774
- **Execution Time:** 6.05s
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
None
```

#### Error Analysis
```
Error in test case execution: Object of type Date is not JSON serializable
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
- **Execution Time:** 7.82s
- **Syntactic Correct:** No
- **Execution Success:** No
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
RETURN p.firstName + ' ' + p.lastName AS name, e.name AS university, s.startYear, s.endYear, s.endYear - s.startYear AS studyDuration
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 780
- **Execution Time:** 5.84s
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
None
```

#### Error Analysis
```
Context retrieval failed: {code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'w1'. (line 11, column 14 (offset: 345))
"       (p1)-[w1]->(c1),"
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
RETURN DISTINCT p.firstName, p.lastName, e.name AS institution, c.name AS company,
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
    "institution": "Priceshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1994,
    "studyEndYear": 1999
  },
  {
    "p.firstName": "Charles",
    "p.lastName": "Taylor",
    "institution": "Priceshire Institute",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1954,
    "studyEndYear": 1957
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institution": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1970,
    "studyEndYear": 1975
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institution": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1970,
    "studyEndYear": 1979
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "institution": "Smithstad University",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1976,
    "studyEndYear": 1979
  },
  {
    "p.firstName": "Christopher",
    "p.lastName": "Miller",
    "institution": "Castanedachester Institute",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1948,
    "studyEndYear": 1953
  },
  {
    "p.firstName": "Connie",
    "p.lastName": "Lawrence",
    "institution": "Castanedachester Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1949,
    "studyEndYear": 1953
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institution": "Priceshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2019
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institution": "Priceshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 2016,
    "studyEndYear": 2019
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institution": "Port Nicoleshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2021
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institution": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 2016,
    "studyEndYear": 2021
  },
  {
    "p.firstName": "Dana",
    "p.lastName": "Douglas",
    "institution": "Castanedachester Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 2012,
    "studyEndYear": 2015
  },
  {
    "p.firstName": "David",
    "p.lastName": "Lee",
    "institution": "Castanedachester Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 1970,
    "studyEndYear": 1972
  },
  {
    "p.firstName": "Debra",
    "p.lastName": "Clark",
    "institution": "Port Nicoleshire Institute",
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 2001,
    "studyEndYear": 2004
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "institution": "Smithstad University",
    "company": "Williams, Johnson and Wright",
    "workStartYear": 1990,
    "studyEndYear": 1991
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "institution": "Smithstad University",
    "company": "Stuart, Higgins and Strickland",
    "workStartYear": 1986,
    "studyEndYear": 1991
  },
  {
    "p.firstName": "Eric",
    "p.lastName": "Ortiz",
    "institution": "Smithstad University",
    "company": "Johnson-Rogers",
    "workStartYear": 1978,
    "studyEndYear": 1980
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "institution": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1961,
    "studyEndYear": 1967
  },
  {
    "p.firstName": "Johnny",
    "p.lastName": "Campos",
    "institution": "Port Nicoleshire Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1966,
    "studyEndYear": 1967
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "institution": "South Jeffrey Institute",
    "company": "Ruiz Ltd",
    "workStartYear": 1995,
    "studyEndYear": 1997
  },
  {
    "p.firstName": "Samuel",
    "p.lastName": "Wagner",
    "institution": "Priceshire Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2015,
    "studyEndYear": 2016
  },
  {
    "p.firstName": "Scott",
    "p.lastName": "Walker",
    "institution": "Priceshire Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1962,
    "studyEndYear": 1965
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Patton",
    "institution": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1955,
    "studyEndYear": 1956
  },
  {
    "p.firstName": "Tammy",
    "p.lastName": "Ryan",
    "institution": "Priceshire Institute",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2002,
    "studyEndYear": 2003
  },
  {
    "p.firstName": "Theresa",
    "p.lastName": "Vazquez",
    "institution": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1956,
    "studyEndYear": 1957
  },
  {
    "p.firstName": "Thomas",
    "p.lastName": "Schmidt",
    "institution": "South Jeffrey Institute",
    "company": "Rogers-Hobbs",
    "workStartYear": 1946,
    "studyEndYear": 1950
  },
  {
    "p.firstName": "Timothy",
    "p.lastName": "Walls",
    "institution": "Smithstad University",
    "company": "Rogers-Hobbs",
    "workStartYear": 1982,
    "studyEndYear": 1984
  },
  {
    "p.firstName": "Todd",
    "p.lastName": "Wilson",
    "institution": "South Jeffrey Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 2006,
    "studyEndYear": 2009
  },
  {
    "p.firstName": "Tracey",
    "p.lastName": "Hickman",
    "institution": "Smithstad University",
    "company": "Patterson, Camacho and White",
    "workStartYear": 2009,
    "studyEndYear": 2013
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "institution": "Priceshire Institute",
    "company": "Wilson, Gould and Marshall",
    "workStartYear": 1981,
    "studyEndYear": 1984
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 5,533
- **Execution Time:** 6.05s
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
MATCH (f:FieldOfStudy)<-[s:STUDIED]-(p:Person)
WHERE s.startYear IS NOT NULL AND s.endYear IS NOT NULL
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
- **Tokens Used:** 3,832
- **Execution Time:** 5.32s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
      (parent)-[pw:WORKED_AT]->(company:Company),
      (child)-[cw:WORKED_AT]->(company)
WHERE pw.status = 'Current' AND cw.status = 'Current'
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
- **Tokens Used:** 3,131
- **Execution Time:** 7.54s
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
MATCH (p1:Person)-[:IS_PARENT*1..3]->(p2:Person),
      (p1)-[:STUDIED_AT]->(uni:EducationalInstitution),
      (p2)-[:STUDIED_AT]->(uni)
WHERE toLower(p1.firstName) <> toLower(p2.firstName)
  AND toLower(p1.lastName) = toLower(p2.lastName)
RETURN DISTINCT p1.firstName + ' ' + p1.lastName AS parent,
       p2.firstName + ' ' + p2.lastName AS descendant,
       uni.name AS university
ORDER BY parent, descendant, university
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
- **Tokens Used:** 1,030
- **Execution Time:** 6.81s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
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
MATCH (p:Person)-[:LIVED_IN]->(l:Location)
WHERE l.country <> p.birthPlace
WITH p, l
MATCH (p)-[:LIVES_IN]->(current:Location)
WHERE current.country = p.birthPlace AND current.country <> l.country
RETURN p.firstName, p.lastName, p.birthPlace, l.country AS foreignCountry, current.country AS currentCountry
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
- **Tokens Used:** 795
- **Execution Time:** 7.41s
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
None
```

#### Error Analysis
```
Error in test case execution: Object of type frozenset is not JSON serializable
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
- **Execution Time:** 10.63s
- **Syntactic Correct:** No
- **Execution Success:** No
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
MATCH (p:Person)-[l:LIVES_IN]->(loc:Location)
WHERE NOT EXISTS((p)-[:LIVED_IN]->(:Location))
RETURN p.firstName, p.lastName, loc.name
ORDER BY p.firstName, p.lastName
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
    "p.firstName": "Angel",
    "p.lastName": "Riggs",
    "loc.name": "Simsview"
  },
  {
    "p.firstName": "Anna",
    "p.lastName": "Davis",
    "loc.name": "Lake Michelle"
  },
  {
    "p.firstName": "Brandi",
    "p.lastName": "Bailey",
    "loc.name": "Lake Justinview"
  },
  {
    "p.firstName": "Cheryl",
    "p.lastName": "Robinson",
    "loc.name": "North Robert"
  },
  {
    "p.firstName": "David",
    "p.lastName": "Brown",
    "loc.name": "Perryborough"
  },
  {
    "p.firstName": "Donald",
    "p.lastName": "Jones",
    "loc.name": "Rivasside"
  },
  {
    "p.firstName": "Jared",
    "p.lastName": "David",
    "loc.name": "Rivasside"
  },
  {
    "p.firstName": "Jeffrey",
    "p.lastName": "Henderson",
    "loc.name": "Stephaniemouth"
  },
  {
    "p.firstName": "Jessica",
    "p.lastName": "Chavez",
    "loc.name": "Simsview"
  },
  {
    "p.firstName": "Jordan",
    "p.lastName": "Gonzalez",
    "loc.name": "Simsview"
  },
  {
    "p.firstName": "Logan",
    "p.lastName": "Archer",
    "loc.name": "Simsview"
  },
  {
    "p.firstName": "Matthew",
    "p.lastName": "Marshall",
    "loc.name": "East Patrick"
  },
  {
    "p.firstName": "Mia",
    "p.lastName": "Sutton",
    "loc.name": "Stephaniemouth"
  },
  {
    "p.firstName": "Michael",
    "p.lastName": "Robinson",
    "loc.name": "Perryborough"
  },
  {
    "p.firstName": "Nathaniel",
    "p.lastName": "Khan",
    "loc.name": "Rivasside"
  },
  {
    "p.firstName": "Rachel",
    "p.lastName": "Graham",
    "loc.name": "East Patrick"
  },
  {
    "p.firstName": "Timothy",
    "p.lastName": "Walls",
    "loc.name": "Stephaniemouth"
  },
  {
    "p.firstName": "William",
    "p.lastName": "Brady",
    "loc.name": "Patricialand"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 2,611
- **Execution Time:** 5.10s
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
WITH c
ORDER BY c.employees ASC
LIMIT 1
RETURN c.name AS CompanyName, c.employees AS NumberOfEmployees
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
    "NumberOfEmployees": 92460
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 938
- **Execution Time:** 5.10s
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
- **Tokens Used:** 721
- **Execution Time:** 4.54s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
- **Infinite Loop:** No

---

### Test Case 89: 90
**Status:** PASS

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
MATCH (ei:EducationalInstitution)
WHERE ei.type = 'College'
RETURN ei.name, ei.country, ei.foundedYear
ORDER BY ei.name
```

#### Results Comparison

**Expected Results:**
```json
[
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
    "ei.name": "Castanedachester Institute",
    "ei.country": "Mauritania",
    "ei.foundedYear": 1730
  },
  {
    "ei.name": "Port Nicoleshire Institute",
    "ei.country": "Hong Kong",
    "ei.foundedYear": 1571
  },
  {
    "ei.name": "Smithstad University",
    "ei.country": "French Southern Territories",
    "ei.foundedYear": 1787
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 3,398
- **Execution Time:** 4.58s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** Yes
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
  AND NOT EXISTS((p)-[:HAD_POSITION]->(:JobTitle) WHERE p.HAD_POSITION.endYear IS NULL)
RETURN p.firstName, p.lastName, p.id
```

#### Error Analysis
```
{code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'WHERE': expected an expression, ')' or ',' (line 3, column 51 (offset: 134))
"  AND NOT EXISTS((p)-[:HAD_POSITION]->(:JobTitle) WHERE p.HAD_POSITION.endYear IS NULL)"
                                                   ^}
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
[]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 824
- **Execution Time:** 6.45s
- **Syntactic Correct:** Yes
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
- **Tokens Used:** 5,051
- **Execution Time:** 5.38s
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
  AND toInteger(substring(p1.birthDate, 0, 4)) / 10 * 10 = toInteger(substring(p2.birthDate, 0, 4)) / 10 * 10
RETURN p1.firstName + ' ' + p1.lastName AS Person1,
       p2.firstName + ' ' + p2.lastName AS Person2,
       toInteger(substring(p1.birthDate, 0, 4)) / 10 * 10 AS Decade
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
- **Tokens Used:** 1,775
- **Execution Time:** 6.87s
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
RETURN l.name, l.country, l.population
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
    "l.name": "Stephaniemouth",
    "l.country": "New Zealand",
    "l.population": 11636146
  },
  {
    "l.name": "Rivasside",
    "l.country": "Kiribati",
    "l.population": 3376763
  },
  {
    "l.name": "Lake Michelle",
    "l.country": "Korea",
    "l.population": 9619364
  },
  {
    "l.name": "Karenview",
    "l.country": "Seychelles",
    "l.population": 13126125
  },
  {
    "l.name": "Simsview",
    "l.country": "Kazakhstan",
    "l.population": 9234763
  },
  {
    "l.name": "Lake Justinview",
    "l.country": "Grenada",
    "l.population": 6060072
  },
  {
    "l.name": "Patricialand",
    "l.country": "Burundi",
    "l.population": 12819117
  },
  {
    "l.name": "East Patrick",
    "l.country": "Cape Verde",
    "l.population": 4875083
  },
  {
    "l.name": "North Robert",
    "l.country": "Greenland",
    "l.population": 530926
  },
  {
    "l.name": "Perryborough",
    "l.country": "Syrian Arab Republic",
    "l.population": 10639534
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 3,852
- **Execution Time:** 5.33s
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
- **Tokens Used:** 1,724
- **Execution Time:** 5.51s
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
MATCH (p1:Person)-[:IS_FRIEND]-(p2:Person)
WHERE id(p1) < id(p2)
WITH p1, p2
MATCH (p1)-[l1:LIVED_IN]->(loc:Location)
WITH p1, p2, collect({loc: loc, start: l1.startYear, end: l1.endYear}) AS p1Locations
MATCH (p2)-[l2:LIVED_IN]->(loc:Location)
WITH p1, p2, p1Locations, collect({loc: loc, start: l2.startYear, end: l2.endYear}) AS p2Locations
WHERE NONE(loc1 IN p1Locations WHERE ANY(loc2 IN p2Locations WHERE 
    loc1.loc = loc2.loc AND 
    ((loc1.start <= loc2.start AND loc1.end >= loc2.start) OR
     (loc2.start <= loc1.start AND loc2.end >= loc1.start))
))
RETURN p1.firstName + ' ' + p1.lastName AS Person1, p2.firstName + ' ' + p2.lastName AS Person2
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
    "Person1": "Kevin Johnson",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Stephanie Martin",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Thomas Schmidt",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Samuel Wagner",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Andrew Diaz",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Eric Ortiz",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Tammy Patton",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Christopher Miller",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Savannah Delacruz",
    "Person2": "Thomas Schmidt"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Vanessa Patel",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Eugene Green",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Steve Newton",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "April Wise",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "April Wise",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Scott Walker",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Todd Wilson"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Debra Clark",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Johnny Campos",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Savannah Delacruz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Juan Calderon",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Tracey Hickman"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Stephanie Martin"
  },
  {
    "Person1": "Tanya Koch",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "April Wise"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Crystal Whitehead",
    "Person2": "Christopher Miller"
  },
  {
    "Person1": "David Lee",
    "Person2": "April Wise"
  },
  {
    "Person1": "David Lee",
    "Person2": "Theresa Vazquez"
  },
  {
    "Person1": "David Lee",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "David Lee",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Joseph Maddox"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Annette Pearson"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Samuel Wagner"
  },
  {
    "Person1": "Mark Johnson",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Johnny Campos"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Scott Walker"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Charles Taylor",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Connie Lawrence",
    "Person2": "Michael Orr"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "April Wise"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Tracey Hickman",
    "Person2": "Joseph Williams"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "April Wise"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Eric Ortiz"
  },
  {
    "Person1": "Annette Pearson",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Vanessa Patel"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Andrew Diaz"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Patton"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Tammy Ryan"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Dana Douglas"
  },
  {
    "Person1": "Joseph Maddox",
    "Person2": "Joseph Williams"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** medium
- **Tokens Used:** 10,309
- **Execution Time:** 10.68s
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
WITH split(p.birthDate, '-')[1] AS birthMonth, count(*) AS monthCount
ORDER BY monthCount DESC, birthMonth
RETURN birthMonth
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
    "birthMonth": "12"
  }
]
```

#### Additional Information

- **Category:** filtering
- **Difficulty:** easy
- **Tokens Used:** 857
- **Execution Time:** 4.33s
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
WITH count(DISTINCT p1) AS sameNameCount
RETURN sameNameCount
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
- **Tokens Used:** 758
- **Execution Time:** 5.22s
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
RETURN count(p) AS peopleFromSun
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
    "peopleFromSun": 0
  }
]
```

#### Additional Information

- **Category:** paradox
- **Difficulty:** easy
- **Tokens Used:** 1,385
- **Execution Time:** 4.52s
- **Syntactic Correct:** Yes
- **Execution Success:** Yes
- **Test Case Passed:** No
- **Infinite Loop:** No

---
