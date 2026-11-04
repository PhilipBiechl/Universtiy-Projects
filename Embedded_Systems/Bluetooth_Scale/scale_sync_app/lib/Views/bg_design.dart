import 'package:flutter/material.dart';
import '../DataAndValues/data_value.dart';
/*  Here, the general Design for background shapes is defined  */

/*  Background-Box for main content  */
class BgMainSizedBox extends StatelessWidget{
  final StatelessWidget inner; // Content in the Box
  const BgMainSizedBox({super.key, required this.inner});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: MediaQuery.of(context).size.height * 0.6,
      decoration: BoxDecoration(
        color: bgColorStyle[3],
        borderRadius: borderSpecifications['outerBorderRadius'],
      ),
      child: Container(
        margin: EdgeInsets.only(
            left: MediaQuery.of(context).size.width * 0.01,
            right: MediaQuery.of(context).size.width * 0.01,
            top: MediaQuery.of(context).size.height * 0.005
        ),
        height: MediaQuery.of(context).size.height * 0.595,
        decoration: BoxDecoration(
          color: bgColorStyle[2],
          borderRadius: borderSpecifications['innerBorderRadius'],
        ),
        /*  Content is displayed here  */
        child: inner,
      )
    );
  }
}

/*  Background-Box for top navigation bar  */
class BgTopSizedBox extends StatelessWidget{
  final StatelessWidget inner; // Content in the Box
  const BgTopSizedBox({super.key, required this.inner});

  @override
  Widget build(BuildContext context) {
    return Container(
        width: MediaQuery.of(context).size.width * 0.9,
        height: MediaQuery.of(context).size.height * 0.075,
        decoration: BoxDecoration(
          color: bgColorStyle[3],
          borderRadius: borderSpecifications['circleOuterBorderRadius'],
        ),
        child: Container(
          margin: EdgeInsets.only(
              left: MediaQuery.of(context).size.width * 0.01,
              right: MediaQuery.of(context).size.width * 0.01,
              top: MediaQuery.of(context).size.height * 0.005,
              bottom: MediaQuery.of(context).size.height * 0.005
          ),
          decoration: BoxDecoration(
            color: bgColorStyle[2],
            borderRadius: borderSpecifications['circleInnerBorderRadius'],
          ),
          /*  Content is displayed here  */
          child: inner,
        )
    );
  }
}