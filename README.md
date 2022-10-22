## Alura Challenges | Back End 3ª Edição | Aplicação Web de Análise de Transações Financeiras em Flask
[ENGLISH VERSION](https://github.com/leonippon/alura-challenge_backend_4-node/edit/main/README.en.md)

#### História
> Precisamos desenvolver uma aplicação Web tradicional(server-side) para realizar análise de milhares de transações financeiras e identificar possíveis transações suspeitas.
> Para realizar essa análise, precisaremos desenvolver uma tela para upload de arquivos, que deve suportar diversos formatos distintos, bem como implementar algoritmos para extração, validação e persistência das informações. Boas práticas de orientação a objetos, design patterns e princípios SOLID serão essenciais. Também será desenvolvido um CRUD de usuários, bem como mecanismos de autenticação e autorização, para proteger a aplicação.

#### Transações

##### Importação de Transações
> Implemente uma classe 'Controller' que receberá a requisição contendo o arquivo e por enquanto você deve apenas imprimir no console o nome do arquivo importado e seu tamanho em megabytes.
> A funcionalidade de upload de arquivos deve permitir importar arquivos no formato CSV ou XML, que serão os arquivos contendo todas as transações financeiras dos bancos realizadas em um determinado dia.

##### Leitura do arquivo
> Cada linha do arquivo representa uma transação financeira distinta e as informações dela são separadas por vírgula.
> Quando da leitura das imformações lidas do arquivo que foi importado, cada linha é impressa no console.
> Uma transação financeira em nossa aplicação representa uma transferência de valor entre contas bancárias, e possui as seguintes informações:
>
>   - Banco de Origem
>   - Agência de Origem
>   - Conta de Origem
>   - Banco de Destino
>   - Agência de Destino
>   - Conta de Destino
>   - Valor da Transação
>   - Data da Transação
>   - ID do Usuário Responssável
>

##### Validação das Informações
> Cada arquivo deverá conter transações de apenas um determinado dia.
> Se o arquivo que foi feito upload estiver vazio, uma mensagem de erro deve ser exibida para o usuário.
> A primeira transação da lista, será usada para determinar a data de todas transações do arquivo.
> Se houver alguma transação com outra data diferente, ela será ignorada.
> Não é possível realizar upload de transações de um dia que já consta no banco de dados.
> Todas as informações da transação são obrigatórias.

##### Gravação das Informações
> Após a etapa de validação das transações contidas no upload, elas serão gravadas no DB.

##### Gerenciamento dos Uploads Efetuados
> Tabela de Transações Importadas: Data do upload e Data das transações.

##### Detalha Importação
> Na tabela de importações, há um botão de "Detalhar Importação" que leva à outra página.
> Essa página, detalha quem e quando importou as transações, bem como uma tabela com todas importações desse dia.

#### Usuários
> Para proteger o acesso à aplicação, precisamos desenvolver um cadastro de usuários e posteriormente implementar um mecanismo de controle de acesso.
> Implemente um CRUD de usuários, contendo uma tela de listagem dos usuários cadastrados, com opções para edição e exclusão de cada registro, e outra com um formulário para cadastrar um novo usuário.

##### CRUD de Usuários:
> Apenas 2 informações serão necessárias no cadastro: Nome e Email, sendo ambas obrigatórias.
> A aplicação deve gerar uma senha aleatória para o usuário, composta de 6 números.
> A senha deverá ser enviada para o email do usuário sendo cadastrado.
> A senha não deve ser armazenada no banco de dados em texto aberto, devendo ser salvo um hash dela, gerado pelo algoritmo BCrypt.
> A aplicação não deve permitir o cadastro de um usuário com o email de outro usuário já cadastrado, devendo exibir uma mensagem de erro caso essa situação ocorra.
> A aplicação deve ter um usuário padrão previamente cadastrado, com nome: Admin, email: admin@email.com.br e senha: 123999.
> O usuário padrão não pode ser editado e nem excluído da aplicação, tampouco deve ser exibido na lista de usuários cadastrados.
> Qualquer usuário tem permissão para listar, cadastrar, alterar e excluir outros usuários.
> Um usuário não pode excluir ele próprio da aplicação.

##### Controle de Acesso:
> O controle de acesso na aplicação é por uma página de login.
> A aplicação restringe o acesso à todas as páginas(exceto a página de login) para os usuários que não estejam previamente autenticados.
> Há uma barra de menu na aplicação, contendo os links para as funcionalidades existentes, bem como um botão para o usuário realizar o logout. Esse menu somente deve ser exibido para usuários autenticados.

##### Responsável pela Transação
> Cada transação terá nela gravada o ID do usuário logado que realizou a importação do arquivo.
> A tabela de transações mostra o nome do usuário que realizou seu upload.

##### Exclusão de Usuários
> Será efetuado somente o _soft_ delete dos usuários, para que não se perca o registro de quem efetuou uploads mesmo que estes sejam excluídos do sistema.

#### Relatório de Transações Suspeitas
> Regras de Suspeição:
>   - Transação: Se seu valor for igual ou superior à R$100.000,00.
>   - Conta: Se enviou ou recebeu valor superior à R$100.000,00.
>   - Agência: Se a soma de todas traNsações do mês for superior à R$100.000,00.
>
> Será uma página com algumas tabelas que demonstram um resumo de informações seguindo as regras de análise.
> Poderá ser selecionado mês e ano para geração do relatório.
> Haverá uma tabela para cada uma das regras acima que for violada.
> Se nenhuma regra for violada no mês, haverá uma mensagem avisando.

#### Testes Automatizados
> Há um teste para cada regra descrita acima.