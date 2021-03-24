import sqlite3 as sql
import pandas as pd


rugby_data = pd.read_csv('all_pages14_03_2021.csv')
rugby_data = rugby_data.iloc[::-1]
#print(rugby_data.iloc[0])

#rugby_data = rugby_data.rename(index={i:c for i,c in enumerate(reversed(range(len(rugby_data))))})
#print(rugby_data.iloc[0])
conn = sql.connect('rugby_data.db')

#rugby_data.to_sql('rugby_data', conn, index_label ='id')

c = conn.cursor()

# c.execute("""CREATE TABLE rugby_data (
#             Home_Team TEXT,
#             Away_Team TEXT,
#             Home_Score INTEGER,
#             Away_Score INTEGER,
#             Date TEXT,
#             Tournament TEXT,
#             SQUAD INTEGER
#             )""") 

# c.execute("INSERT INTO employees VALUES ('Mary', 'Schafer', 70000)")
# conn.commit()

last_row = tuple(c.execute("SELECT * FROM rugby_data where id= (SELECT MAX(id) FROM rugby_data)"))
print(last_row)
print(last_row[0][3])
print(last_row[0][5])
if '14/03/2021' == last_row[0][5]:
    print('cool')
max_id = list(c.execute("SELECT MAX(id) FROM rugby_data").fetchall()[0])[0]
print(f'max_id is {max_id+1} pppp ')

for value, index in enumerate(['a','b','c']):
    print(index)
bbb = ['a','b','c','d','e','f','g','h']
#for index in reversed(range(len(bbb))):
#    print(bbb[index])
max_id_v = 100
id_list = [num_2 for num_2 in reversed(range(max_id_v+1,max_id_v+1+len(bbb)))]
print(id_list)
#below works!!!!!!
#c.execute(f"INSERT INTO rugby_data (id, Home_Team, Away_Team, Home_score, Away_Score, Date, Tournament) VALUES ({max_id+1},'Home_Team', 'Away_Team', 9, 9, 'Date', 'Tournament')")

#c.execute("DELETE FROM rugby_data WHERE id=13839")

#c.execute("ALTER TABLE RENAME COLUMN index to numer;")


# print(c.fetchall())


conn.commit()

conn.close()