class Controller:
    @staticmethod
    def get_transaction_th():
        header_dict = {
            "origin_bank": "Banco Origem",
            "origin_agency": "Agência Origem",
            "origin_account": "Conta Origem",
            "destination_bank": "Banco Destino",
            "destination_agency": "Agência Destino",
            "destination_account": "Conta",
            "transaction_value": "Valor",
            "transaction_date": "Data das Transações",
            "upload_user_email": "Usuário"
            }
        return header_dict


    @staticmethod
    def get_imported_th():
        header_dict = {
            "transaction_date": "Data das Transações",
            "upload_date": "Data do Upload",
            "upload_user_email": "Usuário",
            }
        return header_dict


    @staticmethod
    def get_users_th():
        header_dict = {
            "username": "Usuário",
            "email": "E-mail",
            }
        return header_dict


    @staticmethod
    def get_uploader_th():
        header_dict = {
            "transaction_date": "Data das Transações",
            "upload_user_email": "Usuário",
            "upload_date": "Data da Importação"
            }
        return header_dict


    @staticmethod
    def get_sus_tr_th():
        header_dict = {
            "origin_bank": "Banco Origem",
            "origin_agency": "Agência Origem",
            "origin_account": "Conta Origem",
            "destination_bank": "Banco Destino",
            "destination_agency": "Agência Destino",
            "destination_account": "Conta Destino",
            "transaction_value": "Valor",
            "transaction_date": "Data das Transações"
            }
        return header_dict


    @staticmethod
    def get_sus_acc_th():
        header_dict = {
            "0": "Banco",
            "1": "Agência",
            "2": "Conta",
            "3": "Data das Transações",
            "4": "Total Transacionado",
            "5": "Tipo de Transação"
            }
        return header_dict


    @staticmethod
    def get_sus_ag_th():
        header_dict = {
            "0": "Banco",
            "1": "Agência",
            '2': "Data das Transações",
            "3": "Valor Movimentado",
            "4": "Tipo de Movimentação"
            }
        return header_dict


    @staticmethod
    def get_date_tables(results):
        date_list = list()
        for result in results:
            date_list.append(result[0].transaction_date)
        return date_list