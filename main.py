import ghostdb

if __name__ == "__main__":
    con = ghostdb.connect("test.ods")
    con.execute("CREATE TABLE peoples (id, name, age)")
    con.execute("INSERT INTO peoples (1, 'John Doe', 30) (2, 'Jane Doe', 29)")
    con.execute("SELECT * FROM peoples")
    con.disconnect()