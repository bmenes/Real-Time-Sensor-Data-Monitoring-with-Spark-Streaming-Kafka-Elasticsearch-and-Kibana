from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, col
from elasticsearch import Elasticsearch

spark = SparkSession.builder.appName("Read From Kafka") \
    .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.12.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

es = Elasticsearch("http://es:9200")


index_name = "office_data_index"

try:
    es.indices.delete(index=index_name)
    print(f"{index_name} silindi.")
except Exception as e:
    print(f"{index_name} yok.")


office_index = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "custom_edge_ngram", "asciifolding"]
                    }
                },
                "filter": {
                    "custom_edge_ngram": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 10
                    }
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "event_ts_min": {"type": "date"},
            "ts_min_bignt": {"type": "integer"},
            "room": {"type": "keyword"},
            "co2": {"type": "integer"},
            "humidity": {"type": "float"},
            "light": {"type": "float"},
            "pir": {"type": "float"},
            "temperature": {"type": "float"}
        }
    }
}


es.indices.create(index=index_name, body=office_index)
print(f"{index_name} oluşturuldu.")


# Read data from kafka source
lines = (spark
.readStream
.format("kafka")
.option("kafka.bootstrap.servers", "kafka:9092")
.option("subscribe", "office-input")
.load())

lines2 = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


lines3 = lines2.withColumn("event_ts_min", F.split(F.col("value"), ",")[0].cast(TimestampType())) \
    .withColumn("ts_min_bignt", F.split(F.col("value"),",")[1].cast(IntegerType())) \
    .withColumn("room", F.split(F.col("value"), ",")[2].cast(StringType())) \
    .withColumn("co2", F.split(F.col("value"), ",")[3].cast(IntegerType())) \
    .withColumn("humidity", F.split(F.col("value"), ",")[4].cast(FloatType())) \
    .withColumn("light", F.split(F.col("value"), ",")[5].cast(FloatType())) \
    .withColumn("pir", F.split(F.col("value"), ",")[6].cast(FloatType())) \
    .withColumn("temperature", F.split(F.col("value"), ",")[7].cast(FloatType())) \
    .drop("value")
    
        
def write_to_elasticsearch(df, epoch_id):
    df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "es") \
        .option("es.port", "9200") \
        .option("es.resource", "office_data_index") \
        .mode("append") \
        .save()
        
    
    
    
    

checkpoint_dir = "file:///tmp/streaming/read_from_kafka"
# write result to console sink
streamingQuery = (lines3
.writeStream
.outputMode("append")
.trigger(processingTime="2 second")
.option("checkpointLocation", checkpoint_dir)
.option("numRows",20)
.option("truncate",False)
.foreachBatch(write_to_elasticsearch) 
.start())


# start streaming
streamingQuery.awaitTermination()