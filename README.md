# kprint

Programmatic printing in python. 

#### Note
This software was developed for the [`EPSON TM-T88IV`](http://www.epson.com.sg/epson_singapore/printers_and_all_in_ones/pos/product.page?product_name=Epson_TM-T88IV). However, this should work for most receipt printers. This only works for Debian based systems so far. 

#### Tested on

Raspbian Jessie,    --> YES   
Ubuntu 14.04        --> Not tested, but should work   
Debian Jessie       --> Not tested, but should work   
MacOS               --> Will never work   
Windows             --> Will never work   


# Installation

    $ git clone https://github.com/evdevs/kprint   
    $ cd kprint
    $ sudo ./install.sh
  
# Usage

    $ python print.py
  
# ToDo

- implement a flag to print from a file, given absolute path   
- make different templates for  reciept printing   
- create an API to allow a user to print with one line of code   
