# CS 476 - Project (Winter 2023)

### Problem Statement:
Promoting speech that is likely to incite hatred has been illegal in Canada since 1970. Identifying and quantifying this speech is an active area of research across several social science disciplines. With the advent of social media outlets, digesting and annotating these vast datasets is infeasible for human evaluators who are subject to bias and time constraints. Additionally with the increase in content the task of visualizing and identifying patterns in the data has become increasingly complex. Our solutions to these problems are:
 - A natural language processing deep learning model trained on the ‘Measuring Hate Speech Corpus[1] to interpret user comments and return scoring data.
 - A community crawler to gather comments and community metadata and carry out inference and persist the results to a database.
 - A software interface representing the persisted data in a graph object representing community connections and their statistics pertaining to inference results. 

##### User Roles:
 - Community User ⇒ User has an account and provides a community that they wish to monitor.
 - Admin User ⇒ User role for administering the other user roles.
##### Functional Requirements:
 - AI model is able to process text
 - Web Crawler heuristic functions correctly and interfaces with controller
 - Controller able to communicate data between AI model and View
 - Graph Map View generates correctly and is interactable with users 
##### Quality Requirements:
 - *Robustness*
      - Incorrect user input into the graph view should not cause unintended behaviour
 - *Correctness* 
      - Subreddit data should match correct subreddit
 - *Timeliness*
      - Subreddit graph / map should load in less than 5 seconds
      - Node manipulation should not grind the simulation down to a halt
      - AI can process a batch in under 1000ms
      
      
      
 ###### Citation(s)
*[1]* **Pratik Sachdeva, Renata Barreto, Geoff Bacon, Alexander Sahn, Claudia von Vacano, and Chris Kennedy. 2022. The Measuring Hate Speech Corpus: Leveraging Rasch Measurement Theory for Data Perspectivism. In Proceedings of the 1st Workshop on Perspectivist Approaches to NLP @LREC2022, pages 83–94, Marseille, France. European Language Resources Association.**
