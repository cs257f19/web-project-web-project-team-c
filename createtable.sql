DROP TABLE IF EXISTS spy;
CREATE TABLE spy (
  pricedate date,
  openprice real,
  closeprice real,
  highprice real,
  lowprice real,
  adjcloseprice real,
  volume int
);

DROP TABLE IF EXISTS irx;
CREATE TABLE irx (
  pricedate date,
  openprice real,
  closeprice real,
  highprice real,
  lowprice real,
  adjcloseprice real,
  volume int
);

DROP TABLE IF EXISTS gld;
CREATE TABLE gld (
  pricedate date,
  openprice real,
  closeprice real,
  highprice real,
  lowprice real,
  adjcloseprice real,
  volume int
);

DROP TABLE IF EXISTS btc;
CREATE TABLE btc (
  pricedate date,
  openprice real,
  closeprice real,
  highprice real,
  lowprice real,
  adjcloseprice real,
  volume int
);