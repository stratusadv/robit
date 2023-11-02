from robit.db.table import Table


job_results_table = Table(
    name='job_results',
    fields={
        'job_id': 'TEXT',
        'type': 'TEXT',
        'message': 'TEXT',
        'datetime_entered': 'TEXT',
    }
)