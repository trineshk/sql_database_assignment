import sqlite3 as lite

# Functionality of the class 

class DatabaseManage(object):
    
    def __init__(self):
        global con

        try:
            con = lite.connect('videos.db')
            
            with con:
                cur = con.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS videos(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, tags TEXT)')
                
                
        except Exception as e:
            print('Error creating table ', str(e))
            return False
    
    
    def store_tags(self, video_id, tags_text):
        try:
            tags_list = tags_text.split(',')

            with con:
                cur = con.cursor()
                cur.execute("UPDATE videos SET tags = ? WHERE id = ?", (','.join(tags_list), video_id))
            return True
        except Exception as e:
            print('error storing tags', str(e))
            return False

    def insert_data(self, data):
        try:
            name, descrption, tags_text = data
            tags_list = tags_text.split(',') if tags_text else []
            with con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO videos(name, description, tags) VALUES (?,?, ?)", (name, descrption, ','.join(tags_list))
                    )

                return True
        except Exception as e:
            print('Error inserting into table ', str(e))
            return False
        
    

    def fetch_data(self):
        try:
            with con:
                cur = con.cursor()
                cur.execute("SELECT id, name, description, tags FROM videos")
                rows = cur.fetchall()

                data = []
                for row in rows:
                    video_id, name, description, tags_text = row
                    tags_list = tags_text.split(',') if tags_text else []
                    data.append((video_id, name, description, tags_list))

                return data
            
        except Exception as e:
            print('Error fetching table ', str(e))
            return[]


def main():

    db = DatabaseManage()

    print('\nPress 1. Add video details\n')
    print('\nPress 2. Fetch video details\n')
    
    choice = input('\n Enter your choice: \n')

    if choice == '1':
        name = input('\n Enter course name: ')
        description = input('\n Enter course description: ')
        tags_text = input('\n Enter tags seperated by commas(optional): ')

        if db.insert_data([name, description, tags_text]):
            print('\n Data inserted successfully')
        else:
            print('\n Oops.. something is wrong')

    elif choice == '2':
        print('\n :: Courses list :: \n')

        for index, item in enumerate(db.fetch_data()):
            print('\n Sl No: '+ (str(index + 1 )))
            print('\n Video Id: ' + str(item[0]))
            print('\n Video Name: ' + str(item[1]))
            print('\n Video Description: ' + str(item[2]))

            tags_list = item[3]
            tags_str = ','.join(tags_list)
            print('\n video tags: ' + tags_str)

            print('\n')

    else:
        print('BAD CHOICE')


if __name__ == '__main__':
    main()


    