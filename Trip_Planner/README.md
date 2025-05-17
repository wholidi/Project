## AI Agent 
Learning AI make me realize how limited our time and brain power 
How to achieve more objective with the same 24 hour? 
When we need more hands and brain power, AI Agent is the answer… 

Big thanks to João (Joe) Moura (CrewAI)
Great AI Agent walkthrough from Brandon Hancock

Case:
Suppose we'd like to compare multiple city for our holiday and compare accommodation, place of interest, transport and culture 

Solutions:
Utilize CrewAI to create AI Agent to generate recommendation and calculate budget vs cost according to our interest. 

Is it worth to do it? 
if this is a repeated case like we're going to holiday 2x year and spent days or weeks researching ... it is a Yes 
if this is a on off activities to find favorite cheese cake then googling or instagraming is more fun

My Trip Planner:
https://lnkd.in/gbj2Ngp5

Detail Guide:
https://lnkd.in/gfviChJB

## agents.py
This file contains the definition of custom agents.
To create a Agent, you need to define the following:
1. Role: The role of the agent.
2. Backstory: The backstory of the agent.
3. Goal: The goal of the agent.
4. Tools: The tools that the agent has access to (optional).
5. Allow Delegation: Whether the agent can delegate tasks to other agents(optional).

    [More Details about Agent](https://docs.crewai.com/concepts/agents).

## task.py
This file contains the definition of custom tasks.
To Create a task, you need to define the following :
1. description: A string that describes the task.
2. agent: An agent object that will be assigned to the task.
3. expected_output: The expected output of the task.

    [More Details about Task](https://docs.crewai.com/concepts/tasks).

## crew (main.py)
This is the main file that you will use to run your custom crew.
To create a Crew , you need to define Agent ,Task and following Parameters:
1. Agent: List of agents that you want to include in the crew.
2. Task: List of tasks that you want to include in the crew.
3. verbose: If True, print the output of each task.(default is False).
4. debug: If True, print the debug logs.(default is False).

    [More Details about Crew](https://docs.crewai.com/concepts/crew).
