# loggenerator

loggenerator is a Python library to generate fake logs with date, username, hastags, comments, age, UUID, location, fake world ip address
with an random frequency.
You can generate log with screen only, write log file, send log to a web server, to elastic server, with bulk_mode

## Installation

Need Python 3.6 minimum

Using pip:

``sudo pip3 install log_generator``

Manual:

``git clone https://github.com/DobyLov/loggenerator``

``cd loggenerator``

``setup.py install``


cd 
```
git clone 
setup.py insall
ou
pip install loggenerator
```

## Usage

```Usage

Open a terminal and run ``loggen``. The following options are available:

+---------------------------+------------------------------------------+
| Command line argument     | Description                              |
+===========================+==========================================+
| ``-h``, ``--help``        | show this help message and exit          |
+---------------------------+------------------------------------------+
| ``--num NUMBER``          | change number of usernames generated     |
+---------------------------+------------------------------------------+
| ``--speed_gen NUMBER``    | genlog rate: 1 slow, 2 middle, 3 high    |
+---------------------------+------------------------------------------+
| ``--fname FILE NAME``     | Save output in a text file               |
+---------------------------+------------------------------------------+
| ``--infinite``            | generate logs to infinite (until escape) |
+---------------------------+------------------------------------------+
| ``--webip`` ipdestination | send Logs to specified host              |
+---------------------------+------------------------------------------+
| ``--no_pause`` no pause   | no pause between two logs                |
+---------------------------+------------------------------------------+
| ``--esapiip IP``          | send logs to elastic server              |
+---------------------------+------------------------------------------+
| ``--kfkip IP``            | send logs to kafka broker                |
+---------------------------+------------------------------------------+
| ``--kfktopic``            | specify kafka topic destination          |
+---------------------------+------------------------------------------+
```

## Log example

loggen --num 100 --esapiip 192.168.1.150 --no_pause

`Log style`

```
174.126.127.134 2020-1-28 21:51:36  @Educational_Affair ["#igers", "#beach", "#followmeplease"] "Cras ac purus id lectus varius malesuada. Nulla sodales tellus nec cursus ultricies. Fusce non tempus massa, at blandit ipsum. Mauris eu lacus orci. Etiam pulvinar scelerisque lorem quis congue. Quisque bibendum felis in purus aliquet congue et ac arcu. Nunc sodales nisl semper, hendrerit ligula ac, interdum sem. Praesent ultricies, libero vel rhoncus fermentum, ante ligula ultricies sapien, sed lacinia nisl ipsum fringilla ipsum. Sed finibus a dui a suscipit. Aenean blandit ornare blandit. Sed hendrerit tincidunt tellus, sit amet varius orci. Morbi volutpat mollis ullamcorper. Fusce purus nisl, ullamcorper a dui at, blandit mollis purus. Mauris ultricies nibh a congue finibus. Morbi viverra lectus vitae porttitor auctor. Maecenas aliquet nunc id metus fringilla, in elementum sapien aliquam. Curabitur at turpis finibus, luctus neque non, sλ {'ip_address': '174.126.127.134', 'dateTime': '2020-1-28 21:51:36', 'user': ' @Educational_Affair', 'hasTags': '["#igers", "#beach", "#followmeplease"]', 'message_tweet': 'Cras ac purus id lectus varius malesuada. Nulla sodales tellus nec cursus ultricies. Fusce non tempus massa, at blandit ipsum. Mauris eu lacus orci. Etiam pulvinar scelerisque lorem quis congue. Quisque bibendum felis in purus aliquet congue et ac arcu. Nunc sodales nisl semper, hendrerit ligula ac, interdum sem. Praesent ultricies, libero vel rhoncus fermentum, ante ligula ultricies sapien, sed lacinia nisl ipsum fringilla ipsum. Sed finibus a dui a suscipit. Aenean blandit ornare blandit. Sed hendrerit tincidunt tellus, sit amet varius orci. Morbi volutpat mollis ullamcorper. Fusce purus nisl, ullamcorper a dui at, blandit mollis purus. Mauris ultricies nibh a congue finibus. Morbi viverra lectus vitae porttitor auctor. Maecenas aliquet nunc id metus fringilla, in elementum sapien aliquam. Curabitur at turpis finibus, luctus neque non, suscipit massa. Pellentesque id aliquam enim. Mauris nisi metus, auctor vel ullamcorper at, lobortis.', 'age': 44, 'uuid': '7edebcbf-27ad-4a47-99cc-87481cbf8f71', 'country': {'location': {'longitude': '41.850030', 'latitude': '-87.650050'}, 'country_short': 'US', 'country_long': 'United States', 'region': 'Illinois', 'town': 'Chicago', 'time_zone': '-06:00'}}
```

`JSON style`

```
{'ip_address': '174.126.127.134', 'dateTime': '2020-1-28 21:51:36', 'user': ' @Educational_Affair', 'hasTags': '["#igers", "#beach", "#followmeplease"]', 'message_tweet': 'Cras ac purus id lectus varius malesuada. Nulla sodales tellus nec cursus ultricies. Fusce non tempus massa, at blandit ipsum. Mauris eu lacus orci. Etiam pulvinar scelerisque lorem quis congue. Quisque bibendum felis in purus aliquet congue et ac arcu. Nunc sodales nisl semper, hendrerit ligula ac, interdum sem. Praesent ultricies, libero vel rhoncus fermentum, ante ligula ultricies sapien, sed lacinia nisl ipsum fringilla ipsum. Sed finibus a dui a suscipit. Aenean blandit ornare blandit. Sed hendrerit tincidunt tellus, sit amet varius orci. Morbi volutpat mollis ullamcorper. Fusce purus nisl, ullamcorper a dui at, blandit mollis purus. Mauris ultricies nibh a congue finibus. Morbi viverra lectus vitae porttitor auctor. Maecenas aliquet nunc id metus fringilla, in elementum sapien aliquam. Curabitur at turpis finibus, luctus neque non, suscipit massa. Pellentesque id aliquam enim. Mauris nisi metus, auctor vel ullamcorper at, lobortis.', 'age': 44, 'uuid': '7edebcbf-27ad-4a47-99cc-87481cbf8f71', 'country': {'location': {'longitude': '41.850030', 'latitude': '-87.650050'}, 'country_short': 'US', 'country_long': 'United States', 'region': 'Illinois', 'town': 'Chicago', 'time_zone': '-06:00'}}
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
