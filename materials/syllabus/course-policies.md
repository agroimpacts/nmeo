# Course Policies

|                                |                         |                                       |                               |                                     |
|--------------------------------|-------------------------|---------------------------------------|-------------------------------|-------------------------------------|
| [Course Home](../../README.md) | [Syllabus](syllabus.md) | [Course Policies](course-policies.md) | [Assignments](assignments.md) | [Projects](../projects/projects.md) |

Expectations

Class attendance is expected, as is on-time submission of assignments
(late submissions require valid justification prior to submission date),
and doing all the readings/assignments prior to the class for which they
are assigned.

We follow the University’s policies on plagiarism and cheating. Please
familiarize yourself with the University’s
[policy](http://www2.clarku.edu/offices/aac/integrity.cfm) on academic
integrity, particularly section I.

### Communications

We will conduct class communications via a Slack channel that you should
already be invited to. Please don’t send emails. We use Slack because it
keeps relevant conversations in defined places, rather than scattered
across email inboxes.

### Approach

This is a project-oriented class, and the projects map onto ongoing
research problems. This means that the course will be hands-on and
devoted to developing new methods/analyses from some of the newest tools
to hit the EO scenes. The downside is that this means that we are all
learning as we go, and there will generally not be step-by-step
tutorials or recipes to follow. The upside to that downside is that we
will all learn a lot more!

### Academic Dishonesty

University’s policies on academic integrity will be strictly enforced.
Go to www.clarku.edu/offices/aac/integrity.cfm to learn more about this
policy and what it entails. Plagiarism, cheating, lying, stealing, or
falsification will not be tolerated and will be referred to the
University Administration.

### Additional Information

#### Student Accessibility Services

Clark University is committed to providing students with documented
disabilities equal access to all university programs and facilities.
Students are encouraged to register with Student Accessibility Services
(SAS) to explore and access accommodations that may support their
success in their coursework. SAS is located on the second floor of the
Shaich Family Alumni and Student Engagement Center (ASEC). Please
contact SAS at <accessibilityservices@clarku.edu> with questions or to
initiate the registration process. For additional information, please
visit the [SAS
website](https://www.clarku.edu/offices/student-accessibility-services/).

#### FERPA Policy

The link to Clark’s policy regarding student privacy under the Family
Education Rights and Privacy Act is available
[here](https://www.clarku.edu/offices/registrar/ferpa/)

#### Title IX

Please be aware that all Clark University faculty and teaching
assistants are considered responsible employees, which means that if you
tell us about a situation involving the aforementioned offenses, we must
share that information with the Title IX Coordinator, Brittany Brickman
(<titleix@clarku.edu>). Although we must make that notification, you
will, for the most part, control how your case will be handled,
including whether or not you wish to pursue a formal complaint. Our goal
is to make sure you are aware of the range of options available to you
and have access to the resources you need. 

If you wish to speak to a confidential resource who does not have this
reporting responsibility, you can contact Clark's Center for Counseling
and Professional Growth (508-793-7678), Clark's Health Center
(508-793-7467), or confidential resource providers on campus (see
[here](https://www.clarku.edu/offices/title-ix/resources/) for a list,
and for other resources).

### Assessment

Final letter grades will be assigned as follows:

| Grade Letter | Upper (+) | Middle | Lower (-) |
|--------------|-----------|--------|-----------|
| A            | \>99      | 93-99  | 90-93     |
| B            | 88-90     | 83-88  | 80-83     |
| C            | 78-80     | 73-78  | 70-73     |
| D/F          | 68-70     | 60-68  | \<60 (F)  |

Grades will be based on:

- **Practicals/homework assignments**: There will be two homework
  assignments related to in-class practical work, worth 30% of the
  overall grade
- **Project plan**: A plan describing how your team will undertake the
  final project (20% of total grade)
- **Final project report**: The final analysis and report for your team
  project is worth 35 of the total grade
- **Participation**: Attendance, contribution to discussion, and
  problem-solving is worth 15% of the overall grade.

#### Assignments

The details of the assignments will vary, and will be provided along
with assessment criteria at the same of their release.

#### Project plan

The project plan should provide an overview of how your team will tackle
the final project, and consist of:

1.  A brief description of the project and its objectives
2.  A summary of the data and methods that will be used
3.  A table describing who will be responsible for which parts of the
    project
4.  A summary of anticipated results, including any expected
    difficulties that might be encountered

#### Final project report

The final report will provide a written summary of your project,
including the progress you achieved since the presentation. It should
answer the following questions:

1.  What is the overall aim of the project and what specific Earth
    Observation problem is it trying to solve?
2.  What were the methods you developed and/or applied?
3.  What were your results?
4.  Did the results show that the project aim was realized? Was an Earth
    Observation limit pushed back (or potentially pushed back)? If this
    was a group project, how were the results of individual efforts
    integrated?
5.  What are potential improvements, and any next steps you plan to
    take?

The format of your submission should be styled more like a README or
extended tutorial on a software repository than a final paper. That
means, that most, if not all, of you should write this in Markdown or
Rmarkdown document, presenting code and figures that demonstrate your
methods and results along with your text. Longer scripts can be provided
as separate source files for the relevant language. So please structure
the final projects in a folder like this:

    - project_name
      |- data
      |- docs
      |- scripts

The docs folder contains your Markdown/Rmarkdown file (or other document
if needed, but please discuss), data contains any accompanying data, and
scripts and longer source code that you can link to in your document.
Ultimately, this structure will help us integrate some of the results
into this repo, so that next year’s class can build on your good work
(note: we don’t have to do this in all cases, so we will only do this
based on mutual agreement).

In terms of structure, we want to be less texty and more visual.
Question 1 should be addressed in ~500 words. Question 2 should be
answered using as many words, text, and code snippets as needed to make
the method and your steps reproducible (i.e. someone could read and
figure out how to get the same results you show). Question 3 is better
to answer with figures and tables, and as much text as needed to
describe what the figures are showing. Questions 4 and 5 should together
be answered in **no more** than 500-1000 words, depending on how many
people are in your group.

Since this is a methods class, Questions 2 and 3 hold the greatest
interest, and here is where the size of the group matters. More detail
is expect in these sections, reflecting the subdivision of work

The format you follow in terms of headings and structure can be flexible
as long as the questions above are addressed. It should be submitted as
a single project/report, but each member should write the section that
describes their contribution, while writing in any common sections can
be divided equitably between team members. Please use initials to denote
your parts of the writing.

The following provides a working overview of the paper/report structure:

Assessment is out of 60 pts (note that there is a minimum points floor,
which assumes that a final project has been submitted), and will be
based on three categories (the rubric is nearly identical to the
presentation, but considered in terms of written rather than presented
materials):

- **Quality** evaluates the *content* of the material in your final
  method, focusing on the information and ideas conveyed in your
  descriptions, figures, and tables. How well did you understand and
  execute the project, and how well did you convey what you did? \[30
  points\]
- **Progress** evaluates whether you achieved the objectives put forward
  in your project proposal and final presentation, focusing more on the
  latter due to course corrections (and incorporating any necessary
  changes we discussed) \[15 points\]
- **Clarity** examines the clarity of the writing (is it easy to
  understand, no typos or missed words), the visual aspects of figures
  (does the color choice make sense, legend sensible, size appropriate,
  text readable?), formatting (did html lists end up as lists? do
  headings make sense?), and code syntax. This basically covers the
  stylistic components of your vignettes and code. \[15 points\]

*Rubric*

Codes:

- Assessment sub-categories
  - OM = How well were the objectives/methods/goals of the project
    understood?
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

| Quality               | Quality pts | Progress | Progress pts | Clarity                 | Clarity pts |
|-----------------------|-------------|----------|--------------|-------------------------|-------------|
| OM N, CON N, CRE N    | 0           | N        | 0            | NAR N, NAR N, TIM WRI N | 0           |
| OM NV, CON NV, CRE NV | 20          | NV       | 9            | NAR NV, NAR NV, WRI N/F | 9           |
| OM F, CON F, CRE F    | 25          | F        | 12           | NAR F, NAR F, WRI F     | 12          |
| OM H, CON H, CRE H    | 30          | H        | 15           | NAR H, NAR H, WRI H     | 15          |

|                                |                         |                                       |                               |                                     |
|--------------------------------|-------------------------|---------------------------------------|-------------------------------|-------------------------------------|
| [Course Home](../../README.md) | [Syllabus](syllabus.md) | [Course Policies](course-policies.md) | [Assignments](assignments.md) | [Projects](../projects/projects.md) |
