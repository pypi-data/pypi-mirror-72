oracle-connection
=================

This package is a new tool to connect Oracle database.

One important thing is that `I'm not the first author` of this package.
At the early time, this package was write by my ex-leader in 2017.
And it wasn't a package, just a python file named `my_modules`.
Then, we modified it last year. At last she left this company, Then
I refactored the code, deleted some methods uselsee.

Example
-------

To connect:

.. code-block:: python

    from oracle_connection import ConnectOracle
    from oracle_connection import DatabaseOperate

    conn = ConnectOracle(
        "your host",
        "your instance name",
        "your username",
        "your password"
    )
    cursor = DatabaseOperate(conn)
    # operations
    cursor.close_cursor()

Get datas from database:

.. code-block:: python

    # ...
    sql = """SELECT field1, field2 FROM table"""
    # get all rows
    rows = cursor.get_all(sql)
    # get first row
    row = cursor.get_one(sql)
    # get all datas and reformat it to a dataframe
    df = cursor.get_df(sql)
    sql = """SELECT field FROM table"""
    # get one column and reformat it to a list
    row_list = cursor.one_column_list(sql)
    cursor.close_cursor()

The other operations:

.. code-block:: python

    # ...
    value1, value2, value3 = 1, 2.2, "c"
    sql = """INSERT INTO table (field1, field2, field3
             ) VALUES (:value1, :value2, :value3)"""
    # insert one row into table
    cursor.execute_sql(
        sql, value1=value1, value2=value2, value3=value3
    )

    sql = """INSERT INTO table (field1, field2, field3
             ) VALUES (:1, :2, :3)"""
    data = [
        [1, 2.2, "c"],
        [2, 2.1, "d"],
        [3, 4.2, "f"],
        [4, 6.2, "g"]
    ]
    # insert many rows into table
    cursor.insert_data(sql, data=data)

    sql = """DELETE FROM table WHERE field=:value"""
    # delete datas from table
    cursor.execute_sql(sql, value=value1)
