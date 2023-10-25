from robit.db.sqlite import SqliteDB

JOB_RESULT_TABLE_NAME = 'job_results'

JOB_RESULT_TABLE_STRUCTURE = {
    'pk': 'int',
    'job_id': 'varchar',
    'name': 'text',
    'result': 'text',
}


def insert_job_result(job_id: str, name: str, result: str) -> None:
    db = SqliteDB()
    db.create_table_if_does_not_exist(JOB_RESULT_TABLE_NAME, JOB_RESULT_TABLE_STRUCTURE)
    db.insert(JOB_RESULT_TABLE_NAME, {
        'pk': None,
        'job_id': job_id,
        'name': name,
        'result': result,
    })


def select_job_results(job_id: str) -> list:
    db = SqliteDB()
    db.cursor.execute(f'SELECT result FROM job_results WHERE job_id="{job_id}"')
    return db.cursor.fetchall()