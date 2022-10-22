from werkzeug.utils import secure_filename
from flask import current_app, flash
import defusedxml.ElementTree as xml
import json
import csv
import os

class Controller:
    @staticmethod
    def upload_file(request):
        # CHECK IF FILE EXISTS
        if 'file' not in request.files:
            # RETURN DICT FOR TESTS
            if type(request.json) == dict:
                return request.json
            print("Upload Error, no file received!")
            flash(f'Erro no Upload!')
        else:
            # Save
            file = request.files['file']
            new_fn = secure_filename(file.filename)
            new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_fn)
            file.save(new_path)
            # Print Size
            filesize = Controller.check_file_size(file)
            print(f'Size is {filesize}Kb') 
            return new_path


    @staticmethod
    def open_file(file2open):
        # RETURN DICT TO TEST
        if type(file2open) == dict:
            filetype = "JSON"
            return filetype, file2open
        # DECLARE
        filetype = False
        # TRY TO PARSE XML
        try:
            file = open(file2open, mode='r')
            xml_file = xml.parse(file)
            filetype = "XML"
            return filetype, xml_file
        except xml.ParseError:
            print('Not XML!')
        # TRY TO PARSE JSON
        if not filetype:
            try:
                file = open(file2open, mode='r')
                json_file = json.load(file)
                filetype = "JSON"
                return filetype, json_file
            except json.JSONDecodeError:
                print('Not JSON!')
        # TRY TO PARSE CSV
        if not filetype:
            try:
                file = open(file2open, mode='r')
                csv_file = csv.reader(file)
                filetype = "CSV"
                return filetype, csv_file
            except csv.Error:
                print('Not CSV!')
        # NOTHING WORKS
        print("ERROR! Couldn't open this file!")
        return [], []


    @staticmethod
    def create_raw_transactions_list(filetype, myfile):
        # CSV FILE 2 RAW LIST
        if filetype == "CSV":
            raw_transactions_list = list()
            for line in myfile:
                if len(line) > 0:
                    raw_transactions_list.append(line)
            return raw_transactions_list
        # XML FILE 2 RAW LIST
        elif filetype == "XML":
            raw_transactions_list = list()
            transactions = myfile.getroot()  # type: ignore
            for transaction in transactions:
                new_transaction = [text for text in transaction.itertext() if text.strip() != ""]
                if len(new_transaction) > 0:
                    raw_transactions_list.append(new_transaction)
            return raw_transactions_list
        # JSON FILE 2 RAW LIST
        elif filetype == "JSON":
            raw_transactions_list = list()
            transactions_from_dict = myfile.values()  # type: ignore
            for transaction in transactions_from_dict:
                new_transaction = [value for value in transaction.values()]
                if len(new_transaction) > 0:
                    raw_transactions_list.append(new_transaction)
            return raw_transactions_list
        else:
            return print('ERROR, filetype not supported!')


    @staticmethod
    def check_file_size(file):
        file.seek(0, 2)
        filesize = file.tell()
        nfilesize = filesize / 1024
        nnfilesize = round(nfilesize, 0)
        file.seek(0, 0)
        return nnfilesize