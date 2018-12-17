[Course Home](../README.md) | [Syllabus](syllabus.md) | [Projects](projects.md) | [Intro Modules](introductory-modules.md)

## General information

### Expectations
Since our class is a computer lab, please no food or drink. Class attendance is expected, as is on-time submission of assignments (late submissions require valid justification prior to submission date), and doing all the readings/assignments prior to the class for which they are assigned. 

We follow the University's policies on plagiarism and cheating. Please familiarize yourself with the University's [policy](http://www2.clarku.edu/offices/aac/integrity.cfm) on academic integrity, particularly section I. 

### Communications
We will conduct class communications via a Slack channel that you should already be invited to. Please don't send emails. We use Slack because it keeps relevant conversations in defined places, rather than scattered across email inboxes. 

### Approach
This is a project-oriented class, and the projects map onto ongoing research problems. This means that the course will be hands-on and devoted to developing new methods/analyses from some of the newest tools to hit the EO scenes. The downside is that this means that we are all learning as we go, and there will generally not be step-by-step tutorials or recipes to follow. The upside to that downside is that we will all learn a lot more! 

### Assessment

Final letter grades will be assigned as follows:

| Grade Letter | Upper (+)| Middle    | Lower (-) |
|--------------|----------|-----------|-----------|
|     A        |    >99   |   93-99   |   90-93   |
|     B        |   88-90  |   83-88   |   80-83   |
|     C        |   78-80  |   73-78   |   70-73   |
|     D/F      |   68-70  |   60-68   |   <60 (F) |

Grades will be based on:

- __Participation__, defined as contribution to discussion and problem-solving, and completion of any assigned materials. This is worth 20% of overall grade.
- __Final presentation__: Representing 40% of the final grade for undergraduates and 30% for graduates.
- __Final paper/report__: 40% of undergraduates' grades, 50% of graduates. 

#### Presentations 
The presentation will be assessed according to the following criteria, which sum to 60 points:

- **Quality** evaluates the _content_ of the material you present related to your project, focusing on the information and ideas conveyed in your presentation. How much did you contribute to the project, and how creatively and thoroughly did you do it (i.e. how hard and how-well did you try to problem-solve)? [30 points]
- **Progress** evaluates whether you achieved the objectives put forward in your project proposal, and assessed against the date of project start [15 points]
- **Clarity** relates to the presentation itself--how clear your slides were (they should show, not tell), and your presentation of the material on them; how closely you stuck to time limits; how well you ordered the presentation and how easy it was to follow [15 points]

_Rubric_

Codes: 

- Assessment sub-categories
  - OM = How well were the objectives/methods/goals of the project understood?
  - CON = How much contributed to project?
  - CRE = Creativity/problem-solving 
  - SLI = How clear/effective were the slides?
  - TIM = How was the presentation's timing? 
  - NAR = Was the narrative clear?
- Modifiers:
  - N = No, None, or Not (as in unclear)
  - NV = Not very, not very much
  - F = Fair, fairly
  - H = Highly, outstanding
  - WLWS = Way too long or way too short
  - TLTS = Too long or too short (2-4 minutes)
  - BLBS = Slighly too long or too short (1-2 minutes)
  - PT = Perfect timing

| Quality | Quality pts| Progress | Progress pts | Clarity | Clarity pts |
|--------------|----------|-----------|-----------|-----------|-----------|
| OM N, CON N, CRE N | 0 | N | 0 | NAR N, NAR N, TIM WLWS | 0 |
| OM NV, CON NV, CRE NV | 20 | NV | 9 | NAR NV, NAR NV, TIM TLTS | 9  
| OM F, CON F, CRE F | 25 | F | 12 | NAR F, NAR F, TIM BLBS | 12 |
| OM H, CON H, CRE H | 30 | H | 15 |  NAR H, NAR H, TIM PT | 15 |

##### Presentation structure
- Each person's individual presentation time should last no more than **9 minutes**: *6 minutes* of actual presentation, followed by *2-3 minutes* of questions. That means if you are in a group of 4, your total group time should be no more than 36 minutes. 
- Teams should present together, with each person presenting part of the presentation. Questions can be taken after each person goes, or at the end of all members presentations. 
- A rough rule of them that generally works is to have 1 slide prepared per minute of presentation.  
- Slides should be used to help illustrate a point, and should rather have figures than text. Figures should have labels that can be easily read from the furthest seat in the room.
- What should the presentation convey? 
    - What the overall aim of the project is (introduction)
    - What methods you used and why they might be considered "New Methods in Earth Observation". Here you are providing an explainer to your colleagues, who were focusing on different projects and didn't get a chance to delve into the projects you were doing
    - What results you got so far
    - What you plan to achieve by the submission date, and potentially beyond
    - Projects vary in their format and how they were pursued. It might make more sense for each person in a group to try convey some or all of these aspects, or for each member to focus on presenting one or more of these aspects. We can discuss that. 


#### Final project report
The final project builds on the presentation to provide a written summary of your project, including the progress you achieved since the presentation. It should answer the following questions: 

1. What is the overall aim of the project and what specific Earth Observation is it trying to solve?
2. What were the methods you developed and/or applied?
3. What were your results? 
4. Did the results show that the project aim was realized? Was an Earth Observation limit pushed back (or potentially pushed back)? If this was a group project, how were the results of individual efforts integrated? 
5. What are potential improvements, and any next steps you plan to take? 

The format of your submission should be styled more like a README or extended tutorial on a software repository than a final paper. That means, that most, if not all, of you should write this in Markdown or Rmarkdown document, presenting code and figures that demonstrate your methods and results along with your text. Longer scripts can be provided as separate source files for the relevant language. So please structure the final projects in a folder like this:

```
- project_name
  |- data
  |- docs
  |- scripts
```

The docs folder contains your Markdown/Rmarkdown file (or other document if needed, but please discuss), data contains any accompanying data, and scripts and longer source code that you can link to in your document.  Ultimately, this structure will help us integrate some of the results into this repo, so that next year's class can build on your good work (note: we don't have to do this in all cases, so we will only do this based on mutual agreement). 

