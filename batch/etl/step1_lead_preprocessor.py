import mysql.connector
import json

input_file = open('stack_driver_extract.json')
json_array = json.load(input_file)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12er34ty",
  database="arisa"
)

intent_name_data = ''

for item in json_array:
    record = (item['textPayload'])
    if 'Dialogflow Response' in record:
        json_record = record[22:]
        list = json_record.splitlines()
        
        for i in list:
            i = i.lstrip()

            if i.startswith('session_id:'):
                session_id_data_temp = i.replace("\"","")
                session_id_data = session_id_data_temp.replace("session_id: ","")

            if i.startswith('timestamp:'):
                timestamp_data_temp = i.replace("\"","")
                timestamp_data = timestamp_data_temp.replace("timestamp: ","")

            if i.startswith('resolved_query:'):
                resolved_query_data_temp = i.replace("\"","")
                resolved_query_data = resolved_query_data_temp.replace("resolved_query: ","")

            if i.startswith('intent_name:'):
                intent_name_data_temp = i.replace("\"","")
                intent_name_data = intent_name_data_temp.replace("intent_name: ","")

            if i.startswith('speech:'):
                speech_data = i.replace("speech: ","")

            if i.startswith('code:'):
                response_code_data = i.replace("code: ","")

        print('*******'+session_id_data+"|"+timestamp_data+"|"+resolved_query_data+"|"+intent_name_data+"|"+response_code_data)
        mycursor = mydb.cursor()
        mycursor.execute('insert into chatlogs (session_id, timestamp, resolved_query, intent_name, response_code) values (%s, %s, %s, %s, %s)', (session_id_data, timestamp_data, resolved_query_data, intent_name_data, response_code_data))
        mydb.commit()

        try:
            processed_flag = 'N'
            mycursor2 = mydb.cursor()
            mycursor2.execute('insert into chatlogs_session_ids (session_id, timestamp, processed_flag) values (%s, %s, %s)', (session_id_data, timestamp_data, processed_flag))
            mydb.commit()
        except mysql.connector.Error as err:
            print("Insert to chatlogs table failed : {}".format(err))