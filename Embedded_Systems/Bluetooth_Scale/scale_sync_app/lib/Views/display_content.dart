import 'package:flutter/material.dart';
import 'package:scale_sync_app/Components/normal_button.dart';
import 'package:scale_sync_app/Controller/data_controller.dart';
import '../DataAndValues/data_value.dart';
import 'dart:core';

/*  Class of content for MainView() when a recipe is loaded  */
class InnerMain extends StatelessWidget {
  const InnerMain({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
        children: [
          /*  At first, the difference in needed and measured weight as well
              as the completed steps are shown behind the scale  */
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              /*  Container for difference value  */
              Container(
                margin: EdgeInsets.only(
                    left: MediaQuery.of(context).size.width * 0.01,
                    top: MediaQuery.of(context).size.height * 0.005
                ),
                padding: EdgeInsets.only(
                  left: MediaQuery.of(context).size.width * 0.025,
                ),
                height: MediaQuery.of(context).size.height * 0.075,
                width: MediaQuery.of(context).size.height * 0.15,
                decoration: BoxDecoration(
                  color: bgColorStyle[3],
                  borderRadius: borderSpecifications['allElementBorderRadius'],
                ),
                alignment: Alignment.centerLeft,
                child: Text(
                  /*  Difference is calculated directly from global data -
                      the value is floored to 2 decimal places  */
                    "${(100*(int.parse(gSteps[currentStep]['mass_for_scale']!)
                        - scaleMeasure)).floor() / 100}g",
                    style: TextStyle(
                      /*  Color is set according to difference level -
                          representing the game-like character  */
                      color: highlightStyle[measureResponse != 0
                          ? (measureResponse >= 2 ? 3 : 2) : 4],
                      fontSize: 15,
                    )),
              ),
              /*  Container for step-count  */
              Container(
                margin: EdgeInsets.only(
                    right: MediaQuery.of(context).size.width * 0.01,
                    top: MediaQuery.of(context).size.height * 0.005
                ),
                padding: EdgeInsets.only(
                  right: MediaQuery.of(context).size.width * 0.025,
                ),
                height: MediaQuery.of(context).size.height * 0.075,
                width: MediaQuery.of(context).size.height * 0.15,
                decoration: BoxDecoration(
                  color: bgColorStyle[3],
                  borderRadius: borderSpecifications['allElementBorderRadius'],
                ),
                alignment: Alignment.centerRight,
                child: Text(
                  /*  Current step-count compared with final steps  */
                    "$doneCount / ${gSteps.length}",
                    style: TextStyle(
                      /*  Color is set according to the progress -
                          representing the game-like character  */
                      color: highlightStyle[doneCount < gSteps.length ? 4 : 2],
                      fontSize: 15,
                    )),
              ),
            ],
          ),
          /*  Descriptions for the two fields above are added below  */
          SizedBox(
            width: MediaQuery
                .of(context)
                .size
                .width * 0.9,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                /*  Difference text with color corresponding with the values
                    color  */
                Text("Difference", style: TextStyle(
                  color: highlightStyle[
                    measureResponse != 0 ? (measureResponse >= 2 ? 3 : 2) : 4],
                  fontSize: 15,)),
                /*  Completed text with color corresponding with the values
                    color  */
                Text("Completed", style: TextStyle(
                  color: highlightStyle[doneCount < gSteps.length
                      ? 4 : 2], fontSize: 15,)),
              ],
            ),
          ),
          SizedBox(height: MediaQuery.of(context).size.height * 0.05),
          /*  The last step of the recipe (if there is one) will be shown in
              the following container, else replaced by a SizedBox that will
              keep the space empty but reserved (If the currentStep is
              higher than '0', that means, there is a need for the
              Container - if not, the SizedBox will be shown)  */
          SizedBox(height: currentStep <= 0
              ? MediaQuery.of(context).size.height * 0.06 : 0),
          Container(
            height: currentStep > 0
                ? MediaQuery.of(context).size.height * 0.06 : 0,
            width: MediaQuery.of(context).size.width * 0.98,
            padding: EdgeInsets.only(
              right: MediaQuery.of(context).size.width * 0.025,
              left: MediaQuery.of(context).size.width * 0.025,
            ),
            /*  In this row the important information for the previous step
                is displayed  */
            child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  /*  Container for background decoration of mass display  */
                  Container(
                    height: MediaQuery.of(context).size.height * 0.05,
                    width: MediaQuery.of(context).size.width * 0.15,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: bgColorStyle[3],
                      borderRadius:
                        borderSpecifications['allElementBorderRadius'],
                    ),
                    /*  After a check for no '0' as currentStep, from
                        the step previous to it, the needed weight will load  */
                    child: Text(
                        gSteps[currentStep > 0
                            ? currentStep - 1
                            : 0]['mass_for_scale']!, style: TextStyle(
                      color: highlightStyle[2], fontSize: 20,)
                    ),
                  ),
                  /*  After a check for no '0' as currentStep, from
                      the step previous to it, the name will load  */
                  Text(gSteps[currentStep > 0
                      ? currentStep - 1
                      : 0]['name']!, style: TextStyle(
                    color: highlightStyle[2], fontSize: 20,)
                  ),
                  /*  After a check for no '0' as currentStep, a checked
                      icon will load for the completed step  */
                  Icon(
                    iconStylesRecipe[2],
                    color: highlightStyle[4],
                    size: 30,
                  ),
                ]
            ),
          ),
          /*  The current step of the recipe will be shown here in an extra
              container to make the background lighter to highlight the row  */
          Container(
            decoration: BoxDecoration(
              color: bgColorStyle[3],
            ),
            height: MediaQuery.of(context).size.height * 0.1,
            width: MediaQuery.of(context).size.width * 0.98,
            padding: EdgeInsets.only(
              right: MediaQuery.of(context).size.width * 0.025,
              left: MediaQuery.of(context).size.width * 0.025,
            ),
            /*  Actual row for the current step  */
            child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  /*  Container for background decoration of mass display  */
                  Container(
                    height: MediaQuery.of(context).size.height * 0.05,
                    width: MediaQuery.of(context).size.width * 0.15,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: bgColorStyle[2],
                      borderRadius:
                        borderSpecifications['allElementBorderRadius'],
                    ),
                    /*  Current step needed weight loads here  */
                    child: Text("${gSteps[currentStep]['mass_for_scale']!}g",
                        style: TextStyle(
                        color: highlightStyle[2], fontSize: 20)
                    ),
                  ),
                  /*  Current step name loads here  */
                  Text(gSteps[currentStep]['name']!, style: TextStyle(
                      color: highlightStyle[2], fontSize: 20)
                  ),
                  /*  Current step icon loads here  */
                  Icon(
                    /*  Style depends on, if it is yet to be completed -
                        if yes, only a circle appears, else a checkmark too  */
                    iconStylesRecipe[(currentStep < doneCount)
                        ? 2 : 1
                    ],
                    color: highlightStyle[4],
                    size: 30,
                  ),
                ]
            ),
          ),
          /*  The next step of the recipe (if there is one) will be shown in
              the following container, else replaced by a SizedBox that will
              keep the space empty but reserved (If the currentStep is
              at the max there is a need for the SizedBox -
              if not, the Container will be shown)  */
          SizedBox(height: currentStep >= gSteps.length - 1
              ? MediaQuery.of(context).size.height * 0.06 : 0),
          Container(
            height: currentStep < gSteps.length - 1
                ? MediaQuery.of(context).size.height * 0.06 : 0,
            width: currentStep < gSteps.length - 1
                ? MediaQuery.of(context).size.width * 0.98 : 0,
            padding: EdgeInsets.only(
              right: MediaQuery.of(context).size.width * 0.025,
              left: MediaQuery.of(context).size.width * 0.025,
            ),
            /*  In this row the important information for the next step
                is displayed  */
            child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  /*  Container for background decoration of mass display  */
                  Container(
                    height: MediaQuery.of(context).size.height * 0.05,
                    width: MediaQuery.of(context).size.width * 0.15,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: bgColorStyle[3],
                      borderRadius:
                        borderSpecifications['allElementBorderRadius'],
                    ),
                    /*  After a check for no max as currentStep, from
                        the step next to it, the needed weight will load  */
                    child: Text("${gSteps[currentStep + 1 >=
                        gSteps.length ? 0
                        : currentStep + 1]['mass_for_scale']!}g",
                        style: TextStyle(
                          color: highlightStyle[2], fontSize: 20,
                        )
                    ),
                  ),
                  /*  After a check for no max as currentStep, from
                        the step next to it, the name will load  */
                  Text(gSteps[currentStep + 1 >=
                      gSteps.length ? 0 : currentStep + 1]['name']!,
                      style: TextStyle(
                        color: highlightStyle[2],
                        fontSize: 20
                      )
                  ),
                  /*  Next step icon loads here  */
                  Icon(
                    /*  Style depends on, if it is yet to be completed -
                        if yes, only a circle appears, else a checkmark too  */
                    iconStylesRecipe[(currentStep + 1 < doneCount)
                        ? 2 : 0
                    ],
                    color: highlightStyle[4],
                    size: 30,
                  ),
                ]
            ),
          ),
          /*  Info to the current step is displayed here  */
          Container(
            height: MediaQuery.of(context).size.height * 0.15,
            alignment: Alignment.topLeft,
            padding: EdgeInsets.only(
              right: MediaQuery.of(context).size.width * 0.025,
              left: MediaQuery.of(context).size.width * 0.025,
              top: MediaQuery.of(context).size.height * 0.015,
            ),
            child: Text(
              /*  If not empty, info will be displayed  */
                gSteps[currentStep]['infoText'] == ''
                    ? '' : "Step ${currentStep + 1}:"
                      "\n${gSteps[currentStep]['info'] ?? ''}",
                style: TextStyle(
                    color: highlightStyle[4],
                    fontSize: 20
                )
            ),
          ),
          /*  Recipe-operation buttons are loaded here  */
          SizedBox(
            width: MediaQuery.of(context).size.width * 0.9,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                /*  Go a step back - if not possible, it is grayed out  */
                NormalButtonMainOption(
                    iconFace: 7,
                    buttonText: "Back",
                    function: 10,
                    sizes: Size(75, 50),
                    color: highlightStyle[currentStep == 0 ? 6 : 4]
                ),
                /*  Exit the recipe immediately  */
                NormalButtonMainOption(
                    iconFace: 8,
                    buttonText: "Stop",
                    function: 12,
                    sizes: Size(75, 50),
                    color: highlightStyle[1]
                ),
                /*  Go a step forth - if measured weight is not near needed,
                    it is grayed out (and green if perfect), also
                    changes to finish recipe (as exit but with "finish"
                    - dialog)  */
                NormalButtonMainOption(
                    iconFace: 6,
                    buttonText: (doneCount ==
                        (gSteps.length) &&
                        currentStep ==
                            gSteps.length - 1)
                        ? "Finish"
                        : "Next Step",
                    function: (doneCount ==
                        (gSteps.length) &&
                        currentStep ==
                            gSteps.length - 1)
                        ? 13
                        : 11,
                    sizes: Size(150, 50),
                    color: highlightStyle[(measureResponse != 0
                        ? (measureResponse >= 2 ? 3 : 4)
                        : 6)
                    ]
                )
              ],
            ),
          ),
        ]
    );
  }
}

