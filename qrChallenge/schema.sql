
CREATE Table usage(
                num int UNIQUE,
                qr1_used BOOLEAN DEFAULT FALSE,
                qr2_used BOOLEAN DEFAULT FALSE,
                CONSTRAINT fk_num FOREIGN KEY (num)
                REFERENCES solutions (id)
);

create TABLE solutions (
    id int  PRIMARY KEY unique,
    ind1 VARCHAR(4),
    ind2 VARCHAR(4),
    rep varchar(150)
);




