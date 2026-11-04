import 'package:flutter/material.dart';
import '../DataAndValues/data_value.dart';
import '../Controller/data_controller.dart';
import '../Controller/database_controller.dart';

/*  Standard button with Icon  */
class NormalButtonSSA extends StatelessWidget {
  final int iconFace;
  final int function;
  final int color;

  const NormalButtonSSA({
    super.key,
    required this.iconFace,
    required this.function,
    required this.color
  });

  @override
  Widget build(BuildContext context) {
    final ssaSize = MediaQuery.of(context).size.width * 0.125;
    return IconButton(
      onPressed: () {
        /*  Function depends on calibration  */
        switch (function) {
          case 100: // Settings - dialog
            onActiveScreen = 0;
            final targetDeviceCtr = TextEditingController();
            final targetSUUIDCtr = TextEditingController();
            final targetCUUIDCtr = TextEditingController();

            showDialog<String>(
              context: context,
              builder: (BuildContext context) => AlertDialog(
                title: const Text('Settings'),
                content: SizedBox(
                  width: MediaQuery.of(context).size.width * 0.8,
                  height: MediaQuery.of(context).size.height * 0.3,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Change target device MAC-address'),
                      TextField(decoration: InputDecoration(
                          hintText: targetDeviceId,
                          hintStyle: TextStyle(
                              color: Color.fromRGBO(0, 0, 0, 0.4)
                          )
                      ), controller: targetDeviceCtr,
                      ),
                      SizedBox(
                          height: MediaQuery.of(context).size.height * 0.03
                      ),
                      const Text('Change target service UUID'),
                      TextField(decoration: InputDecoration(
                          hintText: targetServiceUUID,
                          hintStyle: TextStyle(
                              color: Color.fromRGBO(0, 0, 0, 0.4)
                          )
                      ), controller: targetSUUIDCtr,
                      ),
                      SizedBox(
                          height: MediaQuery.of(context).size.height * 0.03
                      ),
                      const Text('Change target characteristic UUID'),
                      TextField(decoration: InputDecoration(
                          hintText: targetCharacteristicUUID,
                          hintStyle: TextStyle(
                              color: Color.fromRGBO(0, 0, 0, 0.4)
                          )
                      ), controller: targetCUUIDCtr,
                      ),
                    ],
                  ),
                ),
                actions: <Widget>[
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      TextButton(
                        onPressed: () => {
                          targetDeviceId = "48:31:B7:B2:C7:16",
                          targetServiceUUID = "00ff",
                          targetCharacteristicUUID = "ff01",

                          onActiveScreen = 1,
                          Navigator.pop(context, 'OK'),
                          Navigator.push(context, routeAction(0))
                        },
                        child: const Text('Restore default'),
                      ),
                      Row(
                        children: [
                          TextButton(
                            onPressed: () => {
                              onActiveScreen = 1,
                              Navigator.pop(context, 'Cancel'),
                            },
                            child: const Text('Cancel'),
                          ),
                          TextButton(
                            onPressed: () async {
                              if (targetDeviceCtr.text.isNotEmpty &&
                                  targetSUUIDCtr.text.isNotEmpty &&
                                  targetCUUIDCtr.text.isNotEmpty) {
                                targetDeviceId = targetDeviceCtr.text;
                                targetServiceUUID = targetSUUIDCtr.text;
                                targetCharacteristicUUID = targetCUUIDCtr.text;

                                onActiveScreen = 1;
                                Navigator.pop(context, 'OK');
                                Navigator.push(context, routeAction(0));
                              } else {
                                await showDialog(
                                    context: context,
                                    builder: (context) {
                                  return AlertDialog(
                                      title: Text('All fields have to be '
                                          'filled to proceed!'),
                                      actions: [
                                        TextButton(
                                          onPressed: () {
                                            Navigator.pop(context);
                                          },
                                          child: Text('OK'),
                                        ),
                                      ]
                                  );
                                });
                              }
                            },
                            child: const Text('Save changes'),
                          ),
                        ],
                      )
                    ],
                  )
                ],
              ),
          );
          case 101: RecipeListScreenState().addRecipe(context);
            // New recipe
          case 102: DatabaseHelper.instance.deleteDatabases();
            Navigator.push(context, routeAction(2));
            // Delete all
          default: Navigator.push(context, routeAction(function));
            // Default makes route according to function number
        }
      },
      style: IconButton.styleFrom(
          shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(80))
          ),
          backgroundColor: highlightStyle[color],
          fixedSize: Size(ssaSize,ssaSize),
          alignment: Alignment.center
      ),
      icon: Icon(
        iconStylesButton[iconFace],
        color: widgetColorStyle[3],
        size: 30,
      ),
    );
  }
}

