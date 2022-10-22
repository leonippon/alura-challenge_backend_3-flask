from controllers.database_transactions import Controller as dbTctrl
from controllers.file_handler import Controller as fhC
from controllers.transactions import Controller as trC


class Controller:
    @staticmethod
    def run_importer(request):
        # "Upload" file
        new_file_path = fhC.upload_file(request)
        # OPEN FILE
        filetype, file = fhC.open_file(new_file_path)
        # Create list of raw lines from file
        raw_list = fhC.create_raw_transactions_list(filetype, file)
        # Remove duplicate lines from raw list
        raw_dedup_list = trC.dedup_raw_list(raw_list)
        # Create list of objects from raw list
        tr_list = trC.create_obj_transactions_list(raw_dedup_list)
        # Validate list of transactions
        validated_list = Controller.validate_transaction_list(tr_list)
        # Upload transactions to server
        if validated_list:
            dbTctrl.transaction_list_upload(validated_list)


    @staticmethod
    def validate_transaction_list(transaction_list):
        # 1 - Check file with zero rows
        validated1 = trC.check_zero_rows(transaction_list)
        if validated1 is None:
            return []
        # 2 - Check lines with empty fields
        validated2 = trC.check_empty_attr(validated1)
        # 3 - Check if date is equal first row
        validated3 = trC.check_transaction_date(validated2)
        # 4 - Check if date isn't already uploaded to db
        validated4 = trC.check_prior_upload(validated3)
        if validated4:
            return validated3
        else:
            print('Error, date already uploaded!')