Assignment 2, Spring 2022
================

# Second assignment

The second class assignment entails comparing data collected by the
Arable Mark sensor in Zambia against three different sets of
satellite-derived data obtained from Google Earth Engine. It is due due
on April 2nd by the start of class.

To undertake the assignment, work through the
[`arable_query.ipynb`](../code/notebooks/arable_query.ipynb) notebook on
your AWS instance.

-   Log into the AWS console and start your instance.

-   `ssh` in to the instance.

-   Once in, `cd /home/rstudio/projects/nmeo`

-   Then run `git pull` to get updates.

-   Then run:

    ``` bash
    cp nmeo/materials/code/notebooks/arable_query.ipynb notebooks/ 
    ```

    That will copy the notebook from the class repo to your notebooks
    folder.

-   Then run `screen`, and once in the other screen `jupyter lab`.
    ctrl+a+d back to the original screen, and open up `jupyter lab`
    interface in a browser.

-   Navigate to the notebook you copied in the `jupyter lab` file
    browser, and rename it `<yourinitials>_nmeo_2022_assn2`, where
    <yourinitials> is replaced with your actual initials.

-   Work through the notebook, running each block. The places you have
    to complete by providing your own code are marked with headers
    beginning with `[Assignment:]`, with empty cells below them
    prompting you to `# insert code here`. Add your code to those cells,
    and run them.

-   Once done, go to the menu at the top of the interface, and select
    File > Download. That will download the notebook to your local
    computer.

### Materials to hand in

Send me the completed notebook.

## Assessment

This assignment will be assessed out of 50 points, allocated as
follows:.

Points will be assigned as follows (maximum points per category):

-   Notebook assignments fully completed: 5 pts
-   Assignment tasks provide correct solutions: 32 pts
-   Code style and legibility: 10 points
-   Downloaded notebook submitted via Slack: 3 points
