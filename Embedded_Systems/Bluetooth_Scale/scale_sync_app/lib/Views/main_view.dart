import 'package:flutter/material.dart';
import 'package:scale_sync_app/Views/bg_design.dart';
import '../DataAndValues/data_value.dart';
import '../Components/scale_face.dart';
import '../Views/display_content.dart';
import '../Components/top_bar.dart';
import '../Controller/data_controller.dart';

/*  MainField is the class to show content of measurement beneath the scale
    on the MainView  */
class MainField extends StatelessWidget {
  const MainField({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      /*  Stack of content-fields in MainView - these are loaded on top of
          each other to make the whole view more flexible and the design
          more aesthetic  */
      children: [
        /*  Differ between a loaded recipe - results in InnerMain() for the
            recipe data to be shown - and the InnerMini() to display only
            a list of previously opened recipes  */
        BgMainSizedBox(inner:
          currentRecipe != 0 ? InnerMain() : InnerMini()
        ),
        /*  SectorsPainter() will indicate the needed weight and the difference
            to it behind the scale  */
        CustomPaint(
          painter: SectorsPainter(),
        ),
        /*  The scale itself is drawn here  */
        const ScaleBody(),
      ],
    );
  }
}

/*  The default screen of the app is loaded here  */
class MainView extends StatelessWidget{
  const MainView({super.key});

  @override
  Widget build(BuildContext context) {
    /*  From screen dependent variables that can only be loaded here,
        the size for the later added scale is set  */
    mainScaleFace['outerRadius'] = MediaQuery.of(context).size.width * 0.6;
    mainScaleFace['outerLeft'] = MediaQuery.of(context).size.width * 0.2;
    mainScaleFace['outerTop'] = - MediaQuery.of(context).size.width * 0.3;

    return Scaffold(
      /*  Return a scaffold with basic BG and without complications when
          keyboard is on screen (resizeToAvoidBottomInset)  */
      resizeToAvoidBottomInset: false,
      backgroundColor: bgColorScheme[0],
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          SizedBox(height: MediaQuery.of(context).size.height * 0.05),
          /*  Bar on top loaded with corresponding icons and actions  */
          TopBar(
            icons: [0, isBleActive ? 10 : 9, 2],
            routes: [2, 1, 100],
            topText: currentRecipe != 0 ? gRecipe['name']
                ?? "Scale by P.B." : "Scale by P.B.",
            colors: [4, isBleActive ? 4 : 1, 4],
          ),
          SizedBox(height: MediaQuery.of(context).size.height * 0.275),
          /*  The above described MainField class is loaded last  */
          const MainField(),
        ],
      ),
    );
  }
}