/*  Standard button with Text and Icon  */
class NormalButtonMainOption extends StatelessWidget {
  final int iconFace;
  final int function;
  final String buttonText;
  final Size sizes;
  final Color color;
  const NormalButtonMainOption({
    super.key,
    required this.iconFace,
    required this.buttonText,
    required this.function,
    required this.sizes,
    required this.color
  });

  @override
  Widget build(BuildContext context) {
    return MaterialButton(
      onPressed: () {
        /*  Function depends on calibration  */
        switch(function) {
          case 10: if (currentStep >= 1) {currentStep -= 1;}
            // Back button in MainView
          case 11:
            if (doneCount <= currentStep)
              {doneCount += 1;}
            if (currentStep < gSteps.length - 1)
              {currentStep += 1;}
            // Forth button in MainView
          case 12: onActiveScreen = 0;
            showDialog<String>(
            context: context,
            builder: (BuildContext context) => AlertDialog(
              title: const Text('Do you want to exit the Recipe?'),
              content: const Text('Your progress in this Recipe will be lost.'),
              actions: <Widget>[
                TextButton(
                  onPressed: () => {
                    onActiveScreen = 1,
                    Navigator.pop(context, 'Cancel'),
                  },
                  child: const Text('Cancel'),
                ),
                TextButton(
                  onPressed: () => {
                    onActiveScreen = 1,
                    Navigator.pop(context, 'OK'),
                    closeRecipe(),
                    Navigator.push(context, routeAction(0))
                  },
                  child: const Text('Yes, exit'),
                ),
              ],
            ),
          );
            // Exit recipe
          case 13: onActiveScreen = 0;
            showDialog<String>(
            context: context,
            builder: (BuildContext context) => AlertDialog(
              title: const Text('You did it!'),
              content: const Text('Do you want to finish? '
                  'Your progress in this Recipe will be lost.'),
              actions: <Widget>[
                TextButton(
                  onPressed: () => {
                    onActiveScreen = 1,
                    Navigator.pop(context, 'Cancel'),
                  },
                  child: const Text('Cancel'),
                ),
                TextButton(
                  onPressed: () => {
                    onActiveScreen = 1,
                    Navigator.pop(context, 'OK'),
                    closeRecipe(),
                    Navigator.push(context, routeAction(0))
                  },
                  child: const Text('Finish the work!'),
                ),
              ],
            ),
          );
            // End recipe after completion
          default: Navigator.push(context, routeAction(function));
          // Default makes route according to function number
        }
        /*  For some functions a back-route to MainView is added (reload)  */
        if(function < 12) {
          Navigator.push(context, routeAction(0));
        }
      },
      color: color,
      height: sizes.height,
      minWidth: sizes.width,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(50))
      ),
      textColor: Colors.black,
      highlightColor: Colors.white,
      child: Row(
        children: [
          Icon(
            iconStylesButton[iconFace],
            color: widgetColorStyle[3],
            size: 30,
          ),
          SizedBox(width: 10),
          Text(buttonText),
        ],
      ),
    );
  }
}