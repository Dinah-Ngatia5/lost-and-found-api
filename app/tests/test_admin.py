import json
from flask_login import login_user

def test_admin_dashboard_access(test_client, init_database):
    # Login as admin
    response = test_client.post('/auth/login', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Access admin dashboard
    response = test_client.get('/admin/dashboard')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'lost_reports' in data
    assert 'found_reports' in data
    assert 'claims' in data
    assert 'rewards' in data

def test_add_item(test_client, init_database):
    # Login as admin
    response = test_client.post('/auth/login', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Add item
    data = {
        'name': 'Test Item',
        'description': 'Test Description'
    }
    response = test_client.post('/admin/items', 
                                data=json.dumps(data),
                                content_type='application/json')
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'Item added successfully' in response_data['message']

def test_update_item(test_client, init_database):
    # Login as admin
    response = test_client.post('/auth/login', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Add item
    data = {
        'name': 'Test Item',
        'description': 'Test Description'
    }
    response = test_client.post('/admin/items', 
                                data=json.dumps(data),
                                content_type='application/json')
    assert response.status_code == 201

    # Update item
    update_data = {
        'name': 'Updated Test Item',
        'description': 'Updated Test Description'
    }
    response = test_client.put('/admin/items/1', 
                               data=json.dumps(update_data),
                               content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'Item updated successfully' in response_data['message']

def test_delete_item(test_client, init_database):
    # Login as admin
    response = test_client.post('/auth/login', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Add item
    data = {
        'name': 'Test Item',
        'description': 'Test Description'
    }
    response = test_client.post('/admin/items', 
                                data=json.dumps(data),
                                content_type='application/json')
    assert response.status_code == 201

    # Delete item
    response = test_client.delete('/admin/items/1')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'Item deleted successfully' in response_data['message']
