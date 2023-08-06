Viya CASual

A simple way to use Viya's tools in Python without getting too serious

    from ViyaCasual.Casual import Casual
    from Database import SqliteConnector

    casual_test = Casual(username='username', server='viya.server.com', password='password', db_conn=SqliteConnector('/tmp/sample.db'))
    table = casual_test.get_table('SYSTEM', 'SystemData')
    decision = casual_test.get_decision(name='Marketing Transaction Grouping', library='public', table_name='dm_table')
    
