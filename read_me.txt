-Tanıtım

## Veri Seti: 
- https://github.com/erkansirin78/datasets/raw/master/sensors_instrumented_in_an_office_building_dataset.zip

## Veri Seti Kaynağı: 
- https://www.kaggle.com/ranakrc/smart-building-system


## Açıklama: Veri seti 
Bu veri seti, UC Berkeley'deki Sutardja Dai Salonu'nun (SDH) 4 katındaki 51 odada konumlanmış 255 sensör zaman serisinden toplanmıştır. Bir binadaki bir odanın fiziksel özelliklerindeki paternleri araştırmak için kullanılabilir. Ayrıca, Nesnelerin İnterneti (IoT), sensör füzyon ağı veya zaman serisi görevleriyle ilgili deneyler için de kullanılabilir. Bu veri seti hem denetimli (sınıflandırma ve regresyon) hem de denetimsiz öğrenme (kümeleme) görevleri için uygundur.

Her oda 5 tür ölçüm içerir: 
- CO2 konsantrasyonu, 
- humidity: oda hava nemi, 
- temperature: oda sıcaklığı, 
- light: parlaklık 
- PIR: hareket sensörü verileri

Veri 23 Ağustos 2013 Cuma ile 31 Ağustos 2013 Cumartesi arasında bir haftalık bir süre boyunca toplanmıştır. Hareket sensörü (PIR) her 10 saniyede bir değer üretir. Kalan sensörler her 5 saniyede bir değer üretir. Her dosya içinde zaman damgası ve sensör değerini içerir.

Pasif kızılötesi sensör (PIR sensörü), görüş alanındaki nesnelerden yayılan kızılötesi (IR) ışığı ölçen ve bir odadaki doluluğu ölçen elektronik bir sensördür. PIR verilerinin yaklaşık %6'sı sıfır değildir ve odanın doluluk durumunu gösterir. PIR verilerinin kalan %94'ü sıfırdır ve boş bir oda olduğunu gösterir.


-Görevler

1. Veriyi indir ve Dataframe haline getir.
``` 
            event_ts_min 	ts_min_bignt room 	co2         light 	    temp 	    humidity 	pir
0 	2013-08-24 02:04:00 	1377299040 	656A 	578.500000 	176.500000 	24.370001 	49.900002 	28.500000 
1 	2013-08-24 02:04:00 	1377299040 	746 	633.000000 	29.000000 	23.059999 	52.840000 	21.000000
2 	2013-08-24 02:05:00 	1377299100 	413 	494.727273 	96.555556 	23.927778 	45.330001 	0.000000
3 	2013-08-24 02:05:00 	1377299100 	421 	362.900000 	194.700000 	22.837000 	52.877999 	0.000000
``` 

2. Dataframe’i diske yaz.

3. Dataframe olarak diske yazılmış veri setini data-generator kullanarak Kafka’ya produce et.

4. Spark Streaming ile Kafka’dan veriyi consume et.

5. Spark Streaming içinde veriyi istenen formata getir ve Elasticsearch’e yaz.

6. Kibana üzerinde dashboard oluştur.


- Data Generator İçin

https://github.com/erkansirin78/data-generator/blob/master/readme.md

Intro
It is easy to find data sources for batch processing, but it is hard to tell same for realtime processing. This repo aims to make easy realtime data processing developments by streaming static datasets to file, postgresql, Apache Kafka, AWS S3/MinIO. There are 4 python scripts:

Stream data to file (dataframe_to_log.py) as log files
PostgreSQL (dataframe_to_postgresql.py)
Kafka (dataframe_to_kafka.py)
AWS S3 (dataframe_to_s3.py)
You must use ** Python3 **.

Installation
erkan@ubuntu:~$ git clone https://github.com/erkansirin78/data-generator.git

erkan@ubuntu:~$ python3 -m pip install virtualenv

erkan@ubuntu:~$ cd data-generator/

erkan@ubuntu:~/data-generator$ python3 -m virtualenv datagen

erkan@ubuntu:~/data-generator$ source datagen/bin/activate

(datagen) erkan@ubuntu:~/data-generator$ pip install -r requirements.txt
