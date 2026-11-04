import 'package:flutter/material.dart';
import '../Controller/data_controller.dart';
/*  Icon, Color and Design Library  */

Map<String, BorderRadius> borderSpecifications = {
  'innerBorderRadius': const BorderRadius.only(topLeft: Radius.circular(20.0), topRight: Radius.circular(20.0)),
  'outerBorderRadius': const BorderRadius.only(topLeft: Radius.circular(22.0), topRight: Radius.circular(22.0)),
  'allInnerBorderRadius': const BorderRadius.all(Radius.circular(20.0)),
  'allElementBorderRadius': const BorderRadius.all(Radius.circular(18.0)),
  'allOuterBorderRadius': const BorderRadius.all(Radius.circular(22.0)),
  'circleInnerBorderRadius': const BorderRadius.all(Radius.circular(40.0)),
  'circleOuterBorderRadius': const BorderRadius.all(Radius.circular(42.0)),
};

const mainRouteStyle = [
  Icons.home
];

const iconStylesBib = [
  Icons.create_new_folder,
  Icons.folder_copy,
  Icons.folder_delete,
  Icons.drive_folder_upload_rounded,
  Icons.rule_folder_rounded             // IDK why, but i can use it maybe...
];

const iconConnectionStyles = [
  Icons.bluetooth,
  Icons.bluetooth_connected,
  Icons.bluetooth_disabled,
];

const iconSettingsStyles = [
  Icons.settings
];

const iconStylesRecipe = [
  Icons.circle_outlined,
  Icons.circle,
  Icons.check_circle,
  Icons.stop_rounded,
];

final bgColorScheme = [
  const Color.fromRGBO(50, 50, 100, 100)
];

final widgetColorStyle = [
  const Color.fromRGBO(255, 255, 255, 1),
  const Color.fromRGBO(255, 255, 0, 1),
  const Color.fromRGBO(255, 50, 50, 1),
  const Color.fromRGBO(80, 80, 80, 1),
];

final bgColorStyle = [
  const Color.fromRGBO(255, 255, 255, 1),
  const Color.fromRGBO(0, 0, 0, 1),
  const Color.fromRGBO(80, 80, 90, 1),
  const Color.fromRGBO(90, 90, 100, 1),
  const Color.fromRGBO(50, 50, 100, 1),
  const Color.fromRGBO(60, 60, 100, 1),
  const Color.fromRGBO(35, 35, 90, 1),
];

final highlightStyle = [
  const Color.fromRGBO(255, 50, 0, 1),
  const Color.fromRGBO(255, 255, 0, 1),
  const Color.fromRGBO(50, 250, 50, 1),
  const Color.fromRGBO(200, 50, 200, 1),
  const Color.fromRGBO(255, 255, 255, 1),
  const Color.fromRGBO(80, 80, 80, 1),
  const Color.fromRGBO(180, 180, 180, 1),
  const Color.fromRGBO(10, 10, 10, 1),
  const Color.fromRGBO(0, 250, 150, 1),
  const Color.fromRGBO(0, 50, 250, 1),
];

Map<String, double> mainScaleFace = {
  'outerRadius' : 0,
  'outerLeft' : 0,
  'outerTop' : 0,
};

var iconStylesButton = [
  iconStylesBib[1],
  iconConnectionStyles[(isBleActive ? 1 : 2)],
  iconSettingsStyles[0],
  mainRouteStyle[0],
  iconStylesBib[0],
  iconStylesBib[2],
  iconStylesRecipe[2],
  Icons.arrow_back,
  Icons.not_interested,
  Icons.bluetooth_disabled,
  Icons.bluetooth_connected,
];

