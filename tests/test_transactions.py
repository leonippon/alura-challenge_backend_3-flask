from datetime import datetime
from flask import session, current_app
import re

transactions_dict_1 = { 
    'transaction_1': {
        '1_origin_bank': 'Banco Bradesco',
        '2_origin_agency': '0001',
        '3_origin_account': '00001-1',
        '4_destination_bank': 'Banco do Brasil',
        '5_destination_agency': '0002',
        '6_destination_account': '00002-1',
        '7_transaction_value': 250000.00,
        '8_transaction_date': '2001-01-01T01:01:01'
    },
    'transaction_2': {
        '1_origin_bank': 'Banco Bradesco',
        '2_origin_agency': '0001',
        '3_origin_account': '00001-1',
        '4_destination_bank': 'Banco do Brasil',
        '5_destination_agency': '0002',
        '6_destination_account': '00002-1',
        '7_transaction_value': 750000.00,
        '8_transaction_date': '2001-01-01T01:01:01'
    }
}

transactions_dict_2 = { 
    'transaction_1': {
        '1_origin_bank': 'Banco Bradesco',
        '2_origin_agency': '0001',
        '3_origin_account': '00001-1',
        '4_destination_bank': 'Banco do Brasil',
        '5_destination_agency': '0002',
        '6_destination_account': '00002-1',
        '7_transaction_value': 250000.00,
        '8_transaction_date': '2001-02-01T01:01:01'
    },
    'transaction_2': {
        '1_origin_bank': 'Banco Bradesco',
        '2_origin_agency': '0001',
        '3_origin_account': '00001-1',
        '4_destination_bank': 'Banco do Brasil',
        '5_destination_agency': '0002',
        '6_destination_account': '00002-1',
        '7_transaction_value': 750000.00,
        '8_transaction_date': '2001-03-01T01:01:01'
    }
}

class TestTransactions:
    def test_import_and_detail(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            assert session['user_logged'] == 'admin@email.com.br'
            # UPLOAD DATA
            client.post('/imports', json=transactions_dict_1)
            response = client.get('/imports')
            text_1 = response.get_data(as_text=True)
            # UPLOAD DUPLICATE DATA
            client.post('/imports', json=transactions_dict_1)
            response = client.get('/imports')
            text_2 = response.get_data(as_text=True)
            search = re.findall('2001-01-01', text_2)
            # DETAIL UPLOADED DATA
            response = client.post('/details', data={'tr_date': '2001-01-01'})
            text_3 = response.get_data(as_text=True)
            # ASSERT
            assert '2001-01-01' in text_1
            assert str(datetime.today().date()) in text_1
            assert len(search) == 2
            assert 'Banco Bradesco' in text_3
            assert '0001' in text_3
            assert '00001-1' in text_3
            assert 'Banco do Brasil' in text_3
            assert '0002' in text_3
            assert '00002-1' in text_3
            assert 'R$ 250000.00' in text_3
            assert '2001-01-01' in text_3
            assert 'R$ 750000.00' in text_3


    def test_import_bad_data(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            assert session['user_logged'] == 'admin@email.com.br'
            # UPLOAD DATA WITH BAD LINE
            client.post('/imports', json=transactions_dict_2)
            response = client.get('/imports')
            text_1 = response.get_data(as_text=True)
            # DETAIL UPLOADED DATA
            response = client.post('/details', data={'tr_date': '2001-02-01'})
            text_2 = response.get_data(as_text=True)
            # ASSERT
            assert '2001-01-01' in text_1
            assert str(datetime.today().date()) in text_1
            assert 'Banco Bradesco' in text_2
            assert '0001' in text_2
            assert '00001-1' in text_2
            assert 'Banco do Brasil' in text_2
            assert '0002' in text_2
            assert '00002-1' in text_2
            assert 'R$ 250000.00' in text_2
            assert '2001-02-01' in text_2
            assert '2001-03-01' not in text_2
            assert 'R$ 750000.00' not in text_2


    def test_reports(self, client, auth):
        with client:
            # LOGIN
            auth.login()
            assert session['user_logged'] == 'admin@email.com.br'
            # DETAIL UPLOADED DATA ON REPORTS
            response = client.post('/reports', data={'Transações': '2001-01-01'})
            text_1 = response.get_data(as_text=True)
            search_0 = re.findall('2001-01-01', text_1)
            # DETAIL UPLOADED DATA ON REPORTS
            response = client.post('/reports', data={'Transações': '2001-02-01'})
            text_2 = response.get_data(as_text=True)
            search_1 = re.findall('2001-02-01', text_2)
            # ASSERT
            assert 'Banco Bradesco' in text_1
            assert '0001' in text_1
            assert '00001-1' in text_1
            assert 'Banco do Brasil' in text_1
            assert '0002' in text_1
            assert '00002-1' in text_1
            assert 'R$ 250000.00' in text_1
            assert 'R$ 750000.00' in text_1
            assert 'R$ 1000000.00' in text_1
            assert len(search_0) == 8
            assert 'R$ 250000.00' in text_2
            assert 'R$ 750000.00' not in text_2
            assert 'R$ 1000000.00' not in text_2
            assert len(search_1) == 7