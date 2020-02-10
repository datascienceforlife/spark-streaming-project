from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import time
import subprocess


def get_host():
    command = "ifconfig en0 | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/'"
    result = subprocess.check_output(command, shell=True)
    HOST = result.decode('utf-8')[:-2]  # Remove \n
    return HOST

# Stop info
#import log4p as logger
#logger.GetLogger("info").logging_level = 0


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)

TCP_IP = get_host()
TCP_PORT = 9999

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream(TCP_IP, TCP_PORT)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
