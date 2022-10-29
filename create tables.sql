CREATE TABLE Member(
	membershipId	VARCHAR(7)	NOT NULL,
    Name       VARCHAR(25),
	eMail       VARCHAR(25),
    faculty		VARCHAR(15),
    phoneNumber VARCHAR(8),
    PRIMARY KEY (membershipId));
    
    
CREATE TABLE Book(
	accessionNo		VARCHAR(10)	 NOT NULL,
    ISBN		VARCHAR(25),
    PRIMARY KEY (accessionNo));
    
CREATE TABLE Author(
	ISBN		VARCHAR(25)	NOT NULL,
    authorName		VARCHAR(50));
    
CREATE TABLE ISBN(
	ISBN		VARCHAR(25) NOT NULL,
    publisherYear		SMALLINT,
    publisher		VARCHAR(50),
    title		VARCHAR(100),
    PRIMARY KEY (ISBN));
    
    
    
    
CREATE TABLE Borrow(
	accessionNo		VARCHAR(10)	NOT NULL,
    membershipId	VARCHAR(7) NOT NULL,
    returnDate	DATE,
    PRIMARY KEY( accessionNo , membershipId));
    
CREATE TABLE Reservation(
	accessionNo		VARCHAR(10)	NOT NULL,
    membershipId	VARCHAR(7) NOT NULL,
    reserveDate	DATE,
    PRIMARY KEY( accessionNo , membershipId));
    
CREATE TABLE Fine(
	membershipId	VARCHAR(7) NOT NULL,
    paymentDate		DATE,
    paymentAmount	SMALLINT);

    

    
	
    
