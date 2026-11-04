import 'package:flutter/material.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'dart:core';
import 'data_controller.dart';
import '../Components/top_bar.dart';
import '../DataAndValues/data_value.dart';
import 'package:flutter/services.dart';


/*  Database operations are defined here  */
class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await initDB('recipes.db');
    return _database!;
  }

  /*  Init database  */
  Future<Database> initDB(String fileName) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, fileName);

    return await openDatabase(path, version: 1, onCreate: createDB);
  }

  /*  Create a database - used for recipe-list & every step  */
  Future createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        comment TEXT,
      )
    ''');
  }

  /*  Creates an entry in recipe database & steps as linked databases */
  Future<int> createRecipe(
      String name, String comment, List<Map<String, dynamic>> steps
      ) async {
    final db = await instance.database;

    final recipeId = await db.insert('recipes', {
      'name': name,
      'comment': comment,
    });

    final tableName = 'steps_$recipeId';
    await db.execute('''
      CREATE TABLE $tableName (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mass_for_scale TEXT,
        info TEXT,
        status INTEGER DEFAULT 0
      )
    ''');

    for (var step in steps) {
      await db.insert(tableName, step);
    }

    return recipeId;
  }

  /*  Loads all current recipes in a query -> needs to go to a map  */
  Future<List<Map<String, dynamic>>> getRecipes() async {
    final db = await instance.database;
    return db.query('recipes');
  }

  /*  Loads all the steps for a recipe ->  needs to go to a list of maps  */
  Future<List<Map<String, dynamic>>> getSteps(int recipeId) async {
    final db = await instance.database;
    return db.query('steps_$recipeId');
  }

  /*  Delete a recipe entry in recipe database and drop all steps (DBs)  */
  Future<void> deleteRecipe(int recipeId) async {
    final db = await instance.database;
    await db.delete('recipes', where: 'id = ?', whereArgs: [recipeId]);
    await db.execute('DROP TABLE IF EXISTS steps_$recipeId');
  }

  /*  Deletes all databases - Q: why would one use this function? A: Because
      sometimes it's good (especially while testing the app) to start
      completely new ;)  */
  Future<void> deleteDatabases() async {
    final db = await instance.database;
    final count = Sqflite.firstIntValue(await db.rawQuery('SELECT COUNT(*) FROM recipes'));

    for (var i = 0; i < count!; i++) {
      await db.delete('recipes', where: 'id = ?', whereArgs: [i]);
      await db.execute('DROP TABLE IF EXISTS steps_$i');
    }
  }
}

/*  This will call the state of the Recipe-List  */
class RecipeListScreen extends StatefulWidget {
  const RecipeListScreen({super.key});

  @override
  RecipeListScreenState createState() => RecipeListScreenState();
}

/*  Recipe-List is displayed here  */
class RecipeListScreenState extends State<RecipeListScreen> {
  /*  Recipes to be shown in listing are stored in this variable  */
  late Future<List<Map<String, dynamic>>> recipes;

  @override
  void initState() {
    super.initState();
    loadRecipes();
  }

  /*  Get all recipes from database  */
  void loadRecipes() {
    setState(() {
      recipes = DatabaseHelper.instance.getRecipes();
    });
  }

  /*  Add a recipe  */
  Future<void> addRecipe(BuildContext context) async {
    /*  Controllers are created for text-inputs  */
    final nameController = TextEditingController();
    final commentController = TextEditingController();

    /*  Steps will be stored here before upload to database on completion  */
    List<Map<String, dynamic>> steps = [];

    /*  Whole process is displayed in a dialog  */
    await showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Add Recipe'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              /*  Name of recipe  */
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Recipe Name'),
                keyboardType: TextInputType.text
              ),
              /*  Additional comment  */
              TextField(
                controller: commentController,
                decoration: InputDecoration(labelText: 'Comment'),
                keyboardType: TextInputType.text
              ),
              /*  Add or manage steps dialog opens here  */
              ElevatedButton(
                onPressed: () async {
                  await manageSteps(steps, context);
                },
                child: Text('Edit Steps'),
              ),
            ],
          ),
          actions: [
            /*  Cancel and return  */
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Cancel'),
            ),
            /*  Save button  */
            ElevatedButton(
              onPressed: () async {
                final name = nameController.text;
                final comment = commentController.text;

                /*  Check requirements to input  */
                if (name.length > 15 || name.length < 2) {
                  await showDialog(context: context, builder: (context) {
                    return AlertDialog(
                      title: Text('Name too long or short! Range is between '
                          '2 and 15 characters'),
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
                } else if (comment.length > 20) {
                  await showDialog(context: context, builder: (context) {
                    return AlertDialog(
                        title: Text('Comment too long! Range is between '
                            '0 and 20 characters'),
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
                } else if (steps.isEmpty) {
                  await showDialog(context: context, builder: (context) {
                    return AlertDialog(
                        title: Text('No steps were provided!'),
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
                } else if (name.isNotEmpty) {
                  /*  Requirements fulfilled -> save recipe  */
                  await DatabaseHelper.instance
                      .createRecipe(name, comment, steps);
                  Navigator.pop(context);
                  Navigator.push(context, routeAction(2));
                }
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }

  /*  Same as new recipe, but loads from existing data  */
  Future<void> editRecipe(
      Map<String, dynamic> recipe,
      List<Map<String, dynamic>> steps,
      context
      ) async {
    final nameController = TextEditingController(text: recipe['name']);
    final commentController = TextEditingController(text: recipe['comment']);
    List<Map<String, dynamic>> updatedSteps = List.from(steps);

    await showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Edit Recipe'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Recipe Name'),
                keyboardType: TextInputType.text
              ),
              TextField(
                controller: commentController,
                decoration: InputDecoration(labelText: 'Comment'),
                keyboardType: TextInputType.text
              ),
              ElevatedButton(
                onPressed: () async {
                  await manageSteps(updatedSteps, context);
                },
                child: Text('Manage Steps'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                final updatedName = nameController.text;
                final updatedComment = commentController.text;

                if (updatedName.length > 15 || updatedName.length < 2) {
                  await showDialog(context: context, builder: (context) {
                    return AlertDialog(
                        title: Text('Name too long or short! Range is between '
                            '2 and 15 characters'),
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
                } else if (updatedComment.length > 20) {
                  await showDialog(context: context, builder: (context) {
                    return AlertDialog(
                        title: Text('Comment too long! Range is '
                            '0 and 20 characters'),
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
                } else if (updatedName.isNotEmpty) {
                  final db = DatabaseHelper.instance;
                  /* Update the recipe details  */
                  await db.database.then((database) {
                    database.update(
                      'recipes',
                      {
                        'name': updatedName,
                        'comment': updatedComment,
                      },
                      where: 'id = ?',
                      whereArgs: [recipe['id']],
                    );
                  });
                  /* Replace steps in the steps table  */
                  final tableName = 'steps_${recipe['id']}';
                  await db.database.then((database) async {
                    /*  Clear the existing steps  */
                    await database.delete(tableName);
                    /*  Insert the updated steps  */
                    for (var step in updatedSteps) {
                      await database.insert(tableName, step);
                    }
                  });
                  Navigator.push(context, routeAction(2));
                }
                Navigator.pop(context);
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }

  /*  Function to add, delete and display steps in current recipe dialog  */
  Future<void> manageSteps(
      List<Map<String, dynamic>> steps,
      BuildContext context
      ) async {
    /*  Currently displayed step  */
    int currentIndex = 0;

    await showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              title: Text('Manage Steps'),
              content: SizedBox(
                child: steps.isEmpty
                    ? Text('No steps added yet.')
                    : Container(
                  width: MediaQuery.of(context).size.width * 0.8,
                  height: MediaQuery.of(context).size.height * 0.25,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.all(Radius.circular(20)),
                      color: Colors.white12
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Step ${currentIndex + 1}',
                          style: TextStyle(fontSize: 25),),
                        SizedBox(
                          height: MediaQuery.of(context).size.height * 0.05
                        ),
                        Text('${steps[currentIndex]['name']
                            ?? ''}\n${steps[currentIndex]['mass_for_scale']
                            ?? ''} g', style: TextStyle(fontSize: 20),
                        ),
                        Text('${steps[currentIndex]['info'] ?? ''}'),
                      ],
                    ),
                  )
              ),
              actions: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    IconButton(onPressed: () {
                      if (currentIndex > 0) {
                        currentIndex--;
                        setState(() {});
                      }
                    }, icon: Icon(Icons.arrow_back)),
                    IconButton(onPressed: () {
                      if (currentIndex < steps.length - 1) {
                        currentIndex++;
                        setState(() {});
                      }
                    }, icon: Icon(Icons.arrow_forward)),
                    TextButton(
                      onPressed: () {
                        if (steps.isNotEmpty) {
                          steps.removeAt(currentIndex);
                          if (currentIndex > 0) {
                            currentIndex = steps.length - 1;
                          }
                          setState(() {});
                        }
                      },
                      child: Text('Delete Step',
                        style: TextStyle(color: Colors.red)
                      ),
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.05,),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: () {
                        final nameController = TextEditingController();
                        final massController = TextEditingController();
                        final infoController = TextEditingController();

                        showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: Text('Add Step'),
                              content: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  TextField(
                                      controller: nameController,
                                      decoration:
                                        InputDecoration(labelText: 'Step Name'),
                                      keyboardType: TextInputType.text
                                  ),
                                  TextField(
                                    controller: massController,
                                    decoration:
                                      InputDecoration(
                                          labelText: 'Mass for Scale'
                                      ),
                                    keyboardType: TextInputType.number,
                                    inputFormatters: <TextInputFormatter>[
                                      FilteringTextInputFormatter.digitsOnly
                                    ],
                                  ),
                                  TextField(
                                      controller: infoController,
                                      decoration:
                                        InputDecoration(labelText: 'Info'),
                                      keyboardType: TextInputType.text
                                  ),
                                ],
                              ),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.pop(context);
                                  },
                                  child: Text('Cancel'),
                                ),
                                ElevatedButton(
                                  onPressed: () async {
                                    if (nameController.text.length > 15
                                        || nameController.text.length < 2) {
                                      await showDialog(
                                          context: context,
                                          builder: (context) {
                                        return AlertDialog(
                                            title: Text('Name too long or '
                                                'short! Range is '
                                                '2 to 15 characters'),
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
                                    } else if (massController.text.isEmpty) {
                                      await showDialog(
                                          context: context,
                                          builder: (context) {
                                        return AlertDialog(
                                            title: Text('No mass was given!'),
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
                                    } else if (int.parse(massController.text)
                                        >= 500) {
                                      await showDialog(
                                          context: context,
                                          builder: (context) {
                                        return AlertDialog(
                                            title: Text('Too much mass! '
                                                'Range is 0 to 500g'),
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
                                    } else if (infoController.text.length
                                        >= 500) {
                                      await showDialog(
                                          context: context,
                                          builder: (context) {
                                        return AlertDialog(
                                            title: Text('Too much information!'
                                                ' Max is 500 characters.'),
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
                                    } else {
                                      steps.add({
                                        'name': nameController.text,
                                        'mass_for_scale': massController.text,
                                        'info': infoController.text,
                                      });
                                    }
                                    Navigator.pop(context);
                                    setState(() {});
                                  },
                                  child: Text('Add'),
                                ),
                              ],
                            );
                          },
                        );
                      },
                      child: Text('Add Step'),
                    ),
                    ElevatedButton(
                        onPressed: () { Navigator.pop(context); },
                        child: Text('Back')
                    )
                  ],
                )
              ],
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: bgColorScheme[0],
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          SizedBox(height: MediaQuery.of(context).size.height * 0.05),
          const TopBar(
            icons: [3,4,5],
            routes: [0,101,102],
            topText: "Recipes",
            colors: [4,4,4],
          ),
          SizedBox(height: MediaQuery.of(context).size.height * 0.075),
          Container(
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height * 0.75,
              decoration: BoxDecoration(
                color: bgColorStyle[3],
                borderRadius: borderSpecifications['allOuterBorderRadius'],
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
                  borderRadius: borderSpecifications['allInnerBorderRadius'],
                ),
                child: FutureBuilder<List<Map<String, dynamic>>>(
                  future: recipes,
                  builder: (context, snapshot) {
                    if (!snapshot.hasData) {
                      return Center(child: CircularProgressIndicator());
                    }

                    final recipes = snapshot.data!;
                    return ListView.builder(
                      itemCount: recipes.length,
                      itemBuilder: (context, index) {
                        final recipe = recipes[index];
                        return ListTile(
                          title: Text(
                            recipe['name'] ?? '',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20
                            ),
                          ),
                          subtitle: Text(
                            recipe['comment'] ?? '',
                            style: TextStyle(
                                color: Colors.white54,
                                fontSize: 15
                            ),
                          ),
                          trailing: SizedBox(
                            width: MediaQuery.of(context).size.width * 0.3,
                            child: Row(
                              children: [
                                IconButton(
                                  onPressed: () async {
                                    final steps = await DatabaseHelper.instance
                                        .getSteps(recipe['id']);
                                    editRecipe(recipe, steps, context);
                                    Navigator.push(
                                        context, routeAction(2)
                                    );
                                  },
                                  icon: Icon(Icons.mode_edit,
                                    color: Colors.white
                                  ),
                                ),
                                SizedBox(
                                    width: MediaQuery.of(context).size
                                        .width * 0.05
                                ),
                                IconButton(
                                  onPressed: () async {
                                    DatabaseHelper.instance
                                        .deleteRecipe(recipe['id']);
                                    Navigator.push(
                                        context, routeAction(2)
                                    );
                                  },
                                  icon: Icon(Icons.delete_forever,
                                    color: Colors.white
                                  ),
                                )
                              ],
                            ),
                          ),
                          onTap: () async {
                            if (currentRecipe != 0) {
                              closeRecipe();
                            }
                            currentRecipe = index + 1;
                            doneCount = 0;
                            currentStep = 0;
                            gSteps = List<Map<String, dynamic>>.from(
                                await DatabaseHelper.instance
                                    .getSteps(recipe['id'])
                            );
                            gRecipe = Map<String, dynamic>.from(recipe);

                            currentRecipeName = gRecipe['name'];

                            Navigator.push(context, routeAction(0));
                          },
                        );
                      },
                    );
                  },
                ),
              )
          )
        ],
      ),
    );
  }
}