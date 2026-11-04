import 'package:flutter/material.dart';
import 'package:scale_sync_app/Views/bg_design.dart';
import '../DataAndValues/data_value.dart';
import '../Components/normal_button.dart';

/*  Content of top navigation bar  */
class TopBarInner extends StatelessWidget {
  final List<int> icons;
  final List<int> routes;
  final List<int> colors;
  final String topText;
  const TopBarInner({
    super.key,
    required this.icons,
    required this.routes,
    required this.colors,
    required this.topText
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      /*  Normal design is 3 buttons with functions & icons & a text  */
      children: [
        NormalButtonSSA(
            function: routes[0], iconFace: icons[0], color: colors[0]
        ),
        SizedBox(
          width: MediaQuery.of(context).size.width * 0.40,
          child: Text(
            topText,
            style: TextStyle(
              fontSize: 20,
              color: bgColorStyle[0],
            ),
            textAlign: TextAlign.start,
          ),
        ),
        NormalButtonSSA(
            function: routes[1], iconFace: icons[1], color: colors[1]
        ),
        NormalButtonSSA(
            function: routes[2], iconFace: icons[2], color: colors[2]
        )
      ],
    );
  }
}

/*  Loads the parameters of a top navigation bar in a top-box  */
class TopBar extends StatelessWidget {
  final List<int> icons;
  final List<int> routes;
  final List<int> colors;
  final String topText;
  const TopBar({
    super.key,
    required this.icons,
    required this.routes,
    required this.colors,
    required this.topText
  });

  @override
  Widget build(BuildContext context) {
    return BgTopSizedBox(inner:
    TopBarInner(icons: icons, routes: routes, topText: topText, colors: colors)
    );
  }
}