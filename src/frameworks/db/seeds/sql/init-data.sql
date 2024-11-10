INSERT IGNORE INTO `users` (id, name, email, password) VALUES 
  (1, "Pepe", "test1@mail.com", "scrypt:32768:8:1$ixo0slrUvaoHEGEN$8f67ea38cb2ec5504a679332208c0b193efb78cf30f10efe59c2789b190b0c0794c2bd0b8a9ff3981027a866814afb9c2f53c259a34ea017cb8aa2826abd9db8"),
  (2, "Pipo", "test2@mail.com", 
  "scrypt:32768:8:1$ixo0slrUvaoHEGEN$8f67ea38cb2ec5504a679332208c0b193efb78cf30f10efe59c2789b190b0c0794c2bd0b8a9ff3981027a866814afb9c2f53c259a34ea017cb8aa2826abd9db8"),
  (3, "Pepo", "test3@mail.com", 
  "scrypt:32768:8:1$ixo0slrUvaoHEGEN$8f67ea38cb2ec5504a679332208c0b193efb78cf30f10efe59c2789b190b0c0794c2bd0b8a9ff3981027a866814afb9c2f53c259a34ea017cb8aa2826abd9db8"),
  (4, "Pepa", "test4@mail.com", 
  "scrypt:32768:8:1$ixo0slrUvaoHEGEN$8f67ea38cb2ec5504a679332208c0b193efb78cf30f10efe59c2789b190b0c0794c2bd0b8a9ff3981027a866814afb9c2f53c259a34ea017cb8aa2826abd9db8"),
  (5, "Piri", "test5@mail.com", 
  "scrypt:32768:8:1$ixo0slrUvaoHEGEN$8f67ea38cb2ec5504a679332208c0b193efb78cf30f10efe59c2789b190b0c0794c2bd0b8a9ff3981027a866814afb9c2f53c259a34ea017cb8aa2826abd9db8");

INSERT IGNORE INTO `events` (id, name, owner_id, min_amount, max_amount) VALUES
  (1, "Test Contest", 1, 1000, 5000);

INSERT IGNORE INTO `event_users` (user_id, event_id, pick_id) VALUES
  (1, 1, 2),
  (2, 1, 3),
  (3, 1, 4),
  (4, 1, 5),
  (5, 1, 1);

INSERT IGNORE INTO `wishlist` (id, user_id, event_id, element, `url`) VALUES
  (1, 1, 1, "Tocomple", "https://upload.wikimedia.org/wikipedia/commons/e/e0/Completo_italiano.jpg"),
  (2, 1, 1, "Bibia Fruna", "https://fruna.restonauta.cl/wp-content/uploads/2021/03/Fruna-Bebida-Pina-500ml.jpg"),
  (3, 2, 1, "Chorito Hello Kitty", "https://i.pinimg.com/originals/a9/59/c1/a959c103d1980f400c463b5e54385ecc.png"),
  (4, 2, 1, "Cualquier cosita", "https://www.librerianorma.com/images/Caratula/Responsive/9789580016830.jpg");