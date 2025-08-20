create table if not exists sales (
                                  doc_id   varchar(6),
                                  item     text,
                                  category text,
                                  amount   smallint,
                                  price    smallint,
                                  discount numeric
                                 );                               