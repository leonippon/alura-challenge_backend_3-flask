## Alura Challenges | Back End 3rd Edition | Web Application for Analysis of Financial Transactions in Flask
[ENGLISH VERSION](https://github.com/leonippon/alura-challenge_backend_4-node/edit/main/README.en.md)

#### History
> We need to develop a traditional web application (server-side) to perform analysis of thousands of financial transactions and identify possible suspicious transactions.
> To carry out this analysis, we will need to develop a screen for uploading files, which must support several different formats, as well as implementing algorithms for extracting, validating and persisting information. Good object-oriented practices, design patterns, and SOLID principles will be essential. A user CRUD, as well as authentication and authorization mechanisms, will also be developed to secure the application.

#### Observation
> Although the challenge was aimed to back-end, a template from [HTML5UP](https://html5up.net/) was used as a front-end base to upload the Flask server and test the application.

### Technologies Used
> - **LANG:** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
> - **FW:** ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
> - **DB:** ![SQLITE](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
> - **ORM:** ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-52B0E7?style=for-the-badge&logo=Sequelize&logoColor=white)
> - **AUTH:** ![BCRYPT](https://img.shields.io/badge/bcrypt-543DE0?style=for-the-badge&logo=bcrypt&logoColor=white)
> - **TEST:** ![Pytest](https://img.shields.io/badge/Pytest-239120?style=for-the-badge&logo=python&logoColor=white)
>
#### Transactions

##### Transaction Import
> Implement a 'Controller' class that will receive the request containing the file and for now you should just print in the console the name of the imported file and its size in megabytes.
> The file upload functionality must allow importing files in CSV or XML format, which will be the files containing all the financial transactions of the banks carried out on a given day.

![Upload](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/transacoes_importar.png)

##### Read the file
> Each line in the file represents a separate financial transaction and its information is separated by a comma.
> When reading the information read from the imported file, each line is printed on the console.
> A financial transaction in our application represents a transfer of value between bank accounts, and has the following information:
>
> - Source Bank
> - Origin Agency
> - Origin Account
> - Destination Bank
> - Destination Agency
> - Destination Account
> - Transaction Amount
> - Transaction Date
> - Responsible User ID

##### Validation of Information
> Each file must contain transactions from only a certain day.
> If the uploaded file is empty, an error message should be displayed to the user.
> The first transaction in the list will be used to determine the date of all transactions in the file.
> If there is any transaction with a different date, it will be ignored.
> It is not possible to upload transactions from one day that are already in the database.
> All transaction information is required.

##### Recording Information
> After the validation step of the transactions contained in the upload, they will be recorded in the DB.

##### Management of Uploads Made
> Table of Imported Transactions: Upload date and Transaction date.

##### Import Details
> In the imports table, there is a "Detail Import" button that takes you to another page.
> This page details who and when imported transactions, as well as a table of all imports for that day.

![Imported](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/transacoes_importadas.png)

#### Other Screens
> - [Import File](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/transacoes_importar.png)
> - [Import Detail 1](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/detalhar_cabecalho.png)
> - [Import Detail 2](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/detalhar_corpo.png)
> - [Import Detail 2](https://github.com/leonippon/alura-challenge_backend_3-flask/blob/master/screenshots/detalhar_corpo2.png)

#### Users
> To protect access to the application, we need to develop a user registry and then implement an access control mechanism.
> Implement a CRUD of users, containing a screen listing the registered users, with options for editing and deleting each record, and another with a form to register a new user.

##### User CRUD:
> only 2
Mais sobre o texto original
É necessário fornecer o texto original para ver mais informações sobre a tradução
Enviar feedback
Painéis laterais
Limite de caracteres: 5.000. Use as setas para traduzir mais.
