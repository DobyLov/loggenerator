Log generator
==================

**A command line application to generate random logs.**

Log gen.

Wordlist sources:

- http://www.talkenglish.com/vocabulary/top-500-adjectives.aspx
- http://www.talkenglish.com/vocabulary/top-1500-nouns.aspx

Hastags list source
- https://www.shopify.com/blog/instagram-hashtags

Installation
------------

Need Python 3.6 minimum

Using pip:

``sudo pip3 install log_generator``

Manual:

``git clone `https://github.com/DobyLov/loggenerator`

``cd loggenerator``

``setup.py install``

Usage
-----

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
