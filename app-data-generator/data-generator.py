import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
from neo4j import GraphDatabase

# Initialize Faker
Faker.seed(42)
fake = Faker()

# Neo4j connection setup
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "thesis2025")  # Replace with your credentials

driver = GraphDatabase.driver(URI, auth=AUTH)

# Configuration parameters
NUM_PERSONS = 50
NUM_LOCATIONS = 10
NUM_EDUCATIONAL_INSTITUTIONS = 5
NUM_COMPANIES = 8 
NUM_FIELDS_OF_STUDY = 5
NUM_JOB_TITLES = 10

# Helper functions for generating dates
def random_date(start_year=1920, end_year=2005):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def generate_person(person_id, birth_year_min=1920, birth_year_max=2005):
    gender = random.choice(['Male', 'Female'])
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    
    birth_date = random_date(birth_year_min, birth_year_max).strftime('%Y-%m-%d')
    
    return {
        'id': f'p{person_id}',
        'firstName': first_name,
        'lastName': fake.last_name(),
        'gender': gender,
        'birthDate': birth_date,
        'birthPlace': fake.city(),
        'email': fake.email(),
        'nationality': random.choice(['American', 'British', 'Canadian', 'Australian', 'German', 'French'])
    }

def generate_location(location_id):
    return {
        'id': f'loc{location_id}',
        'name': fake.city(),
        'type': 'City',
        'country': fake.country(),
        'population': random.randint(5000, 15000000)
    }

def generate_educational_institution(edu_id):
    types = ['University', 'College', 'Institute']
    return {
        'id': f'edu{edu_id}',
        'name': f"{fake.city()} {random.choice(types)}",
        'type': random.choice(types),
        'foundedYear': random.randint(1500, 2000),
        'country': fake.country()
    }

def generate_company(company_id):
    return {
        'id': f'comp{company_id}',
        'name': fake.company(),
        'industry': random.choice(['Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing', 'Retail']),
        'foundedYear': random.randint(1800, 2020),
        'headquarters': f"{fake.city()}, {fake.state_abbr()}",
        'employees': random.randint(10, 500000)
    }

def generate_field_of_study(field_id):
    fields = ['Computer Science', 'Business Administration', 'Medicine', 'Law', 'Engineering', 
             'Physics', 'Mathematics', 'Literature', 'History', 'Chemistry', 'Biology', 
             'Psychology', 'Sociology', 'Philosophy', 'Economics']
    categories = ['Science', 'Engineering', 'Arts', 'Humanities', 'Business']
    
    field = fields[field_id % len(fields)]
    
    return {
        'id': f'field{field_id}',
        'name': field,
        'category': random.choice(categories)
    }

def generate_job_title(job_id):
    titles = ['Software Engineer', 'Data Scientist', 'Manager', 'Director', 'CEO', 
             'CTO', 'CFO', 'Doctor', 'Lawyer', 'Teacher', 'Professor', 'Researcher',
             'Designer', 'Artist', 'Writer', 'Accountant', 'Analyst', 'Consultant',
             'Marketing Specialist', 'HR Manager', 'Product Manager', 'Sales Representative',
             'Customer Support', 'Project Manager', 'Architect']
    categories = ['Technology', 'Management', 'Healthcare', 'Education', 'Finance', 'Arts']
    
    title = titles[job_id % len(titles)]
    
    return {
        'id': f'job{job_id}',
        'title': title,
        'category': random.choice(categories)
    }

