-- 10 sample patients
INSERT INTO patient (
    medical_record_number, first_name, last_name,
    date_of_birth, gender, phone, email, password,
    address, BloodType
) VALUES
  ('MRN0001', 'John',     'Doe',        '1985-04-12', 'Male',   '+201001234567', 'john.doe@example.com',      'passJohn1',     '123 Nile St, Cairo, Egypt',    'O+'),
  ('MRN0002', 'Sarah',    'Ali',        '1990-11-30', 'Female', '+201012345678', 'sarah.ali@example.com',     'S@rahA90',      '45 Tahrir Sq, Cairo, Egypt',   'A-'),
  ('MRN0003', 'Ahmed',    'Hassan',     '1978-06-05', 'Male',   '+201023456789', 'ahmed.hassan@example.com',  'Ahm3dH!78',     '78 Garden City, Cairo, Egypt', 'B+'),
  ('MRN0004', 'Fatima',   'Hussein',    '2001-02-17', 'Female', '+201034567890', 'fatima.hussein@example.com','F@tima2001',    '12 Dokki St, Giza, Egypt',     'AB+'),
  ('MRN0005', 'Mohamed',  'Abdel',      '1969-09-23', 'Male',   '+201045678901', 'mohamed.abdel@example.com', 'MoAb1969',       '5 Maadi Ave, Cairo, Egypt',     'O-'),
  ('MRN0006', 'Lina',     'Farouk',     '1988-12-14', 'Female', '+201056789012', 'lina.farouk@example.com',   'Lin@F88',       '33 Heliopolis, Cairo, Egypt',   'A+'),
  ('MRN0007', 'Omar',     'Karim',      '1995-07-08', 'Male',   '+201067890123', 'omar.karim@example.com',    '0marK95',        '22 Zamalek, Cairo, Egypt',      'B-'),
  ('MRN0008', 'Yara',     'Mostafa',    '2003-05-19', 'Female', '+201078901234', 'yara.mostafa@example.com',  'Y@raM03',        '99 Nasr City, Cairo, Egypt',    'AB-'),
  ('MRN0009', 'Khaled',   'Saeed',      '1975-01-02', 'Male',   '+201089012345', 'khaled.saeed@example.com',  'Kha1ed75',       '14 Giza Rd, Giza, Egypt',       'O+'),
  ('MRN0010', 'Asmaa',    'El-Sayed',   '1992-10-27', 'Female', '+201090123456', 'asmaa.elsayed@example.com', 'Asm@a92',        '7 Downtown, Cairo, Egypt',      'B+');

-- 10 sample doctors

