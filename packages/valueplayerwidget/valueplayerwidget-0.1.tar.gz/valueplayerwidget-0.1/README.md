# ValuePlayerWidget

ValuePlayerWidget is a tool to save and display the different steps of a visualisation. It allows the Player to watch all the steps leading to a final step backward and forward. It is also possible to give it a set of action buttons to display and to display the name of the executed action for each step.

ValuePlayerWidget takes three parameters for its initialization :
 * 'visualisation' : this parameter is obligatory, it has to be or inheritate from a traitlets object. This will be the visualisation, le Player interacts with.
 * 'buttons' : this parameter is optionnal. It has to be a list of list. This is an example to understand its structure :
     * buttons=[[("B1",f1,0,8,10),("B2",f2)],[("B3",f3),("B4",f4,15,"abc"),("B5",f6,"b")]]
     
     Each list inside the main one is meant to be a column of buttons and each tupple is a button. In this example, we have two columns, the first column has two buttons and the second one has three buttons. 
     For each button, we give a tupple t in which we may find two or three elements :
         * "B1" : the name of the action, it will be displayed on the buttons with the value given to the function
         * "f1" : the function the button must execute when clicked
         * args : it is optional, they are arguments to give to the function

There are several possibles modes to wtach the steps :
* With the sliders : The player may choose which step to display with the "Time" slider and choose the speed with the "Speed" slider
* With the buttons, each butons changes the way to display the step (from the left to the right):
    * Display the first step and pause
    * Display the steps backward or/and increase the speed
    * Display the steps backward with a normal speed
    * Display the previous step and pause
    * Play/Pause
    * Display the next step and pause
    * Display the steps wiath a normal speed
    * Display the steps or/and increase the speed
    * Display the last step and pause
    

Link to the [Demo](https://gitlab.u-psud.fr/edwige.gros/ValuePlayerWidget/blob/master/Demo.ipynb)
Binder : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.u-psud.fr%2Fedwige.gros%2FValuePlayerWidget.git/master?filepath=Demo.ipynb)


Dependencies:
- traitlets
- time
- ipywidgets