def create_family_generations(session):
    print("Generating multi-generational families...")
    
    # Creating family generations
    # We'll create families spanning 3-4 generations
    num_root_families = NUM_PERSONS // 30  # Each family tree will have about 30 people on average
    
    # Track all persons for relationship creation
    all_persons = []
    
    for family_idx in range(num_root_families):
        # Create grandparents (generation 1) - born between 1920-1950
        grandpa = generate_person(len(all_persons) + 1, 1920, 1950)
        all_persons.append(grandpa)
        
        grandma = generate_person(len(all_persons) + 1, 1920, 1950)
        all_persons.append(grandma)
        
        # Add marriage relationship between grandparents
        session.run("""
        MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
        CREATE (p1)-[:IS_HUSBAND]->(p2), (p2)-[:IS_WIFE]->(p1)
        """, id1=grandpa['id'], id2=grandma['id'])
        
        # Generate 2-4 children for grandparents (generation 2) - born between 1945-1975
        num_children = random.randint(2, 4)
        parents_children = []
        
        for i in range(num_children):
            child = generate_person(len(all_persons) + 1, 1945, 1975)
            all_persons.append(child)
            parents_children.append(child)
            
            # Add parent-child relationships
            session.run("""
            MATCH (parent1:Person {id: $parent1_id}), (parent2:Person {id: $parent2_id}), (child:Person {id: $child_id})
            CREATE (parent1)-[:IS_PARENT]->(child), (parent2)-[:IS_PARENT]->(child),
                   (child)-[:IS_CHILD]->(parent1), (child)-[:IS_CHILD]->(parent2)
            """, parent1_id=grandpa['id'], parent2_id=grandma['id'], child_id=child['id'])
            
            # Each child gets married
            spouse = generate_person(len(all_persons) + 1, 1945, 1975)
            all_persons.append(spouse)
            
            # Add marriage relationship
            if child['gender'] == 'Male':
                session.run("""
                MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                CREATE (p1)-[:IS_HUSBAND]->(p2), (p2)-[:IS_WIFE]->(p1)
                """, id1=child['id'], id2=spouse['id'])
            else:
                session.run("""
                MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                CREATE (p1)-[:IS_WIFE]->(p2), (p2)-[:IS_HUSBAND]->(p1)
                """, id1=child['id'], id2=spouse['id'])
            
            # Generation 3: Grandchildren - born between 1970-2000
            num_grandchildren = random.randint(1, 3)
            for j in range(num_grandchildren):
                grandchild = generate_person(len(all_persons) + 1, 1970, 2000)
                all_persons.append(grandchild)
                
                # Add parent-child relationships
                session.run("""
                MATCH (parent1:Person {id: $parent1_id}), (parent2:Person {id: $parent2_id}), (child:Person {id: $child_id})
                CREATE (parent1)-[:IS_PARENT]->(child), (parent2)-[:IS_PARENT]->(child),
                       (child)-[:IS_CHILD]->(parent1), (child)-[:IS_CHILD]->(parent2)
                """, parent1_id=child['id'], parent2_id=spouse['id'], child_id=grandchild['id'])
                
                # Some grandchildren get married and have kids (generation 4) if they're old enough
                if datetime.strptime(grandchild['birthDate'], '%Y-%m-%d').year < 1990:
                    if random.random() < 0.7:  # 70% chance of marriage
                        g_spouse = generate_person(len(all_persons) + 1, 1970, 2000)
                        all_persons.append(g_spouse)
                        
                        # Add marriage relationship
                        if grandchild['gender'] == 'Male':
                            session.run("""
                            MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                            CREATE (p1)-[:IS_HUSBAND]->(p2), (p2)-[:IS_WIFE]->(p1)
                            """, id1=grandchild['id'], id2=g_spouse['id'])
                        else:
                            session.run("""
                            MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                            CREATE (p1)-[:IS_WIFE]->(p2), (p2)-[:IS_HUSBAND]->(p1)
                            """, id1=grandchild['id'], id2=g_spouse['id'])
                        
                        # Generation 4: Great-grandchildren - born between 1990-2005
                        if random.random() < 0.6:  # 60% chance of having children
                            num_greatgrandchildren = random.randint(1, 2)
                            for k in range(num_greatgrandchildren):
                                greatgrandchild = generate_person(len(all_persons) + 1, 1990, 2005)
                                all_persons.append(greatgrandchild)
                                
                                # Add parent-child relationships
                                session.run("""
                                MATCH (parent1:Person {id: $parent1_id}), (parent2:Person {id: $parent2_id}), (child:Person {id: $child_id})
                                CREATE (parent1)-[:IS_PARENT]->(child), (parent2)-[:IS_PARENT]->(child),
                                       (child)-[:IS_CHILD]->(parent1), (child)-[:IS_CHILD]->(parent2)
                                """, parent1_id=grandchild['id'], parent2_id=g_spouse['id'], child_id=greatgrandchild['id'])
        
        # Add sibling relationships within each generation
        # Generation 2 siblings
        for i in range(len(parents_children)):
            for j in range(i+1, len(parents_children)):
                session.run("""
                MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                CREATE (p1)-[:IS_SIBLING]->(p2), (p2)-[:IS_SIBLING]->(p1)
                """, id1=parents_children[i]['id'], id2=parents_children[j]['id'])
    
    return all_persons

