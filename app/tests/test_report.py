import json
from datetime import datetime, time

def test_report_lost_item(test_client, init_database):
    # Login as user
    response = test_client.post('/auth/login', data=dict(
        username='testuser1',
        password='password123'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Report lost item
    data = {
        'item_id': 1,
        'item_name': 'Test Item',
        'date_lost': '2024-07-04',
        'time_lost': '14:30:00',
        'place_lost': 'Test Location',
        'contact': 'test@example.com',
        'description': 'Lost description',
        'primary_color': 'Red',
        'secondary_color': 'Blue'
    }
    response = test_client.post('/report/lost', 
                                data=json.dumps(data),
                                content_type='application/json')
    
    assert response.status_code == 201
    assert b'Lost report submitted successfully' in response.data

def test_report_found_item(test_client, init_database):
    # Login as user
    response = test_client.post('/auth/login', data=dict(
        username='testuser1',
        password='password123'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Report found item
    data = {
        'item_id': 1,
        'item_name': 'Test Item',
        'date_found': '2024-07-04',
        'time_found': '14:30:00',
        'place_found': 'Test Location',
        'contact': 'test@example.com',
        'description': 'Found description',
        'primary_color': 'Red',
        'secondary_color': 'Blue'
    }
    response = test_client.post('/report/found', 
                                data=json.dumps(data),
                                content_type='application/json')
    
    assert response.status_code == 201
    assert b'Found report submitted successfully' in response.data
