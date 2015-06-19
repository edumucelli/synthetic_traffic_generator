# synthetic_traffic_generator

Synthetic traffic generator created from real data from more than 6.8 million subscribers in Mexico City.

The methodology involved in order to create this synthetic traffic generator has been described in [1]. 

### Usage 

`python run.py <number of synthetic users>`, e.g., `python run.py 10000`

### Output

The synthetic trace represents the data generated for all the users during one day, i.e., it represents all data *sessions* (refer to [1]) for each user during one day. After executing the generator, the traffic files are be stored in the directory './users/synthetic/'. There is one file per synthetic user and each line corresponds to a session as described and exemplified bellow:

`2013-08-25 07:30:32 0 27624.3102372 MO`

The example above shows an actual resulting line, all fields space-separated, thus, there are 5 fields for every line in the synthetic trace formatted as follows:

1. Day, this is a fixed day in the format `%Y-%m-%d` and it is hard-coded as 25th August, 2013 but it can be changed, and a simple code change allows it to generate for as many days as needed
2. Hour, in the format of `%H:%M:%S`, this represents the actual moment when the synthetic user generated traffic within the day
3. User ID
4. The traffic volume, in KiloBytes generated in this session
5. User class, in this example it is a MO that stands for *Middle Occasional* (please refer to [1] for a better description of each of the classes)   


[1] Eduardo Mucelli Rezende Oliveira, Aline Carneiro Viana, K. P. Naveen and Carlos Sarraute, *"Measurement-driven mobile data traffic modeling in a large metropolitan area"*, IEEE Percom, March 2014, Saint Louis, United States
