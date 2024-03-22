# 🛋 Chair calculator

This command line tool prints chair type statistics for the apartment and per room for the floor plan from the given file.

```
usage: app.py [-h] --file file_path

Prints the chair statistics of the floor plan.

options:
  -h, --help        show this help message and exit
  --file file_path  path to a file with the floor plan
```

The tool uses the [Span fill](https://en.wikipedia.org/wiki/Flood_fill#Span_filling) algorithm to find the chairs that belong to each room.

## Inputs and limitations

* Floor plan without walls considered as one room
* Room name labels should be in the `(room name)` format, where room name is an alphanumeric string, chairs are one of the `WPSC` characters, space is for floors, and walls are any other character
* Each room label and every chair character should be one symbol away from any wall on the plan, otherwise the application will crash
* Application crashes if there is any text other than a wall, a room label, or a chair character on the plan

## Reusability and extensibility

The `mask_room` and `print_mask` functions can be reused to create an application that identifies the rooms for the workers carrying the chairs during the home furnishing process.

## How to run for local development

1. Make sure that you have python and poetry installed with `asdf install`
2. Install project dependencies with `make deps`
3. Run tests with `make tests`
4. Run type checks with `make typeckeck`
5. Run application with `make run args="--file rooms.txt"`


## How to build for release

You can build the application for standalone execution with `make binary`. This will write the `chari_calculator` executable binary to the `/dist` directory.


## Copyright

Copyright © 2024 Ivan Rublev.

This project is licensed under the [MIT license](https://github.com/IvanRublev/Domo/blob/master/LICENSE.md).