/*  Class of content for MainView() when no recipe is loaded  */
class InnerMini extends StatelessWidget {
  const InnerMini({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
        children: [
          /*  Background cleared and highlighted Container at bottom  */
          SizedBox(height: MediaQuery.of(context).size.height * 0.35),
          Container(
              height: MediaQuery.of(context).size.height * 0.245,
              width: MediaQuery.of(context).size.width * 0.95,
              margin: EdgeInsets.only(
                right: MediaQuery.of(context).size.width * 0.015,
                left: MediaQuery.of(context).size.width * 0.015,
              ),
              decoration: BoxDecoration(
                color: bgColorStyle[5],
                borderRadius: borderSpecifications['innerBorderRadius'],
              ),
              /*  Column to display content  */
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  /*  Explanatory message if there are last opened recipes
                      or not  */
                  Text(lastRecipes[0] != ""
                      ? "This is a list of your last opened recipes:"
                      : "Here you will see your last opened recipes",
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 15)
                  ),
                  /*  If given, the last two opened recipes are displayed
                      here  */
                  Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      /*  Highlighted Container for first one  */
                      Container(
                        /*  Disappear if no name is there (height '0')  */
                        height: lastRecipes[0] != ""
                            ? MediaQuery.of(context).size.height * 0.05 : 0,
                        width: MediaQuery.of(context).size.width * 0.65,
                        margin: EdgeInsets.only(
                          right: MediaQuery.of(context).size.width * 0.015,
                          left: MediaQuery.of(context).size.width * 0.015,
                        ),
                        decoration: BoxDecoration(
                          color: bgColorStyle[6],
                          borderRadius:
                            borderSpecifications['allInnerBorderRadius'],
                        ),
                        alignment: Alignment.center,
                        /*  Load last visited name  */
                        child: Text(
                            lastRecipes[0],
                            style: TextStyle(color: Colors.white)
                        )
                      ),
                      /*  For space in between  */
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.025
                      ),
                      /*  Highlighted Container for second one  */
                      Container(
                        /*  Disappear if no name is there (height '0')  */
                          height: lastRecipes[1] != ""
                              ? MediaQuery.of(context).size.height * 0.05 : 0,
                          width: MediaQuery.of(context).size.width * 0.65,
                          margin: EdgeInsets.only(
                            right: MediaQuery.of(context).size.width * 0.015,
                            left: MediaQuery.of(context).size.width * 0.015,
                          ),
                          decoration: BoxDecoration(
                            color: bgColorStyle[6],
                            borderRadius:
                              borderSpecifications['allInnerBorderRadius'],
                          ),
                          alignment: Alignment.center,
                          /*  Load second last visited name  */
                          child: Text(
                              lastRecipes[1],
                              style: TextStyle(color: Colors.white)
                          ),
                      ),
                    ],
                  )
                ],
              )
          ),
        ]
    );
  }
}