def create_friendship_network(session, persons):
    print("Creating friendship network...")
    
    # Each person will have 3-10 friends
    for person in persons:
        num_friends = random.randint(3, 10)
        potential_friends = [p for p in persons if p['id'] != person['id']]
        friends = random.sample(potential_friends, min(num_friends, len(potential_friends)))
        
        for friend in friends:
            # Avoid duplicate relationships by only creating friendship in one direction
            # The query will create it in both directions
            if person['id'] < friend['id']:
                # Random friendship start date
                start_date = random_date(2010, 2023).strftime('%Y-%m-%d')
                
                session.run("""
                MATCH (p1:Person {id: $id1}), (p2:Person {id: $id2})
                MERGE (p1)-[:IS_FRIEND {since: $since}]->(p2)
                MERGE (p2)-[:IS_FRIEND {since: $since}]->(p1)
                """, id1=person['id'], id2=friend['id'], since=start_date)

def create_education_relationships(session, persons, institutions, fields):
    print("Creating education relationships...")
    
    for person in persons:
        # Not everyone has higher education
        if random.random() < 0.7:  # 70% chance of having higher education
            num_degrees = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            
            birth_year = int(person['birthDate'].split('-')[0])
            
            for i in range(num_degrees):
                institution = random.choice(institutions)
                field = random.choice(fields)
                
                # Calculate education dates based on person's age
                # Bachelor's starts at ~18-20
                start_year = birth_year + 18 + i*3 + random.randint(0, 2)
                if start_year > 2020:  # Don't create future education
                    continue
                    
                degree_type = random.choice(['Bachelor', 'Master', 'PhD']) if i > 0 else 'Bachelor'
                end_year = start_year + (2 if degree_type == 'Master' else 4 if degree_type == 'Bachelor' else 5)
                
                if end_year > 2023:  # Set current students
                    status = 'Current'
                    end_year = None
                else:
                    status = 'Graduated'
                
                # Create studied at relationship
                session.run("""
                MATCH (p:Person {id: $person_id}), (i:EducationalInstitution {id: $institution_id}), (f:FieldOfStudy {id: $field_id})
                CREATE (p)-[:STUDIED_AT {
                    startYear: $start_year, 
                    endYear: $end_year,
                    degree: $degree_type,
                    status: $status
                }]->(i),
                (p)-[:STUDIED {
                    startYear: $start_year, 
                    endYear: $end_year,
                    degree: $degree_type
                }]->(f)
                """, person_id=person['id'], institution_id=institution['id'], field_id=field['id'],
                     start_year=start_year, end_year=end_year, degree_type=degree_type, status=status)

