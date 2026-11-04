import 'package:flutter/material.dart';
import '../Views/main_view.dart';
import '../Controller/ble_controller.dart';
import '../Controller/database_controller.dart';

/* fixed Design */
final range = 500; // Scale range

/* BLE - Connection vars */
String targetDeviceId = "48:31:B7:B2:C7:16";
String targetServiceUUID = "00ff";
String targetCharacteristicUUID = "ff01";

/* State vars for all files */
bool isBleActive = false;
var currentRecipe = 0; // 0 - no recipe, else recipe-number
var currentRecipeName = "";
var currentStep = 0;
var doneCount = 0;  // How many steps are done

var onActiveScreen = 0; // To check if MainScreen is open

var scaleMeasure = 0.0; // Current measurement from scale
var measureResponse = 0; /*  Do measure and needed fit?
                             (0 - no, 1 - yes, 2 - perfect)  */
var scaleNeeded = 0; // Needed weight in current step

var lastRecipes = [
  "",
  ""
];

/*  Currently loaded recipe and it's steps  */
Map<String, dynamic> gRecipe = {};
List<Map<String, dynamic>> gSteps = [];

/*  Functions for controlling  */

/*  End recipe operations clean, add to last opened recipes  */
void closeRecipe() {
  doneCount = 0;
  for (int i = 0; i < gSteps.length; i++) {
    //gSteps[i]['status'] = 0;
  }
  if (currentRecipeName != lastRecipes[0]) {
    lastRecipes[1] = lastRecipes[0];
    lastRecipes[0] = currentRecipeName;
  }
  currentStep = 0;
  currentRecipe = 0;
  currentRecipeName = "";
  scaleNeeded = 0;
}

/*  All routs that have to be called to all screens - no animation to be shown
    (transitionDuration is therefore set to '0')  */
routeAction(int functionIdentifier) {
  switch (functionIdentifier) {
    case 1: onActiveScreen = 0;
      return PageRouteBuilder(pageBuilder: (context, animation1, animation2)
        => BleHomeScreen(),
        transitionDuration: Duration.zero,
        reverseTransitionDuration: Duration.zero,);
    case 2: onActiveScreen = 0;
      return PageRouteBuilder(pageBuilder: (context, animation1, animation2)
        => RecipeListScreen(),
        transitionDuration: Duration.zero,
        reverseTransitionDuration: Duration.zero,);
    default: onActiveScreen = 1;
      return PageRouteBuilder(pageBuilder: (context, animation1, animation2)
        => MainView(),
        transitionDuration: Duration.zero,
        reverseTransitionDuration: Duration.zero,);
  }
}