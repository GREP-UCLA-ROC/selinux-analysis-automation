# Review of SELinux Policy Analysis Tools

## Contributors

| Contributor | Affiliation                                                                                         | Google Scholar                                                          |
| ----------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Amir Eaman  | [University of Ottawa](https://www.uottawa.ca/en) | [Profile](https://scholar.google.com/citations?user=4GTciD8AAAAJ&hl=en) |
| Mark Lee    | [University of California, Los Angeles](https://ucla.edu/)                                          | [Profile](https://www.linkedin.com/in/shinyoung-mark-lee-a502bb1b8/)    |
| Joann Sum   | [CSUF](https://www.fullerton.edu/)                                              | [Profile](https://www.linkedin.com/in/joann-s-5a585a1ba/)               |
| Krish Jain   | [University of Rochester](https://rochester.edu/)                                              | [Profile](https://www.linkedin.com/in/krishjain02)               |
| Pranav Kapoor   | [Acadia University](https://www2.acadiau.ca/home.html)                                              | [Profile](https://ca.linkedin.com/in/pranav-kapoor-91b918270)              |


## Area of Study

Our work reviews existing analysis tools for SELinux security policies and proposes improvements to address current challenges.

## Key Points

- SELinux implements mandatory access control (MAC) in Linux systems
- SELinux policies are complex and difficult to develop and analyze
- Many tools have been created to help analyze SELinux policies, but they have limitations

## Existing Tools Reviewed

The paper **Review of Existing Analysis Tools for SELinux Security Policies: Challenges and a Proposed Solution** reviews 18 different SELinux policy analysis tools, including:

- APOL
- SLAT
- XcelLog
- GOKYO
- PAL
- SEGrapher
- SEAnalyzer
- PVA/GPA
- SELint

## Challenges Identified

- Complexity of SELinux policy language
- Lack of formal semantics
- Difficulty expressing high-level security goals
- Limited query capabilities of existing tools
- Lack of provable correctness for analysis results

## Proposed Solution

- Adopt a certified policy language like ACCPL (A Certified Core Policy Language)
- Develop a domain-specific certified language for SELinux policies
- Leverage formal verification capabilities [WIP]
- Simplify policy development and analysis [WIP]

## Future Work

Design certified domain-specific policy language based on ACCPL
Develop certified analysis tools using the new language

# Graph-Powered Analysis of SELinux Security Policies

## Overview
This research proposes using graph database technology to analyze and visualize SELinux security policies, which are often complex and difficult to manage. The authors use Neo4j to model and query SELinux Type Enforcement (TE) policies.

## Key Points
- SELinux implements mandatory access control (MAC) in Linux systems, providing fine-grained security but resulting in complex policies
- Existing analysis tools often have limitations or add complexity
- Graph databases are well-suited for representing and querying relationships in SELinux policies
- The approach models SELinux TE policies using Neo4j, with nodes representing subjects, objects, and object classes, and relationships representing actions/permissions

## Methodology
1. Extract policy data using APOL tool
2. Import data into Neo4j graph database
3. Design queries to analyze policies

## Query Types Demonstrated
1. Node to Node Direct Information Flow 
2. Group to Groups Direct Information Flow
3. Node/Group to Group/Node Information Flow
4. Node to Node Indirect Information Flow
5. Reachability Analysis
6. Security Goal Verification

## Benefits
- Visual representation of policies
- Simplified query language (Cypher)
- Efficient analysis of complex relationships

## Future Work
- Integrate machine learning for more efficient analysis
- Develop dedicated SELinux analysis software using graph database principles
- Automate query generation based on security objectives

## Limitations
- Potential scalability concerns for very large policy sets (not explicitly addressed)
- Requires learning a new query language (Cypher), though simpler than alternatives

This approach aims to make SELinux policy analysis more accessible and efficient for system administrators, potentially improving overall system security.
