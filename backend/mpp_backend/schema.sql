DROP TABLE IF EXISTS elements;
DROP TABLE IF EXISTS molecules;    

CREATE TABLE elements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  symbol VARCHAR UNIQUE NOT NULL,
  atomic_number INTEGER UNIQUE NOT NULL,
  name VARCHAR NOT NULL,
  category VARCHAR ,
  appearance VARCHAR,
  discovered_by VARCHAR,
  named_by VARCHAR,
  phase VARCHAR ,
  bohr_model_image VARCHAR,
  summary VARCHAR
);

CREATE TABLE molecules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  formula VARCHAR NOT NULL,
  logp FLOAT,
  primary_element_symbol VARCHAR ,
  primary_element INTEGER ,
  FOREIGN KEY (primary_element) REFERENCES elements(atomic_number)
);


-- asta nu trebuie ca o sa pun eu dupa gen nui b ai
-- insert into elements (name, category, atomic_number, appearance, discovered_by, named_by, phase, bohr_model_image, summary) values ('Hydrogen', 'Nonmetal', 1, 'colorless gas', 'Henry Cavendish', 'Antoine Lavoisier', 'Gas', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Bohr_model_of_Hydrogen.png/220px-Bohr_model_of_Hydrogen.png', 'Hydrogen is a chemical element with symbol H and atomic number 1. With a standard atomic weight of 1.008, hydrogen is the lightest element on the periodic table.');