In terms of structure, we want to be less texty and more visual. Question 1 should be addressed in ~500 words. Question 2 should be answered using as many words, text, and code snippets as needed to make the method and your steps reproducible (i.e. someone could read and figure out how to get the same results you show). Question 3 is better to answer with figures and tables, and as much text as needed to describe what the figures are showing.  Questions 4 and 5 should together be answered in **no more** than 500-1000 words, depending on how many people are in your group. 

Since this is a methods class, Questions 2 and 3 hold the greatest interest, and here is where the size of the group matters.  More detail is expect in these sections, reflecting the subdivision of work

The format you follow in terms of headings and structure can be flexible as long as the questions above are addressed.  It should be submitted as a single project/report, but each member should write the section that describes their contribution, while writing in any common sections can be divided equitably between team members. Please use initials to denote your parts of the writing. 

The following provides a working overview of the paper/report structure:

Assessment is out of 60 pts (note that there is a minimum points floor, which assumes that a final project has been submitted), and will be based on three categories (the rubric is nearly identical to the presentation, but considered in terms of written rather than presented materials): 

- **Quality** evaluates the _content_ of the material in your final method, focusing on the information and ideas conveyed in your descriptions, figures, and tables. How well did you understand and execute the project, and how well did you convey what you did? [30 points]
- **Progress** evaluates whether you achieved the objectives put forward in your project proposal and final presentation, focusing more on the latter due to course corrections (and incorporating any necessary changes we discussed) [15 points]
- **Clarity** examines the clarity of the writing (is it easy to understand, no typos or missed words), the visual aspects of figures (does the color choice make sense, legend sensible, size appropriate, text readable?), formatting (did html lists end up as lists? do headings make sense?), and code syntax. This basically covers the stylistic components of your vignettes and code. [15 points]

_Rubric_ 

Codes: 

- Assessment sub-categories
  - OM = How well were the objectives/methods/goals of the project understood?
  - CON = How much contributed to project?
  - CRE = Creativity/problem-solving 
  - NAR = Was the narrative clear?
  - WRI = How clear/effective/tidy was the writing?
- Modifiers:
  - N = No, None, or Not (as in unclear)
  - NV = Not very, not very much
  - F = Fair, fairly
  - H = Highly, outstanding
  - PT = Perfect timing

| Quality | Quality pts| Progress | Progress pts | Clarity | Clarity pts |
|--------------|----------|-----------|-----------|-----------|-----------|
| OM N, CON N, CRE N | 0 | N | 0 | NAR N, NAR N, TIM WRI N | 0 |
| OM NV, CON NV, CRE NV | 20 | NV | 9 | NAR NV, NAR NV, WRI N/F | 9  
| OM F, CON F, CRE F | 25 | F | 12 | NAR F, NAR F, WRI F | 12 |
| OM H, CON H, CRE H | 30 | H | 15 |  NAR H, NAR H, WRI H | 15 |


[Course Home](../README.md) | [Syllabus](syllabus.md) | [Projects](projects.md) | [Intro Modules](introductory-modules.md)