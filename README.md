# Vrum Vrum Locadora

Este é um sistema de gerenciamento para uma locadora de veículos, desenvolvido para gerenciar o cadastro de clientes, veículos, locações e devoluções. O sistema é projetado para otimizar o processo de locação, incluindo o cálculo de valores de aluguel, histórico de locações e multas.

## Estrutura do Projeto

O projeto foi estruturado para oferecer uma interface amigável para a equipe de atendimento da locadora.

### Entidades Principais
- **Pessoa**: Dados básicos das pessoas cadastradas no sistema (Clientes e Usuários).
- **Cliente**: Herda de Pessoa e contém informações adicionais, como CNH.
- **Usuário**: Herda de Pessoa e representa os funcionários que acessam o sistema.
- **Veículo**: Contém dados dos veículos disponíveis para locação.
- **Locação**: Registra uma nova locação, associando um cliente a um veículo específico.
- **Devolução**: Registra a devolução de um veículo, calculando multas e valores totais.

## Tecnologias Utilizadas

- **SQLite**: Banco de dados para armazenamento das informações.
- **Diagrama de classes**: Foi utilizado para auxiliar no desenvolvimento do software.
- **Diagrama MER**: Foi utilizado para o planejamento do banco de dados e mapeamento das entidades.
- **SQL**: Para criação das tabelas e definição das chaves primárias e estrangeiras.
