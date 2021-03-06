#stworzenie tabeli
#%sql
#create table status_table(id string, runId string, name string, timestamp_field string, batchId int, numInputRows int, inputRowsPerSecond float, processedRowsPerSecond float, addBatch int, getBatch int, latestOffset int, queryPlanning int, triggerExecution int, walCommit int, sources string, sink string, instance string, memory int, cores int, testName string, transformation string, batchSize string, kafkaInputRate string )


# deklaracja parametrów testu
_instance = "i3.xlarge (2-4)"
_memory_GB=16
_cores=8
_test_name = "persist" # autoscaling etc
_transformation="data clearing" #grouping, filtering
_batch_size="10 seconds"
_kafka_input_rate="20 seconds"


from time import sleep
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, FloatType

# deklaracja typów danych dla Dataframe'u
schema = StructType([ \
    StructField("id",StringType(),True), \
    StructField("runId",StringType(),True), \
    StructField("name",StringType(),True), \
    StructField("timestamp_field",StringType(),True), \
    StructField("batchId",IntegerType(),True), \
    StructField("numInputRows",IntegerType(),True), \
    StructField("inputRowsPerSecond",FloatType(),True), \
    StructField("processedRowsPerSecond",FloatType(),True), \
    StructField("addBatch",IntegerType(),True), \
    StructField("getBatch",IntegerType(),True), \
    StructField("latestOffset",IntegerType(),True), \
    StructField("queryPlanning",IntegerType(),True), \
    StructField("triggerExecution",IntegerType(),True), \
    StructField("walCommit",IntegerType(),True), \
    StructField("sources",StringType(),True), \
    StructField("sink",StringType(),True), \
    StructField("instance",StringType(),True), \
    StructField("memory",IntegerType(),True), \
    StructField("cores",IntegerType(),True), \
    StructField("testName",StringType(),True), \
    StructField("transformation",StringType(),True), \
    StructField("batchSize",StringType(),True), \
    StructField("kafkaInputRate",StringType(),True), \
  ])

# pętla uruchamiająca zapis danych z lastProgress 30 razy w odstępach 10 sekundowych
for count in range(30):
  
  # warunek sprawdzający typ obiektu, aby uniknąć błędu, przy inicjacji streamu, gdy dany obiekt dopiero się tworzy
  if type(streamingQuery.lastProgress) is dict:
    
    # przejęcie wartości ze słownika lastProgress
    _id=streamingQuery.lastProgress['id']
    _runId=streamingQuery.lastProgress['runId']
    _name=streamingQuery.lastProgress['name']
    _timestamp=streamingQuery.lastProgress['timestamp']
    
    _batchId=streamingQuery.lastProgress['batchId']
    _numInputRows=streamingQuery.lastProgress['numInputRows']
    
    _inputRowsPerSecond=streamingQuery.lastProgress['inputRowsPerSecond']
    _processedRowsPerSecond=streamingQuery.lastProgress['processedRowsPerSecond']
    
    #durations - obsługa błędu KeyError - nie wszystkie wartości są zawsze podane w lastProgress
    try: 
      _addBatch=streamingQuery.lastProgress['durationMs']['addBatch']
    except KeyError:
      _addBatch=0
    
    try:
      _getBatch=streamingQuery.lastProgress['durationMs']['getBatch']
    except KeyError:
      _getBatch=0
      
    try:
      _latestOffset=streamingQuery.lastProgress['durationMs']['latestOffset']
    except KeyError:
      _latestOffset=0
      
    try:
      _queryPlanning=streamingQuery.lastProgress['durationMs']['queryPlanning']
    except KeyError:
      _queryPlanning=0
      
    try:
      _triggerExecution=streamingQuery.lastProgress['durationMs']['triggerExecution']
    except KeyError:
      _triggerExecution=0
      
    try:
      _walCommit=streamingQuery.lastProgress['durationMs']['walCommit']
    except KeyError:
      _walCommit=0

    # lista sources jest zapisywana jako string
    _sources=str(streamingQuery.lastProgress['sources'])
    # słownik sink jest zapisywany jako string
    _sink=str(streamingQuery.lastProgress['sink'])
  
  
    #stworzenie rekordu danych
    new_data=[(_id,_runId,_name,_timestamp,_batchId,_numInputRows,_inputRowsPerSecond,\
               _processedRowsPerSecond,_addBatch,_getBatch,_latestOffset,_queryPlanning,_triggerExecution,_walCommit,_sources,_sink,\
              _instance, _memory_GB, _cores, _test_name, _transformation, _batch_size, _kafka_input_rate)]
  
    # stworzenie Dataframe'u składającego się z rekordu new_data i zdefiniowanego schematu danych 
    df = spark.createDataFrame(data=new_data,schema=schema)
    df.write.insertInto("status_table",overwrite = False)
   
  # poczekaj 10 sekund przed kolejnym zapisem informacji z lastProgress 
  sleep(10)
