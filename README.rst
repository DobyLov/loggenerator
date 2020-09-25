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
| ``-h``, ``--help``        | Show this help message and exit          |
+---------------------------+------------------------------------------+
| ``--num NUMBER``          | Change number of usernames generated     |
+---------------------------+------------------------------------------+
| ``--fname FILE NAME``     | Save output in a text file               |
+---------------------------+------------------------------------------+
| ``--speed_gen NUMBER``    | genlog rate: 1 slow, 2 middle, 3 high    |
+---------------------------+------------------------------------------+
| ``--infinite``            | loggen to infinite                       |
+---------------------------+------------------------------------------+
| ``--webip IPDEST``        | Send Log to specified web host           |
+---------------------------+------------------------------------------+
| ``--no_pause``            | no pause between two logs                |
+---------------------------+------------------------------------------+
| ``--esapiip IPDEST``      | send logs to elastic server              |
+---------------------------+------------------------------------------+
