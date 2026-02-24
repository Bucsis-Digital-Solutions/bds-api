import hmac
from pg import connect

def validate(message, signature, secret):
    digest = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), 'sha256').hexdigest()
    return hmac.compare_digest(signature, f'sha256={digest}')

def update_time_entries(data):
    keys = []
    values = []
    placeholders = []

    for key in data:
        keys.append(key)
        values.append(data[key])
        placeholders.append('%s')

    query = f'''
        INSERT INTO bds.time_entries ({", ".join(keys)})
        VALUES ({", ".join(placeholders)})
        ON CONFLICT (toggl_id) DO UPDATE
            SET record_status = EXCLUDED.record_status,
            toggl_id = EXCLUDED.toggl_id,
            description = EXCLUDED.description,
            project_id = EXCLUDED.project_id,
            start = EXCLUDED.start,
            stop = EXCLUDED.stop,
            tags = EXCLUDED.tags,
            user_id = EXCLUDED.user_id
    '''

    conn = connect()
    cur = conn.cursor()
    
    cur.execute(query, tuple(values))
    conn.commit()

    if cur:
        cur.close()
    if conn:
        conn.close()