def create_work_relationships(session, persons, companies, job_titles):
    print("Creating work relationships...")
    
    for person in persons:
        birth_year = int(person['birthDate'].split('-')[0])
        work_start_age = random.randint(18, 25)  # Age when person started working
        work_start_year = birth_year + work_start_age
        
        if work_start_year > 2023:  # Person is too young to work
            continue
        
        # Number of jobs in career so far
        career_length = 2023 - work_start_year
        num_jobs = min(1 + career_length // 4, 7)  # Roughly changing jobs every 4 years, max 7 jobs
        
        current_year = work_start_year
        
        for i in range(num_jobs):
            company = random.choice(companies)
            job_title = random.choice(job_titles)
            
            # Each job lasts 2-5 years unless it's the current job
            job_duration = random.randint(2, 5)
            start_year = current_year
            
            if i == num_jobs - 1 or start_year + job_duration > 2023:
                # This is the current job
                end_year = None
                status = 'Current'
            else:
                end_year = start_year + job_duration
                status = 'Former'
                current_year = end_year + random.randint(0, 1)  # 0-1 year gap between jobs
            
            # Create employment relationship
            session.run("""
            MATCH (p:Person {id: $person_id}), (c:Company {id: $company_id}), (j:JobTitle {id: $job_id})
            CREATE (p)-[:WORKED_AT {
                startYear: $start_year,
                endYear: $end_year,
                status: $status
            }]->(c),
            (p)-[:HAD_POSITION {
                startYear: $start_year,
                endYear: $end_year,
                companyId: $company_id
            }]->(j)
            """, person_id=person['id'], company_id=company['id'], job_id=job_title['id'],
                 start_year=start_year, end_year=end_year, status=status)

def create_location_relationships(session, persons, locations):
    print("Creating location relationships...")

    for person in persons:
        # Current living location
        current_location = random.choice(locations)

        # Create lives in relationship
        session.run("""
        MATCH (p:Person {id: $person_id}), (l:Location {id: $location_id})
        CREATE (p)-[:LIVES_IN {since: $since}]->(l)
        """, person_id=person['id'], location_id=current_location['id'],
                    since=random_date(2000, 2023).strftime('%Y-%m-%d'))

        # Some people have previously lived in other locations
        if random.random() < 0.7:  # 70% chance of having lived elsewhere
            num_previous_locations = random.randint(1, 3)
            previous_locations = random.sample([loc for loc in locations if loc['id'] != current_location['id']],
                                                min(num_previous_locations, len(locations)-1))

            birth_year = int(person['birthDate'].split('-')[0])
            min_moving_age = 18  # Minimum age when a person might move

            for prev_loc in previous_locations:
                earliest_possible_move = birth_year + min_moving_age
                latest_possible_start = 2020

                if earliest_possible_move <= latest_possible_start:
                    start_year = random.randint(earliest_possible_move, latest_possible_start)
                    end_year = random.randint(start_year + 1, 2022)

                    # Create previously lived in relationship
                    session.run("""
                    MATCH (p:Person {id: $person_id}), (l:Location {id: $location_id})
                    CREATE (p)-[:LIVED_IN {startYear: $start_year, endYear: $end_year}]->(l)
                    """, person_id=person['id'], location_id=prev_loc['id'],
                                start_year=start_year, end_year=end_year)

def create_nodes(session):
    print("Creating nodes in database...")
    
    # Create Person nodes
    persons = []
    for i in range(NUM_PERSONS):
        person = generate_person(i + 1)
        persons.append(person)
        
        session.run("""
        CREATE (p:Person {
            id: $id,
            firstName: $firstName,
            lastName: $lastName,
            gender: $gender,
            birthDate: $birthDate,
            birthPlace: $birthPlace,
            email: $email,
            nationality: $nationality
        })
        """, **person)
    
    # Create Location nodes
    locations = []
    for i in range(NUM_LOCATIONS):
        location = generate_location(i + 1)
        locations.append(location)
        
        session.run("""
        CREATE (l:Location {
            id: $id,
            name: $name,
            type: $type,
            country: $country,
            population: $population
        })
        """, **location)
    
    # Create Educational Institution nodes
    institutions = []
    for i in range(NUM_EDUCATIONAL_INSTITUTIONS):
        institution = generate_educational_institution(i + 1)
        institutions.append(institution)
        
        session.run("""
        CREATE (e:EducationalInstitution {
            id: $id,
            name: $name,
            type: $type,
            foundedYear: $foundedYear,
            country: $country
        })
        """, **institution)
    
    # Create Company nodes
    companies = []
    for i in range(NUM_COMPANIES):
        company = generate_company(i + 1)
        companies.append(company)
        
        session.run("""
        CREATE (c:Company {
            id: $id,
            name: $name,
            industry: $industry,
            foundedYear: $foundedYear,
            headquarters: $headquarters,
            employees: $employees
        })
        """, **company)
    
    # Create Field of Study nodes
    fields = []
    for i in range(NUM_FIELDS_OF_STUDY):
        field = generate_field_of_study(i + 1)
        fields.append(field)
        
        session.run("""
        CREATE (f:FieldOfStudy {
            id: $id,
            name: $name,
            category: $category
        })
        """, **field)
    
    # Create JobTitle nodes
    job_titles = []
    for i in range(NUM_JOB_TITLES):
        job_title = generate_job_title(i + 1)
        job_titles.append(job_title)
        
        session.run("""
        CREATE (j:JobTitle {
            id: $id,
            title: $title,
            category: $category
        })
        """, **job_title)
    
    return persons, locations, institutions, companies, fields, job_titles

def create_indexes(session):
    print("Creating indexes...")
    
    # Create indexes for faster lookups
    session.run("CREATE INDEX person_id FOR (p:Person) ON (p.id)")
    session.run("CREATE INDEX location_id FOR (l:Location) ON (l.id)")
    session.run("CREATE INDEX institution_id FOR (e:EducationalInstitution) ON (e.id)")
    session.run("CREATE INDEX company_id FOR (c:Company) ON (c.id)")
    session.run("CREATE INDEX field_id FOR (f:FieldOfStudy) ON (f.id)")
    session.run("CREATE INDEX job_id FOR (j:JobTitle) ON (j.id)")


def clear_database(session):
    print("Clearing previous data...")
    session.run("MATCH (n) DETACH DELETE n")
    
    # Drop all indexes
    session.run("DROP INDEX person_id IF EXISTS")
    session.run("DROP INDEX location_id IF EXISTS")
    session.run("DROP INDEX institution_id IF EXISTS")
    session.run("DROP INDEX company_id IF EXISTS")
    session.run("DROP INDEX field_id IF EXISTS")
    session.run("DROP INDEX job_id IF EXISTS")


def get_graph_schema_with_examples(session):
    """
    Retrieves the graph schema including node labels, relationship types, and properties
    with example values for each.
    """
    print("Retrieving graph schema with examples...")
    schema = {}

    # Get node labels and their properties with examples
    node_labels_query = """
    CALL db.labels() YIELD label
    CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN properties(n) AS props LIMIT 1', null) YIELD value
    RETURN label, value.props AS exampleProperties
    """
    node_labels_result = session.run(node_labels_query)
    schema['nodes'] = {}
    for record in node_labels_result:
        label = record['label']
        example_properties = record['exampleProperties']
        schema['nodes'][label] = example_properties

    # Get relationship types and their properties with examples
    relationship_types_query = """
    CALL db.relationshipTypes() YIELD relationshipType
    CALL apoc.cypher.run('MATCH ()-[r:`' + relationshipType + '`]->() RETURN properties(r) AS props LIMIT 1', null) YIELD value
    RETURN relationshipType, value.props AS exampleProperties
    """
    relationship_types_result = session.run(relationship_types_query)
    schema['relationships'] = {}
    for record in relationship_types_result:
        rel_type = record['relationshipType']
        example_properties = record['exampleProperties']
        schema['relationships'][rel_type] = example_properties

    return schema




def get_generator_schema_as_string():
    """
    Analyzes the generator functions to provide a concise schema definition for an LLM.
    Focuses on Label/Type, Properties, Data Types, and Possible Values/Ranges,
    without exposing the internal Faker library usage.
    """
    schema_parts = []
    schema_parts.append("## Neo4j Graph Schema Definition (Generator Logic)")

    # --- Node Definitions ---
    schema_parts.append("\n### Nodes:")

    # Person
    schema_parts.append(f"- **Person**: {{")
    schema_parts.append(f"    id: string (Format: p<integer>)")
    schema_parts.append(f"    firstName: string (Common English male/female first names)")
    schema_parts.append(f"    lastName: string (Common English last names)")
    schema_parts.append(f"    gender: string (['Male', 'Female'])")
    schema_parts.append(f"    birthDate: string (YYYY-MM-DD, Range: 1920-2005)")
    schema_parts.append(f"    birthPlace: string (Real-world city names)")
    schema_parts.append(f"    email: string (Standard email address format, e.g., user@example.com)")
    schema_parts.append(f"    nationality: string (['American', 'British', 'Canadian', 'Australian', 'German', 'French'])")
    schema_parts.append(f"}}")

    # Location
    schema_parts.append(f"- **Location**: {{")
    schema_parts.append(f"    id: string (Format: loc<integer>)")
    schema_parts.append(f"    name: string (Real-world city names)")
    schema_parts.append(f"    type: string (Fixed: 'City')")
    schema_parts.append(f"    country: string (Real-world country names)")
    schema_parts.append(f"    population: integer (Range: 5,000 - 15,000,000)")
    schema_parts.append(f"}}")

    # EducationalInstitution
    schema_parts.append(f"- **EducationalInstitution**: {{")
    schema_parts.append(f"    id: string (Format: edu<integer>)")
    schema_parts.append(f"    name: string (Format: <city> <University|College|Institute>)")
    schema_parts.append(f"    type: string (['University', 'College', 'Institute'])")
    schema_parts.append(f"    foundedYear: integer (Range: 1500 - 2000)")
    schema_parts.append(f"    country: string (Real-world country names)")
    schema_parts.append(f"}}")

    # Company
    schema_parts.append(f"- **Company**: {{")
    schema_parts.append(f"    id: string (Format: comp<integer>)")
    schema_parts.append(f"    name: string (Realistic company names)")
    schema_parts.append(f"    industry: string (['Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing', 'Retail'])")
    schema_parts.append(f"    foundedYear: integer (Range: 1800 - 2020)")
    schema_parts.append(f"    headquarters: string (Format: <city>, <state/province abbreviation>)")
    schema_parts.append(f"    employees: integer (Range: 10 - 500,000)")
    schema_parts.append(f"}}")

    # FieldOfStudy
    all_fields = ['Computer Science', 'Business Administration', 'Medicine', 'Law', 'Engineering',
                  'Physics', 'Mathematics', 'Literature', 'History', 'Chemistry', 'Biology',
                  'Psychology', 'Sociology', 'Philosophy', 'Economics']
    all_categories_field = ['Science', 'Engineering', 'Arts', 'Humanities', 'Business']
    schema_parts.append(f"- **FieldOfStudy**: {{")
    schema_parts.append(f"    id: string (Format: field<integer>)")
    schema_parts.append(f"    name: string ({all_fields})")
    schema_parts.append(f"    category: string ({all_categories_field})")
    schema_parts.append(f"}}")

    # JobTitle
    all_titles = ['Software Engineer', 'Data Scientist', 'Manager', 'Director', 'CEO',
                  'CTO', 'CFO', 'Doctor', 'Lawyer', 'Teacher', 'Professor', 'Researcher',
                  'Designer', 'Artist', 'Writer', 'Accountant', 'Analyst', 'Consultant',
                  'Marketing Specialist', 'HR Manager', 'Product Manager', 'Sales Representative',
                  'Customer Support', 'Project Manager', 'Architect']
    all_categories_job = ['Technology', 'Management', 'Healthcare', 'Education', 'Finance', 'Arts']
    schema_parts.append(f"- **JobTitle**: {{")
    schema_parts.append(f"    id: string (Format: job<integer>)")
    schema_parts.append(f"    title: string ({all_titles})")
    schema_parts.append(f"    category: string ({all_categories_job})")
    schema_parts.append(f"}}")

    # --- Relationship Definitions ---
    schema_parts.append("\n### Relationships:")

    schema_parts.append(f"- **(:Person)-[IS_HUSBAND]->(:Person)**: No properties.")
    schema_parts.append(f"- **(:Person)-[IS_WIFE]->(:Person)**: No properties.")
    schema_parts.append(f"- **(:Person)-[IS_PARENT]->(:Person)**: No properties.")
    schema_parts.append(f"- **(:Person)-[IS_CHILD]->(:Person)**: No properties.")
    schema_parts.append(f"- **(:Person)-[IS_SIBLING]-(:Person)**: No properties.")

    schema_parts.append(f"- **(:Person)-[IS_FRIEND]-(:Person)**: {{")
    schema_parts.append(f"    since: string (YYYY-MM-DD, Range: 2010-2023)")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[STUDIED_AT]->(:EducationalInstitution)**: {{")
    schema_parts.append(f"    startYear: integer (Range: Person's birth year + 18 to 20 + offset)")
    schema_parts.append(f"    endYear: integer/null (Range: startYear + 2/4/5 years or null for 'Current' status)")
    schema_parts.append(f"    degree: string (['Bachelor', 'Master', 'PhD'])")
    schema_parts.append(f"    status: string (['Current', 'Graduated'])")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[STUDIED]->(:FieldOfStudy)**: {{")
    schema_parts.append(f"    startYear: integer (Range: Person's birth year + 18 to 20 + offset)")
    schema_parts.append(f"    endYear: integer/null (Range: startYear + 2/4/5 years or null for 'Current' status)")
    schema_parts.append(f"    degree: string (['Bachelor', 'Master', 'PhD'])")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[WORKED_AT]->(:Company)**: {{")
    schema_parts.append(f"    startYear: integer (Range: Person's birth year + 18 to 25)")
    schema_parts.append(f"    endYear: integer/null (Range: startYear + 2-5 years or null for 'Current' status)")
    schema_parts.append(f"    status: string (['Current', 'Former'])")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[HAD_POSITION]->(:JobTitle)**: {{")
    schema_parts.append(f"    startYear: integer (Range: Person's birth year + 18 to 25)")
    schema_parts.append(f"    endYear: integer/null (Range: startYear + 2-5 years or null for 'Current' status)")
    schema_parts.append(f"    companyId: string (Refers to Company.id)")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[LIVES_IN]->(:Location)**: {{")
    schema_parts.append(f"    since: string (YYYY-MM-DD, Range: 2000-2023)")
    schema_parts.append(f"}}")

    schema_parts.append(f"- **(:Person)-[LIVED_IN]->(:Location)**: {{")
    schema_parts.append(f"    startYear: integer (Range: Person's birth year + 18 to 2020)")
    schema_parts.append(f"    endYear: integer (Range: startYear + 1 to 2022)")
    schema_parts.append(f"}}")

    return "\n".join(schema_parts)


def main():

    schema = get_generator_schema_as_string()
    print(schema)

    filename = "generated_schema.txt"



    with open(filename, "w", encoding="utf-8") as f:
            f.write(schema)
    
    # with driver.session() as session:


        # # Clear any existing data
        # clear_database(session)
        
        # # Create indexes for better performance
        # create_indexes(session)
        
        # # Create nodes
        # persons, locations, institutions, companies, fields, job_titles = create_nodes(session)
        
        # # Create family relationships
        # all_persons = create_family_generations(session)
        
        # # Create friendship network
        # create_friendship_network(session, persons)
        
        # # Create education relationships
        # create_education_relationships(session, persons, institutions, fields)
        
        # # Create work relationships
        # create_work_relationships(session, persons, companies, job_titles)
        
        # # Create location relationships
        # create_location_relationships(session, persons, locations)
        
        # print(f"Successfully created graph database with:")
        # print(f"- {NUM_PERSONS} persons")
        # print(f"- {NUM_LOCATIONS} locations")
        # print(f"- {NUM_EDUCATIONAL_INSTITUTIONS} educational institutions")
        # print(f"- {NUM_COMPANIES} companies")
        # print(f"- {NUM_FIELDS_OF_STUDY} fields of study")
        # print(f"- {NUM_JOB_TITLES} job titles")
        # print("And numerous relationships between them.")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.close()
