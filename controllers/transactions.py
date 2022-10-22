from controllers.database_transactions import Controller as dbTctrl
from flask import session, flash
import db.models as models
import uuid as uuid_pkg
import datetime

class Transaction:
    @staticmethod
    def create_fields():
        transaction_fields = [
            "origin_bank", "origin_agency", "origin_account",
            "destination_bank", "destination_agency", "destination_account",
            "transaction_value", "transaction_date"
            ]
        attr_fields = [
            "origin_bank", "origin_agency", "origin_account",
            "destination_bank", "destination_agency", "destination_account",
            "transaction_value", "transaction_date", "upload_date",
            "upload_user_email"
            ]
        tr_details_user_header = [
            "transaction_date", "upload_user_email", "upload_date"
        ]
        return transaction_fields, attr_fields, tr_details_user_header


transaction_fields, attr_fields, tr_details_user_header = Transaction.create_fields()
headers_list = [transaction_fields, attr_fields, tr_details_user_header]


class Controller:
    @staticmethod
    def create_obj_transactions_list(raw_list):
        # Declare lists
        transactions_list = list()
        # Create objects from rows
        for line in raw_list:
            newTr = models.Transaction()
            for i in (range(len(transaction_fields))):
                try:
                    setattr(newTr, transaction_fields[i], line[i])
                except:
                    print(f'Error assigning attr')
            newTr.id = str(uuid_pkg.uuid4())
            newTr.transaction_date = datetime.datetime.fromisoformat(newTr.transaction_date).date()
            newTr.upload_date = datetime.datetime.now().date()
            newTr.upload_user_email = session['user_logged']
            transactions_list.append(newTr)
        print("Object list created!")
        return transactions_list


    @staticmethod
    def dedup_raw_list(raw_list):
        # New list
        new_raw_list = list()
        [new_raw_list.append(item) for item in raw_list if item not in new_raw_list]
        # Check size difference
        dif = len(raw_list) - len(new_raw_list)
        if dif > 0:
            print(f'Removed {dif} duplicates from raw list!')
        else:
            print('No duplicates found!')
        return new_raw_list


    @staticmethod
    def check_zero_rows(transaction_list):
        if len(transaction_list) == 0 or type(transaction_list) is None:
            print('Validation #1 Error, empty file, zero rows!')
            flash('Erro! Arquivo em branco!')
            return []
        else:
            print("Validation #1 OK!")
            return transaction_list


    @staticmethod
    def check_empty_attr(transaction_list):
        print(f"Validation #2 (Start Length): {len(transaction_list)}")
        new_list = transaction_list.copy()
        for transaction in new_list:
            # Check ATTRS
            for attr in attr_fields:
                attr_value = getattr(transaction, attr)
                if attr_value == "" or attr_value == None:
                    # POP if Empty
                    print(f'Invalid transaction: {transaction}')
                    transaction_list.pop(transaction_list.index(transaction))
        # Check list not empty
        if len(transaction_list) != 0:
            print(f"Validation #2 (End Length): {len(transaction_list)}")
            print("Validation #2 OK!")
            return transaction_list
        else:
            print('Validation #2 Error, empty file, zero rows!')
            return []


    @staticmethod
    def check_transaction_date(transaction_list):
        print(f"Validation #3 (Start Length): {len(transaction_list)}")
        # Catch reference date
        ref_date = transaction_list[0].transaction_date
        new_list = transaction_list.copy()
        # Check row dates
        for item in new_list:
            if item.transaction_date != ref_date:
                print(f'Data da transação inválida: Ref({ref_date}) Invalid({item.transaction_date})')
                transaction_list.pop(transaction_list.index(item))
        # Check list not empty
        if len(transaction_list) != 0:
            print(f"Validation #3 (End Length): {len(transaction_list)}")
            print("Validation #3 OK!")
            return transaction_list
        else:
            print('Validation #3 Error, empty file, zero rows!')
            return []


    @staticmethod
    def check_prior_upload(transaction_list):
        if len(transaction_list) > 0:
            tr_date = transaction_list[0].transaction_date
            validated4 = dbTctrl.transaction_query_detailed(tr_date, True)
            if validated4:
                return True
            else:
                return False


    @staticmethod
    def reorder_data(out_in_list):
        new_result = list()
        # OUT LIST
        for out_transaction in out_in_list[0]:
            new_transaction = list()
            transaction_type = "Saída"
            for item in out_transaction:
                new_transaction.append(item)
            new_transaction.append(transaction_type)
            new_result.append(new_transaction)
        # IN LIST
        for in_transaction in out_in_list[1]:
            transaction_type="Entrada"
            new_transaction = list()
            for item in in_transaction:
                new_transaction.append(item)
            new_transaction.append(transaction_type)
            new_result.append(new_transaction)
        return new_result


    @staticmethod
    def unpack_transactions(transaction_list, attr_list):
        # TR LIST
        new_result = list()
        for transaction in transaction_list:
            # UNPACK TR
            new_transaction = list()
            for attr in headers_list[attr_list]:
                new_transaction.append(getattr(transaction[0], attr))
            # APPEND TR TO LIST
            new_result.append(new_transaction)
        return new_result


    @staticmethod
    def change_tf_format(transaction_list):
        # LOOP TR LIST
        if len(transaction_list) > 0:
            new_transaction_list = list()
            # LOOP TR
            for transaction in transaction_list:
                new_transaction = list()
                #LOOP ITEM
                for item in transaction:
                    # CHANGE FORMAT
                    if type(item) == float:
                        item = f'R$ {round(item, 2)}'
                    if type(item) == int:
                        item = f'R$ {item}.00'
                    # APPEND ITEM TO TR
                    new_transaction.append(item)
                # APPEND TR TO NEW TR LIST
                new_transaction_list.append(new_transaction)
            return new_transaction_list
        else:
            return []