CREATE TABLE IF NOT EXISTS giveAway (
  ServerID Integer PRIMARY KEY,
  ChannelID Integer
);

CREATE TABLE IF NOT EXISTS openAPI (
  ServerID Integer PRIMARY KEY,
  APIKey String
);
