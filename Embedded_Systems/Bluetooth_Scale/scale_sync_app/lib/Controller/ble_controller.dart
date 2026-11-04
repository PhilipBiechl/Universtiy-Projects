import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../Controller/data_controller.dart';
import 'dart:async';
import '../Components/top_bar.dart';
import '../DataAndValues/data_value.dart';

/*  Calls State of BleHomeScreen  */
class BleHomeScreen extends StatefulWidget {
  const BleHomeScreen({super.key});

  @override
  BleHomeScreenState createState() => BleHomeScreenState();
}

/*  Class to handle all BLE operations  */
class BleHomeScreenState extends State<BleHomeScreen> {
  BluetoothDevice? targetDevice;
  BluetoothCharacteristic? targetCharacteristic;
  StreamSubscription? connectionStateSubscription;
  StreamSubscription? dataSubscription;

  List<int> receivedData = [0, 0, 0, 0]; // Variable to hold the received data
  double input = 0.0;

  @override
  void dispose() {
    connectionStateSubscription?.cancel();
    dataSubscription?.cancel();
    targetDevice?.disconnect();
    super.dispose();
  }

  /*  Seek for device - service - characteristic, then start listener  */
  Future<void> connectToDevice() async {
    // Start scanning for the device
    FlutterBluePlus.startScan(timeout: const Duration(seconds: 10));

    FlutterBluePlus.scanResults.listen((results) async {
      for (ScanResult result in results) {
        if (result.device.remoteId.toString() == targetDeviceId) {
          targetDevice = result.device;
          FlutterBluePlus.stopScan();

          try {
            await targetDevice!.connect();
            isBleActive = true;
          } catch (e) {
            isBleActive = false;
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text("Error: $e")),
            );
          }

          /*  Listen for steady subscription  */
          connectionStateSubscription = targetDevice!.connectionState
              .listen((state) {
            setState(() {
              if (state == BluetoothConnectionState.connected) {
                isBleActive = true;
              }
              else {
                isBleActive = false;
                receivedData = [0, 0, 0, 0];
                scaleMeasure = 0;
                measureResponse = 0;
                Navigator.push(context, routeAction(0));
              }
            });
          });

          if (isBleActive) {
            List<BluetoothService> services = await targetDevice!
                .discoverServices();
            for (BluetoothService service in services) {
              if (service.uuid.toString() == targetServiceUUID) {
                for (BluetoothCharacteristic characteristic
                in service.characteristics) {
                  if (characteristic.uuid.toString() ==
                      targetCharacteristicUUID) {
                    targetCharacteristic = characteristic;

                    /*  Listen for data  */
                    await targetCharacteristic!.setNotifyValue(true);
                    dataSubscription = targetCharacteristic!.lastValueStream
                        .listen((data) {
                      setState(() {
                        isBleActive = true;

                        /*  Get data from packages  */
                        receivedData[0] = data.isNotEmpty ? data[1].toInt() : 0;
                        receivedData[1] = data.isNotEmpty ? data[2].toInt() : 0;
                        receivedData[2] = data.isNotEmpty ? data[3].toInt() : 0;
                        receivedData[3] = data.isNotEmpty ? data[3].toInt() : 0;
                        input = ((receivedData[0] << 24)
                          | (receivedData[1] << 16) | (receivedData[2] << 8)
                          | receivedData[3]) / 1000;

                        /*  Only update if real change in value  */
                        if ((((100 / (scaleMeasure + 1)) * (input + 1)) < 90 ||
                            ((100 / (scaleMeasure + 1)) * (input + 1)) > 110)
                            && onActiveScreen == 1) {
                          scaleMeasure = input;
                          var difference = (scaleMeasure /
                              int.parse(gSteps[currentStep]['mass_for_scale']!)
                          ).abs();
                          measureResponse = (difference < 0.8
                              ? (difference < 0.1 ? 2 : 1) : 0);
                          Navigator.push(context, routeAction(0));
                        }
                      });
                    });
                    Navigator.push(context, routeAction(0));
                  }
                }
              }
            }
          }
          break;
        }
      }
    });
  }

  /*  Clean disconnect  */
  Future<void> disconnectFromDevice() async {
    try {
      if (dataSubscription != null) {
        await dataSubscription!.cancel();
        dataSubscription = null;
      }
      if (targetDevice != null) {
        await targetDevice!.disconnect();
        targetDevice = null;
        targetCharacteristic = null;
      }

      setState(() {
        isBleActive = false;
        receivedData = [0, 0, 0, 0];
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
    Navigator.push(context, routeAction(0));
  }

  /*  View to operate BLE options  */
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: bgColorScheme[0],
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SizedBox(height: MediaQuery.of(context).size.height * 0.05),
          TopBar(
              icons: [3, isBleActive ? 10 : 9, 2],
              routes: const [0, 1, 100],
              topText: "connecting...",
              colors: [4, isBleActive ? 4 : 1, 4]
          ),
          Container(
            height: MediaQuery.of(context).size.height * 0.85,
            width: MediaQuery.of(context).size.width,
            alignment: Alignment.center,
            child: ElevatedButton(
              onPressed: () async {
                if (isBleActive) {
                  disconnectFromDevice();
                } else {
                  await connectToDevice();
                }
              },
              child: Text(
                  isBleActive ? 'Disconnect from Device' : 'Connect to Device'
              ),
            ),
          ),
        ],
      ),
    );
  }
}